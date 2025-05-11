# """
# This is HtmlParser's API interface.
# You should not implement it, or speculate about its implementation
# """
#class HtmlParser(object):
#    def getUrls(self, url):
#        """
#        :type url: str
#        :rtype List[str]
#        """
import time
from typing import List 
from concurrent.futures import ThreadPoolExecutor, as_completed

# news.yahoo.com 1 news.yahoo.com/1 2 news.yahoo.com/100 3                     4 []
#                  news.yahoo.com/2                        news.yahoo.com/200    []

class HtmlParser:
    def getUrls(self, url: str) -> List[str]:
        time.sleep(1) # Simulate network delay
        if url == "http://news.yahoo.com":
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/1","http://news.yahoo.com/2"]
        elif url == "http://news.yahoo.com/1":
            time.sleep(3)
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/10"]
        elif url == "http://news.yahoo.com/2":
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/20"]
        elif url == "http://news.yahoo.com/20":
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/200"]
        elif url == "http://news.yahoo.com/200":
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/2000"]
        elif url == "http://news.yahoo.com/2000":
            raise Exception('This link is broken')
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/20000"]
        else:
            return []


class Solution:
    def get_domain(self,url):
        return url.split('/')[2]
    
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        hostname = self.get_domain(startUrl)
        futures = set()
        visited = set()
        visited.add(startUrl)
        future_to_url = {}
        bad_urls = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            startUrl_future = executor.submit(htmlParser.getUrls, startUrl)
            futures.add(startUrl_future)
            future_to_url[startUrl_future] = startUrl
            while futures:
                for future in as_completed(futures): # whenever a future is finished, it will loop, future being the one that is finished
                    # remove the future that just finished
                    futures.discard(future)
                    try:
                        urls = future.result()
                    except Exception as e:
                        bad_urls.append(future_to_url[future])
                        continue
                    for url in urls:
                        if url not in visited and self.get_domain(url) == hostname:
                            visited.add(url)
                            new_future = executor.submit(htmlParser.getUrls, url)
                            futures.add(new_future)
                            future_to_url[new_future] = url
                    break
        print(bad_urls)
        return list(visited)

    
crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = crawler.crawl(startUrl, parser)
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds") # should be around 4 seconds with multithreading. 7 seconds if not.
print(result)