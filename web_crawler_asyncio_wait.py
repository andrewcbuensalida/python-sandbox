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
from concurrent.futures import ThreadPoolExecutor
import asyncio

# news.yahoo.com 1 news.yahoo.com/1 2 news.yahoo.com/100 3                     4 []
#                  news.yahoo.com/2                        news.yahoo.com/200    []

class HtmlParser:
    async def getUrls(self, url: str) -> List[str]:
        await asyncio.sleep(1) # Simulate network delay
        if url == "http://news.yahoo.com":
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/1","http://news.yahoo.com/2"]
        elif url == "http://news.yahoo.com/1":
            await asyncio.sleep(3)
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/10"]
        elif url == "http://news.yahoo.com/2":
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/20"]
        elif url == "http://news.yahoo.com/20":
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/200"]
        elif url == "http://news.yahoo.com/200":
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/2000"]
        elif url == "http://news.yahoo.com/2000":
            # raise Exception('This link is broken') # not catching, even with try except block in helper
            return []
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/20000"]
        else:
            return []


class Solution:
    def get_domain(self,url):
        return url.split('/')[2]
    
    def crawl(self,startUrl,htmlParser):
        return asyncio.run(self.helper(startUrl,htmlParser))
         
    
    async def helper(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        hostname = self.get_domain(startUrl)
        tasks = set()
        visited = set()
        visited.add(startUrl)
        bad_urls = []
        async with asyncio.TaskGroup() as tg:
            startUrl_task = tg.create_task(htmlParser.getUrls(startUrl))
            tasks.add(startUrl_task)

            while tasks:
                done,pending = await asyncio.wait(tasks,return_when="FIRST_COMPLETED")
                tasks = pending
                urls = []

                for finished in done:
                    urls += await finished

                for url in urls:
                    if url not in visited and self.get_domain(url) == hostname:
                        visited.add(url)
                        new_task = tg.create_task(htmlParser.getUrls(url))
                        tasks.add(new_task)

        return list(visited)

    
crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = crawler.crawl(startUrl, parser)
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds") # should be around 4 seconds with multithreading. 7 seconds if not.
print(result)