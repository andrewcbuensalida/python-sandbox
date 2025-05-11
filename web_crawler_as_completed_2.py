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
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/100"]
        elif url == "http://news.yahoo.com/100":
            time.sleep(1) # Simulate network delay
            return []
        elif url == "http://news.yahoo.com/2":
            time.sleep(1) # Simulate network delay
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/200"]
        else:
            return []


class Solution:
    def get_domain(self,url):
        return url.split('/')[2]
    
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        hostname = self.get_domain(startUrl)
        tasks = []
        visited = set()
        visited.add(startUrl)
        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks.append(executor.submit(htmlParser.getUrls, startUrl))
            while tasks:
                new_tasks = []
                for future in as_completed(tasks):
                    urls = future.result()
                    for url in urls:
                        if url not in visited and self.get_domain(url) == hostname:
                            visited.add(url)
                            new_tasks.append(executor.submit(htmlParser.getUrls, url))
                tasks = new_tasks
        return list(visited)

    
crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = crawler.crawl(startUrl, parser)
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds") # should be around 4 seconds with multithreading. 7 seconds if not.
print(result)