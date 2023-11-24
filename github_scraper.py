from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Don't need to plug this in webdriver.Chrome() because I have a new version of selenium.
# chrome_driver_path = "C:\\swe\\code\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"


# TODO this only gets from the first page
def get_repos(gh_account_url):
    driver = webdriver.Chrome()
    driver.get(gh_account_url)  # for prod
    elements = driver.find_elements(
        By.CSS_SELECTOR, "a[itemprop='name codeRepository']"
    )
    # Note: can't get_attribute after driver.quit()
    repo_urls = list(map(lambda element: element.get_attribute("href"), elements))
    driver.quit()
    return repo_urls


def find_urls_with_passwords_in_repo(repo_url):
    urls_with_passwords = []
    visited_urls = []
    driver = webdriver.Chrome()
    urls_to_visit = [repo_url]
    while len(urls_to_visit) != 0:
        current_url = urls_to_visit.pop()
        if current_url in visited_urls:
            continue
        driver.get(current_url)
        visited_urls.append(current_url)

        body = driver.find_element(By.TAG_NAME, "body")
        body_inner_html = body.get_attribute("innerHTML") or ""

        if "password" in body_inner_html:
            # if "password" in body_inner_html:
            print("in if age")
            urls_with_passwords.append(current_url)

        anchor_elements = driver.find_elements(
            By.CSS_SELECTOR, ".Link--primary"
        )  # TODO if this changes, it might break. Better to select all anchor tags instead.


        anchor_urls = []
        for element in anchor_elements:
            try:
                # Thie errors with stale element not found when scraping https://github.com/googleapis/google-auth-library-python when it reaches https://github.com/googleapis/google-auth-library-python/tree/main/tests/transport or other urls, it seems to change each time.
                url = element.get_attribute("href")
                anchor_urls.append(url)
            except:
                print("********could not find element")

        non_empty_anchor_urls = list(
            filter(
                lambda url: url is not None and url != "" and url != False, anchor_urls
            )
        )
        new_anchor_urls = list(
            filter(lambda url: url not in visited_urls, non_empty_anchor_urls)
        )

        file_urls = list(filter(lambda url: repo_url + "/blob" in url, new_anchor_urls))

        folder_urls = list(
            filter(lambda url: repo_url + "/tree" in url, new_anchor_urls)
        )
        urls_to_visit += file_urls + folder_urls
        # urls_to_visit.extend(file_urls + folder_urls)  # Alternatively

    driver.quit()
    return urls_with_passwords


gh_account_url = input("What github account would you like to scan for repos?")
# https://github.com/googleapis

while True:
    urls_with_passwords = []

    repo_urls = get_repos(gh_account_url) # for prod
    # repo_urls = get_repos("https://github.com/googleapis")  # for faster development
    # repo_urls = [
    #     "https://github.com/googleapis/google-auth-library-python"  
    #     # "https://github.com/andrewcbuensalida/scraper_test" # This works
    # ]  # for fastest development

    for repo_url in repo_urls:
        urls_with_passwords += find_urls_with_passwords_in_repo(repo_url)

    print("Example urls_with_passwords: ")
    print(urls_with_passwords)
    print(len(urls_with_passwords))

    print("Sleeping.......")
    time.sleep(60 * 60 * 24)  # a day is 60*60*24
