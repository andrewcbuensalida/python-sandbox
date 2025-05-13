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
from threading import Lock

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
            # raise Exception('This link is broken',url) # not catching, even with try except block in helper
            return []
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/20000"]
        else:
            return []


class Solution:
    lock = Lock()
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        visited = set()
        initialHostname = startUrl.split("/")[2]


        with ThreadPoolExecutor(20) as executor:
            def _dfs(url):
                with self.lock:
                    visited.add(url)
                    for nextUrl in htmlParser.getUrls(url):
                        if nextUrl.split("/")[2] == initialHostname and nextUrl not in visited:
                            executor.submit(_dfs, nextUrl)
            
            _dfs(startUrl)
        return list(visited)
    
crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = crawler.crawl(startUrl, parser)
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds") # should be around 3 seconds with multithreading. 5 seconds if not using asyncio task.
print(result)