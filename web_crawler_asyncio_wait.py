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
            # raise Exception('This link is broken') # not catching, even with try except block in helper
            return []
            return ["http://news.yahoo.com", "http://news.google.com","http://news.yahoo.com/20000"]
        else:
            return []


class Solution:
    def get_hostname(self,url):
        return url.split('/')[2]

    def crawl(self,startUrl,htmlParser):
        return asyncio.run(self.crawl_helper(startUrl,htmlParser))

    async def crawl_helper(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        visited = set([startUrl])
        startUrl_hostname = self.get_hostname(startUrl)

        async with asyncio.TaskGroup() as tg:
            startUrl_future = tg.create_task(asyncio.to_thread(htmlParser.getUrls,startUrl))
            futures = set([startUrl_future])

            while futures:
                done,futures = await asyncio.wait(futures,return_when='FIRST_COMPLETED')
                new_urls = await done.pop()
                    
                for new_url in new_urls:
                    if startUrl_hostname == self.get_hostname(new_url) and new_url not in visited:
                        visited.add(new_url)
                        new_future = tg.create_task(asyncio.to_thread(htmlParser.getUrls,new_url))
                        futures.add(new_future)

                
        return list(visited)

    
crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = crawler.crawl(startUrl, parser)
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds") # should be around 4 seconds with multithreading. 7 seconds if not.
print(result)