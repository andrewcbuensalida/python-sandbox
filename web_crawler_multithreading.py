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
    def get_hostname(self, url):
        return url.split("/")[2]

    def helper(self):
        url = self.pending.pop()
        new_urls = self.getUrls(url)
        for new_url in new_urls:
            if (
                self.get_hostname(new_url) == self.start_hostname
                and new_url not in self.visited
            ):
                self.visited.add(new_url)
                self.pending.append(new_url)

    def crawl(self, startUrl: str, htmlParser: "HtmlParser") -> List[str]:
        self.visited = set([startUrl])
        self.start_hostname = self.get_hostname(startUrl)
        self.getUrls = htmlParser.getUrls
        self.pending = list([startUrl])

        while self.pending:
            threads = [threading.Thread(target=self.helper) for url in self.pending]
            [thread.start() for thread in threads]
            for future in threads:
                future.join()

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
