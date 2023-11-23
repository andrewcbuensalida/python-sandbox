from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

visited_urls = set()


def spider(url, keyword):
    if url in visited_urls or len(visited_urls) > 5:
        return

    try:
        print(url)
        with open('urls.txt', 'w') as file:
            file.write(url + '\n')
        # Alternatively
        # f = open("urls.txt", "a")
        # f.write(url + '\n')
        # f.close()
        response = requests.get(url)
    except:
        print(f"URL {url} is not valid. ")
        return

    if response.status_code == 200:
        visited_urls.add(url)
        soup = BeautifulSoup(response.content, "html.parser")
        a_tags = soup.find_all("a")
        new_urls = []
        for tag in a_tags:
            href = tag.get("href")
            if href is not None and href != "":
                new_urls.append(href)

        for new_url in new_urls:
            base_and_new_url = urljoin(url, new_url)
            if keyword in base_and_new_url:
                spider(base_and_new_url, keyword)


url = input("What url would you like to crawl?: ")
# https://en.wikipedia.org/wiki/Xenotransplantation
# https://yahoo.com
keyword = input("What is the keyword?: ")
spider(url, keyword)

# print(f"Example visited_urls: ")
# print(visited_urls)

# example usage of urljoin. Basically takes the base part of the first aargument and adds the second argument to it.
# print(
#     urljoin("https://en.wikipedia.org/wiki/Xenotransplantation", "/something")
# )  # https://en.wikipedia.org/something
