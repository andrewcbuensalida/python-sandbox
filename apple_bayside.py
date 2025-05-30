class TinyUrl:
    counter = 0
    to_fullUrl = {}
    to_shortUrl = {}
    base_url = "http://tinyurl.com/"
    access_count = {}

    def get_short_url(self, fullUrl: str) -> str:
        if fullUrl in self.to_shortUrl:
            return self.to_shortUrl[fullUrl]

        suffix = self.counter
        shortUrl = self.base_url + str(suffix)
        self.counter += 1
        self.to_shortUrl[fullUrl] = shortUrl
        self.to_fullUrl[shortUrl] = fullUrl
        return shortUrl

    def resolve_url(self, shortUrl: str) -> str:
        try:
            if shortUrl in self.access_count:
                self.access_count[shortUrl] += 1
            else:
                self.access_count[shortUrl] = 1
            return self.to_fullUrl[shortUrl]
        except Exception as e:
            return "There was an error"

    def get_stats(self) -> list[str]:
        """
        returns top 10 most accessed shortUrls
        """
        urls = []
        for url, count in self.access_count.items():
            print(url, count)
            urls.append([url, count])
        urls.sort(key=lambda url: url[1])
        just_urls = list(map(lambda url: url[0], urls))
        top_urls = just_urls[-10:]
        print("top_urls", top_urls)
        return top_urls

        # alternatively, this is more pythonic
        sorted_urls = sorted(
            self.access_count.items(), key=lambda item: item[1], reverse=True
        )
        top_urls = [url for url, _ in sorted_urls[:10]]
        return top_urls

    def get_url_stats(self, short_url: str) -> float:
        return self.access_count[short_url]


t = TinyUrl()
print(t.get_short_url("http://google.com"))  # http://tinyurl.com/0
print(t.get_short_url("http://a.com"))  # http://tinyurl.com/0
print(t.resolve_url("http://tinyurl.com/0"))  # http://google.com
print(t.resolve_url("http://tinyurl.com/0"))  # http://google.com
print(t.resolve_url("http://a.com"))  # http://google.com
print(t.access_count)
print("print", t.get_stats())
print(t.get_url_stats("http://tinyurl.com/0"))
# randomizing can have collisions
# base 62 instead of base10 to save space
# cassandra for read heavy, dynamodb write heavy
# hot partitions, popular short urls, store it in redis in-memory 20% - 80%
# redirect with 301 permanent, 304 temporary
