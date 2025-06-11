#!/usr/bin/env python3
"""
Advanced Multi-threaded Web Scraper

Features:
- Multi-threaded crawling with ThreadPoolExecutor
- URL deduplication (no duplicate URLs scraped)
- Content deduplication (no duplicate content saved)
- Respects robots.txt and rate limiting
- Saves content to files with timestamps
- Comprehensive logging and error handling
- Domain filtering (stays within same domain by default)
"""

import hashlib
import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import List, Set, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser

import requests
import urllib3
import xxhash
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(
        self,
        output_dir: str = "scraped_content",
        output_file: str = "scraped_content.txt",
        content_selector: str = "#main-content",
        allowed_paths: Optional[List[str]] = None,
        max_workers: int = 10,
        delay_between_requests: float = 1.0,
        max_pages: int = 100,
        same_domain_only: bool = True,
        respect_robots: bool = True,
        timeout: int = 30,
    ):
        """
        Initialize the web scraper.
        
        Args:
            output_dir: Directory to save scraped content
            output_file: Single file to save all scraped content
            content_selector: CSS selector for the main content element (e.g., "#main-content", ".content", "main", "article")
            allowed_paths: List of URL paths to include (e.g., ["/docs", "/api"]). If None, uses the starting URL's path as base
            max_workers: Maximum number of concurrent threads
            delay_between_requests: Delay between requests (seconds)
            max_pages: Maximum number of pages to scrape
            same_domain_only: Only scrape URLs from the same domain
            respect_robots: Respect robots.txt rules
            timeout: Request timeout in seconds
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.output_file = self.output_dir / output_file
        self.content_selector = content_selector
        self.allowed_paths = allowed_paths or []
        
        self.max_workers = max_workers
        self.delay_between_requests = delay_between_requests
        self.max_pages = max_pages
        self.same_domain_only = same_domain_only
        self.respect_robots = respect_robots
        self.timeout = timeout
        
        # Thread-safe sets and locks
        self.visited_urls: Set[str] = set()
        self.content_hashes: Set[str] = set()
        self.robots_cache: Dict[str, Optional[RobotFileParser]] = {}
        self.url_lock = Lock()
        self.content_lock = Lock()
        self.robots_lock = Lock()
        
        # Statistics
        self.stats = {
            "pages_scraped": 0,
            "pages_skipped_duplicate_url": 0,
            "pages_skipped_duplicate_content": 0,
            "pages_failed": 0,
            "start_time": None,
            "end_time": None,
        }
        
        # Setup logging
        self._setup_logging()
        
        # HTTP session for connection pooling
        self.session = requests.Session()
        
        # Use realistic browser headers to avoid 403 errors
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Charset': 'utf-8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        # Disable SSL verification for testing internal sites
        self.session.verify = False
        
        # Additional SSL configuration
        import ssl
        from requests.adapters import HTTPAdapter
        from urllib3.util.ssl_ import create_urllib3_context
        
        # Create a custom SSL context that doesn't verify certificates
        class NoSSLAdapter(HTTPAdapter):
            def init_poolmanager(self, *args, **kwargs):
                context = create_urllib3_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                kwargs['ssl_context'] = context
                return super().init_poolmanager(*args, **kwargs)
        
        # Mount the adapter for HTTPS
        self.session.mount('https://', NoSSLAdapter())
        
        # Suppress SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _setup_logging(self):
        """Setup logging configuration."""
        log_file = self.output_dir / "scraper.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragments while preserving case-sensitive paths."""
        # Remove fragment (anchor)
        url, _ = urldefrag(url)
        # Parse URL to handle case sensitivity properly
        parsed = urlparse(url)
        
        # Only lowercase the scheme and netloc (domain), preserve path case
        normalized_url = f"{parsed.scheme.lower()}://{parsed.netloc.lower()}"
        if parsed.path:
            normalized_url += parsed.path  # Keep original case for path
        if parsed.params:
            normalized_url += f";{parsed.params}"
        if parsed.query:
            normalized_url += f"?{parsed.query}"
        
        return normalized_url.strip()

    def _is_valid_url(self, url: str, base_domain: str, allowed_paths: Optional[List[str]] = None) -> bool:
        """Check if URL is valid for scraping based on domain and path filtering."""
        try:
            parsed = urlparse(url)
            
            # Must have scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Only HTTP/HTTPS
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Domain filtering
            if self.same_domain_only and parsed.netloc != base_domain:
                return False
            
            # Dynamic path filtering
            if allowed_paths:
                # Check if URL path starts with any of the allowed paths
                url_path = parsed.path.rstrip('/')  # Remove trailing slash for consistency
                path_allowed = any(
                    url_path.startswith(allowed_path.rstrip('/')) 
                    for allowed_path in allowed_paths
                )
                if not path_allowed:
                    self.logger.debug(f"URL {url} not in allowed paths: {allowed_paths}")
                    return False
                
            return True
        except Exception:
            return False

    def _can_fetch(self, url: str) -> bool:
        """Check if we can fetch URL according to robots.txt."""
        if not self.respect_robots:
            return True
            
        try:
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            with self.robots_lock:
                if base_url not in self.robots_cache:
                    robots_url = urljoin(base_url, '/robots.txt')
                    try:
                        # Use our session to respect SSL settings
                        response = self.session.get(robots_url, timeout=10)
                        if response.status_code == 200:
                            rp = RobotFileParser()
                            rp.set_url(robots_url)
                            # Set the robots.txt content manually
                            rp.read()
                            self.robots_cache[base_url] = rp
                        else:
                            # If robots.txt not found, allow scraping
                            self.robots_cache[base_url] = None
                    except Exception as e:
                        self.logger.warning(f"Could not read robots.txt for {base_url}: {e}")
                        # If we can't read robots.txt, allow scraping
                        self.robots_cache[base_url] = None
                
                rp = self.robots_cache[base_url]
                if rp is None:
                    return True
                    
                return rp.can_fetch('*', url)
        except Exception as e:
            self.logger.warning(f"Error checking robots.txt for {url}: {e}")
            return True

    def _extract_links(self, html_content: str, base_url: str) -> List[str]:
        """Extract all links from HTML content."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            links = set()
            
            # Extract from <a> tags
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and isinstance(href, str):
                    absolute_url = urljoin(base_url, href)
                    normalized_url = self._normalize_url(absolute_url)
                    if normalized_url:
                        links.add(normalized_url)
            
            # Extract from <link> tags (CSS, etc.)
            for link in soup.find_all('link', href=True):
                href = link.get('href')
                if href and isinstance(href, str):
                    absolute_url = urljoin(base_url, href)
                    normalized_url = self._normalize_url(absolute_url)
                    if normalized_url:
                        links.add(normalized_url)
            
            return list(links)
        except Exception as e:
            self.logger.error(f"Error extracting links from {base_url}: {e}")
            return []

    def _extract_content_text(self, soup: BeautifulSoup) -> str:
        """
        Extract text content using the configured selector with intelligent fallbacks.
        
        Args:
            soup: BeautifulSoup object of the HTML content
            
        Returns:
            Extracted text content
        """
        text_content = ""
        
        try:
            # Try the configured selector first
            if self.content_selector.startswith('#'):
                # ID selector
                element_id = self.content_selector[1:]  # Remove the #
                target_element = soup.find(id=element_id)
            elif self.content_selector.startswith('.'):
                # Class selector
                class_name = self.content_selector[1:]  # Remove the .
                target_element = soup.find(class_=class_name)
            else:
                # Tag selector
                target_element = soup.find(self.content_selector)
            
            if target_element:
                text_content = target_element.get_text(strip=True, separator='\n')
                self.logger.debug(f"Content extracted using selector: {self.content_selector}")
            else:
                # Fallback hierarchy
                fallback_selectors = [
                    ('main', soup.find('main')),
                    ('article', soup.find('article')),
                    ('.content', soup.find('div', class_='content')),
                    ('.main-content', soup.find('div', class_='main-content')),
                    ('#content', soup.find(id='content')),
                    ('body', soup.find('body')),
                ]
                
                for selector_name, fallback_element in fallback_selectors:
                    if fallback_element:
                        text_content = fallback_element.get_text(strip=True, separator='\n')
                        self.logger.debug(f"Content extracted using fallback: {selector_name}")
                        break
                
                # Last resort: get all text
                if not text_content:
                    text_content = soup.get_text(strip=True, separator='\n')
                    self.logger.debug("Content extracted using full page text")
        
        except Exception as e:
            self.logger.warning(f"Error extracting content with selector {self.content_selector}: {e}")
            # Emergency fallback
            text_content = soup.get_text(strip=True, separator='\n')
        
        return text_content

    def _get_content_hash(self, content: str) -> str:
        """Generate fast hash of content for deduplication."""
        # Use xxhash for speed, fallback to hashlib
        try:
            return xxhash.xxh64(content.encode('utf-8')).hexdigest()
        except:
            return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _save_content(self, url: str, content: str, links: List[str]) -> str:
        """Save scraped content to single file (using dynamic content selector)."""
        try:
            # Extract content using dynamic selector
            soup = BeautifulSoup(content, 'html.parser')
            text_content = self._extract_content_text(soup)
            
            # Skip if no meaningful content
            if not text_content or len(text_content.strip()) < 50:
                self.logger.info(f"Skipping {url} - insufficient content")
                return ""
            
            # Append to single output file with URL header
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"URL: {url}\n")
                f.write(f"Scraped: {datetime.now().isoformat()}\n")
                f.write(f"Content Selector: {self.content_selector}\n")
                f.write(f"Links found: {len(links)}\n")
                f.write(f"{'='*80}\n\n")
                f.write(text_content)
                f.write(f"\n\n")
            
            self.logger.info(f"Appended content from: {url}")
            return str(self.output_file)
        except Exception as e:
            self.logger.error(f"Error saving content for {url}: {e}")
            return ""

    def _scrape_single_url(self, url: str, base_domain: str, allowed_paths: Optional[List[str]] = None) -> Tuple[List[str], bool]:
        """
        Scrape a single URL and return found links.
        
        Returns:
            Tuple of (links_found, success_flag)
        """
        try:
            # Rate limiting
            time.sleep(self.delay_between_requests)
            
            # Check if we can fetch this URL
            if not self._can_fetch(url):
                self.logger.info(f"Robots.txt disallows scraping: {url}")
                return [], False
            
            # Make request with retry logic for 403 errors
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Add some jitter to delay to appear more human-like
                    if attempt > 0:
                        import random
                        extra_delay = random.uniform(2, 5)
                        time.sleep(extra_delay)
                        self.logger.info(f"Retry attempt {attempt + 1} for {url} after {extra_delay:.1f}s delay")
                    
                    response = self.session.get(url, timeout=self.timeout)
                    response.raise_for_status()
                    break  # Success, exit retry loop
                    
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 403:
                        self.logger.warning(f"403 Forbidden for {url} (attempt {attempt + 1}/{max_retries})")
                        if attempt == max_retries - 1:
                            self.logger.error(f"All retries failed for {url}: {e}")
                            self.stats["pages_failed"] += 1
                            return [], False
                        continue  # Try again with different headers
                    else:
                        # For other HTTP errors, don't retry
                        raise e
                        
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                self.logger.info(f"Skipping non-HTML content: {url} ({content_type})")
                return [], False
            
            # Handle content encoding and charset properly
            content = self._decode_response_content(response, url)
            
            # Extract content text for hashing using dynamic selector
            soup = BeautifulSoup(content, 'html.parser')
            text_content = self._extract_content_text(soup)
            
            # Check for garbled/binary content
            if self._is_content_garbled(text_content):
                self.logger.warning(f"Detected garbled content for {url}, saving debug info")
                self._save_debug_content(url, response, text_content)
                # Skip this URL as content is corrupted
                return [], False
            
            # Check for duplicate content using extracted text hash
            content_hash = self._get_content_hash(text_content)
            with self.content_lock:
                if content_hash in self.content_hashes:
                    self.stats["pages_skipped_duplicate_content"] += 1
                    self.logger.info(f"Skipping duplicate content: {url}")
                    return [], False
                self.content_hashes.add(content_hash)
            # Extract links
            links = self._extract_links(content, url)
            # Filter valid links
            valid_links = [
                link for link in links 
                if self._is_valid_url(link, base_domain, allowed_paths)
            ]
            
            # Save content
            self._save_content(url, content, valid_links)
            
            self.stats["pages_scraped"] += 1
            self.logger.info(f"Successfully scraped: {url} (found {len(valid_links)} valid links)")
            
            return valid_links, True
            
        except requests.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            self.stats["pages_failed"] += 1
            return [], False
        except Exception as e:
            self.logger.error(f"Unexpected error scraping {url}: {e}")
            self.stats["pages_failed"] += 1
            return [], False

    def scrape(self, start_url: str) -> Dict:
        """
        Main scraping method - starts from a URL and crawls related pages.
        
        Args:
            start_url: The starting URL to begin scraping
            
        Returns:
            Dictionary containing scraping statistics
        """
        self.stats["start_time"] = datetime.now()
        start_url = self._normalize_url(start_url)
        parsed_start = urlparse(start_url)
        base_domain = parsed_start.netloc
        
        # Determine allowed paths - use configured paths or derive from start URL
        if self.allowed_paths:
            allowed_paths = self.allowed_paths
        else:
            # Auto-detect base path from start URL
            base_path = parsed_start.path.rstrip('/')
            # Include the base path and any sub-paths
            allowed_paths = [base_path] if base_path else ["/"]
        
        self.logger.info(f"Starting scrape from: {start_url}")
        self.logger.info(f"Base domain: {base_domain}")
        self.logger.info(f"Allowed paths: {allowed_paths}")
        self.logger.info(f"Max pages: {self.max_pages}")
        self.logger.info(f"Max workers: {self.max_workers}")
        
        # Initialize with start URL
        urls_to_process = {start_url}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while urls_to_process and len(self.visited_urls) < self.max_pages:
                # Submit batch of URLs for processing
                future_to_url = {}
                current_batch = set()
                
                for url in list(urls_to_process):
                    with self.url_lock:
                        if url not in self.visited_urls:
                            self.visited_urls.add(url)
                            current_batch.add(url)
                            future_to_url[executor.submit(self._scrape_single_url, url, base_domain, allowed_paths)] = url
                        else:
                            self.stats["pages_skipped_duplicate_url"] += 1
                
                # Remove processed URLs
                urls_to_process -= current_batch
                
                if not future_to_url:
                    break
                
                # Process completed futures
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        links, success = future.result()
                        if success and links:
                            # Add new URLs to process (filter out already visited)
                            new_urls = set(links) - self.visited_urls
                            urls_to_process.update(new_urls)
                            self.logger.info(f"Added {len(new_urls)} new URLs to queue")
                    except Exception as e:
                        self.logger.error(f"Error processing future for {url}: {e}")
                
                self.logger.info(f"Progress: {len(self.visited_urls)} URLs processed, {len(urls_to_process)} in queue")
        
        self.stats["end_time"] = datetime.now()
        self._log_final_stats()
        return self.stats

    def _log_final_stats(self):
        """Log final scraping statistics."""
        duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
        
        self.logger.info("=" * 50)
        self.logger.info("SCRAPING COMPLETED")
        self.logger.info("=" * 50)
        self.logger.info(f"Total time: {duration:.2f} seconds")
        self.logger.info(f"Pages scraped: {self.stats['pages_scraped']}")
        self.logger.info(f"Pages skipped (duplicate URL): {self.stats['pages_skipped_duplicate_url']}")
        self.logger.info(f"Pages skipped (duplicate content): {self.stats['pages_skipped_duplicate_content']}")
        self.logger.info(f"Pages failed: {self.stats['pages_failed']}")
        self.logger.info(f"Total URLs processed: {len(self.visited_urls)}")
        
        if self.stats['pages_scraped'] > 0:
            avg_time = duration / self.stats['pages_scraped']
            self.logger.info(f"Average time per page: {avg_time:.2f} seconds")

    def _decode_response_content(self, response, url: str) -> str:
        """
        Properly decode response content handling various encodings and compression.
        
        Args:
            response: requests.Response object
            url: URL being processed (for logging)
            
        Returns:
            Decoded content as string
        """
        try:
            # Check content encoding
            content_encoding = response.headers.get('content-encoding', '').lower()
            self.logger.debug(f"Content-Encoding for {url}: {content_encoding}")
            
            # Check charset from Content-Type header
            content_type = response.headers.get('content-type', '')
            charset = 'utf-8'  # Default
            
            if 'charset=' in content_type:
                try:
                    charset = content_type.split('charset=')[1].split(';')[0].strip()
                    self.logger.debug(f"Detected charset for {url}: {charset}")
                except:
                    charset = 'utf-8'
            
            # Handle different compression types explicitly
            if content_encoding in ['br', 'brotli']:
                # Handle Brotli compression
                try:
                    import brotli
                    decompressed = brotli.decompress(response.content)
                    content = decompressed.decode(charset, errors='replace')
                    self.logger.debug(f"Successfully decompressed Brotli content for {url}")
                    return content
                except ImportError:
                    self.logger.warning(f"Brotli compression detected but brotli module not available for {url}")
                    # Fall back to requests.text which might handle it
                    pass
                except Exception as e:
                    self.logger.warning(f"Failed to decompress Brotli content for {url}: {e}")
                    # Fall back to requests.text
                    pass
            
            elif content_encoding in ['gzip', 'deflate']:
                # These should be handled automatically by requests, but check
                self.logger.debug(f"Gzip/deflate compression detected for {url}")
            
            # Let requests handle decompression automatically
            try:
                # This should handle gzip/deflate and sometimes brotli automatically
                content = response.text
                
                # Check if content still looks like binary after requests processing
                if self._looks_like_binary(content):
                    self.logger.warning(f"Content still appears binary after requests.text for {url}")
                    # Try manual decoding of raw content
                    try:
                        content = response.content.decode(charset, errors='replace')
                        self.logger.info(f"Used manual content decoding for {url}")
                    except:
                        content = response.content.decode('utf-8', errors='replace')
                        self.logger.warning(f"Used UTF-8 fallback for {url}")
                
                return content
                
            except UnicodeDecodeError as e:
                self.logger.warning(f"Unicode decode error for {url}: {e}")
                # Try different encodings
                for fallback_charset in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
                    try:
                        content = response.content.decode(fallback_charset, errors='replace')
                        self.logger.info(f"Successfully decoded {url} using {fallback_charset}")
                        return content
                    except:
                        continue
                
                # Last resort: decode with error replacement
                content = response.content.decode('utf-8', errors='replace')
                self.logger.warning(f"Used error replacement for {url}")
                return content
                
        except Exception as e:
            self.logger.error(f"Error decoding content for {url}: {e}")
            # Emergency fallback
            try:
                return response.content.decode('utf-8', errors='replace')
            except:
                return str(response.content)

    def _looks_like_binary(self, content: str) -> bool:
        """Quick check if content looks like binary data."""
        if not content or len(content) < 100:
            return False
        
        # Check first 100 characters for excessive non-printable chars
        non_printable = sum(1 for c in content[:100] if ord(c) < 32 and c not in '\n\r\t\f')
        return non_printable > 10  # More than 10% non-printable

    def _save_debug_content(self, url: str, response, text_content: str) -> None:
        """Save debug information for content encoding issues."""
        try:
            debug_file = self.output_dir / f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(f"Debug Info for: {url}\n")
                f.write(f"{'='*50}\n")
                f.write(f"Status Code: {response.status_code}\n")
                f.write(f"Content-Type: {response.headers.get('content-type', 'N/A')}\n")
                f.write(f"Content-Encoding: {response.headers.get('content-encoding', 'N/A')}\n")
                f.write(f"Content-Length: {response.headers.get('content-length', 'N/A')}\n")
                f.write(f"Transfer-Encoding: {response.headers.get('transfer-encoding', 'N/A')}\n")
                f.write(f"Detected Encoding: {response.encoding}\n")
                f.write(f"Text Content Length: {len(text_content)}\n")
                f.write(f"Binary Content Length: {len(response.content)}\n")
                f.write(f"First 500 chars of text content:\n")
                f.write(f"{repr(text_content[:500])}\n")
                f.write(f"{'='*50}\n")
                
            self.logger.info(f"Debug info saved to: {debug_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving debug info: {e}")

    def _is_content_garbled(self, text_content: str) -> bool:
        """
        Check if content appears to be garbled or binary data.
        
        Args:
            text_content: The extracted text content
            
        Returns:
            True if content appears garbled, False otherwise
        """
        if not text_content or len(text_content.strip()) < 10:
            return False
            
        # Check for null bytes (clear sign of binary data)
        if '\x00' in text_content:
            return True
            
        # Count non-printable characters (excluding common whitespace)
        non_printable_count = 0
        for char in text_content[:1000]:  # Check first 1000 chars
            if ord(char) < 32 and char not in '\n\r\t\f':
                non_printable_count += 1
        
        # If more than 10% of characters are non-printable, likely garbled
        if len(text_content[:1000]) > 0 and (non_printable_count / len(text_content[:1000])) > 0.1:
            return True
            
        # Check for patterns common in compressed/binary data
        garbled_patterns = [
            b'\x1f\x8b',  # gzip magic number
            b'PK\x03\x04',  # zip magic number
            b'\xff\xfe',  # UTF-16 BOM
            b'\xfe\xff',  # UTF-16 BE BOM
        ]
        
        content_bytes = text_content.encode('utf-8', errors='ignore')[:100]
        for pattern in garbled_patterns:
            if pattern in content_bytes:
                return True
                
        return False

def main():
    """Example usage of the WebScraper with dynamic content selector and path filtering."""
    # Example usage with dynamic path filtering
    scraper = WebScraper(
        output_dir="scraped_content",
        content_selector="main",  # CSS selector for content
        allowed_paths=["/flux"],  # Only scrape URLs in this path
        max_workers=5,
        delay_between_requests=1.0,
        max_pages=20,
        same_domain_only=True,
        respect_robots=False,  # Disable robots.txt for internal sites to avoid SSL issues
    )
    
    # Start scraping from a URL
    start_url = "https://fluxcd.io/flux/"  
    
    print(f"Starting web scraper...")
    print(f"Output directory: {scraper.output_dir}")
    print(f"Content selector: {scraper.content_selector}")
    print(f"Allowed paths: {scraper.allowed_paths}")
    
    try:
        stats = scraper.scrape(start_url)
        print("\nScraping completed successfully!")
        print(f"Check the '{scraper.output_dir}' directory for scraped content")
        print(f"Output file: {scraper.output_file}")
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"Error during scraping: {e}")
        

if __name__ == "__main__":
    main()