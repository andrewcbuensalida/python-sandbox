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
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

# news.yahoo.com 1 news.yahoo.com/1 2 news.yahoo.com/100 3                     4 []
#                  news.yahoo.com/2                        news.yahoo.com/200    []


class HtmlParser:
    def getUrls(self, url: str) -> List[str]:
        time.sleep(1)  # Simulate network delay
        result = {"url": url}
        try:
            if url == "http://news.yahoo.com":
                result["urls"] = [
                    "http://news.yahoo.com",
                    "http://news.google.com",
                    "http://news.yahoo.com/1",
                    "http://news.yahoo.com/2",
                ]
            elif url == "http://news.yahoo.com/1":
                time.sleep(3)
                result["urls"] = [
                    "http://news.yahoo.com",
                    "http://news.google.com",
                    "http://news.yahoo.com/100",
                ]
            elif url == "http://news.yahoo.com/100":
                # time.sleep(1) # Simulate network delay
                raise Exception(f"This is an exception in url {url}")
            elif url == "http://news.yahoo.com/2":
                # time.sleep(1) # Simulate network delay
                result["urls"] = [
                    "http://news.yahoo.com",
                    "http://news.google.com",
                    "http://news.yahoo.com/200",
                ]
            elif url == "http://news.yahoo.com/200":
                result["urls"] = [
                    "http://news.yahoo.com",
                    "http://news.google.com",
                    "http://news.yahoo.com/2000",
                ]
            elif url == "http://news.yahoo.com/2000":
                result["urls"] = [
                    "http://news.yahoo.com",
                    "http://news.google.com",
                    "http://news.yahoo.com/20000",
                ]
            elif url == "http://news.yahoo.com/200000":
                result["urls"] = [
                    "http://news.yahoo.com",
                    "http://news.google.com",
                    "http://news.yahoo.com/2000000",
                ]
            else:
                result["urls"] = []  # 7 seconds for 2 route.
        except Exception as e:
            result["error"] = e

        return result


class Solution:
    def get_domain(self, url):
        return url.split("/")[2]

    def crawl(self, startUrl: str, htmlParser: "HtmlParser") -> List[str]:
        hostname = self.get_domain(startUrl)
        futures = []
        visited = set()
        visited.add(startUrl)
        bad_urls = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures.append(executor.submit(htmlParser.getUrls, startUrl))
            while futures:
                print("in while", futures)
                for future in as_completed(
                    futures
                ):  # whenever a future is finished, it will loop, future being the one that is finished
                    print(future)
                    # futures = filter(lambda future_in_stack:future_in_stack is not future,futures)
                    futures = [
                        future
                        for future_in_stack in futures
                        if future_in_stack is not future
                    ]
                    result = future.result()
                    if result.get("error"):
                        bad_urls.append(result.get("url"))
                        continue
                    else:
                        urls = result.get("urls")
                    for url in urls:
                        if url not in visited and self.get_domain(url) == hostname:
                            visited.add(url)
                            futures.append(executor.submit(htmlParser.getUrls, url))
                    break
        print(bad_urls)
        for bad_url in bad_urls:
            visited.discard(bad_url)
        return list(visited)


crawler = Solution()
startUrl = "http://news.yahoo.com"
parser = HtmlParser()
start_time = time.perf_counter()
result = crawler.crawl(startUrl, parser)
end_time = time.perf_counter()
print(
    f"Execution time: {end_time - start_time} seconds"
)  # should be around 4 seconds with multithreading. 7 seconds if not.
print(result)
