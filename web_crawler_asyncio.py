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
import asyncio
import time
from typing import List 

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
    
    async def crawl_helper(self, stack, visited, htmlParser, domain):
        current_url = stack.pop()
        if current_url not in visited:
            visited.add(current_url)
        else:
            return

        new_urls = await htmlParser.getUrls(current_url)
        
        for new_url in new_urls:
            if new_url not in visited and domain == self.get_domain(new_url):
                stack.append(new_url)

    async def crawl(self, startUrl: str, htmlParser ) -> List[str]:
        stack = [startUrl]
        visited = set([])
        domain = self.get_domain(startUrl)

        while stack:
            print("Stack:", stack)
            async with asyncio.TaskGroup() as tg:
            # this runs per batch of new urls
                for i in range(len(stack)):
                    print(i)
                    tg.create_task(self.crawl_helper(stack, visited, htmlParser, domain))
                print("TaskGroup finished")


        return list(visited)
    
crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = asyncio.run(crawler.crawl(startUrl, parser))
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds") # should be around 3 seconds if using asyncio task. 5 seconds if not using asyncio task.
print(result)