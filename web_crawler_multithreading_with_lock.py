# """
# This is HtmlParser's API interface.
# You should not implement it, or speculate about its implementation
# """
# class HtmlParser(object):
#    def getUrls(self, url):
#        """
#        :type url: str
#        :rtype List[str]
#        """
import threading
import time
from typing import List


class HtmlParser:
    def getUrls(self, url: str) -> List[str]:
        time.sleep(1)  # Simulate network delay
        if url == "http://news.yahoo.com":
            return [
                "http://news.yahoo.com",
                "http://news.google.com",
                "http://news.yahoo.com/1",
                "http://news.yahoo.com/2",
            ]
        elif url == "http://news.yahoo.com/1":
            return [
                "http://news.yahoo.com",
                "http://news.google.com",
                "http://news.yahoo.com/100",
            ]
        elif url == "http://news.yahoo.com/2":
            return [
                "http://news.yahoo.com",
                "http://news.google.com",
                "http://news.yahoo.com/200",
            ]
        else:
            return []


class Solution:
    lock = threading.Lock()
    stack = []
    visited = set([])
    domain = ""

    def get_domain(self, url):
        return url.split("/")[2]

    def crawl_helper(self, htmlParser):
        with self.lock:
            current_url = self.stack.pop()
            if current_url not in self.visited:
                # if current_url not in self.visited:
                self.visited.add(current_url)
            else:
                return

        # if there's a with self.lock here, it takes longer
        new_urls = htmlParser.getUrls(current_url)

        with self.lock:
            for new_url in new_urls:
                if new_url not in self.visited and self.domain == self.get_domain(
                    new_url
                ):
                    self.stack.append(new_url)

    def crawl(self, startUrl: str, htmlParser) -> List[str]:
        self.stack.append(startUrl)
        self.domain = self.get_domain(startUrl)
        self.visited = set([])
        while self.stack:
            threads: list[threading.Thread] = []
            for _ in range(len(self.stack)):
                thread = threading.Thread(target=self.crawl_helper, args=(htmlParser,))
                threads.append(thread)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

        return list(self.visited)


crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = crawler.crawl(startUrl, parser)
end_time = time.perf_counter()
print(
    f"Execution time: {end_time - start_time} seconds"
)  # should be around 3 seconds with multithreading. 5 seconds if not using asyncio task.
print(result)
