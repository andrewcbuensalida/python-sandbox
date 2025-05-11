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
    def process_url(self, url):
        urls = set(u for u in self.htmlParser.getUrls(url) if u.startswith(self.hostname))
        not_visited = urls - self.seen
        for u in not_visited:
            self.submit_to_executor(u)

    def submit_to_executor(self, url):
        self.seen.add(url)
        self.pending.append(self.executor.submit(self.process_url, url))

    def crawl(self, startUrl, htmlParser):
        self.seen = set()
        self.hostname = '/'.join(startUrl.split('/', 3)[:3])
        self.htmlParser = htmlParser
        self.pending = []

        with ThreadPoolExecutor(max_workers=64) as self.executor: # or can do self.executor = ThreadPoolExecutor(max_workers=10) but would have to call self.executor.shutdown() at the end
            self.submit_to_executor(startUrl)
            while self.pending:
                pending_so_far, self.pending = self.pending, []
                for fut in as_completed(pending_so_far):
                    if e := fut.exception():
                        raise RuntimeError("Future failed with an exception") from e

        return self.seen
    
crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = crawler.crawl(startUrl, parser)
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds") # should be around 3 seconds with multithreading. 5 seconds if not using asyncio task.
print(result)