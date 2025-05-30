from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter, sleep


def fetch_image(url):
    sleep(1)  # Simulate a network delay
    return f"Fetched image from {url}"


urls = ["a", "b", "c", "d"]


def main():
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for url in urls:
            future = executor.submit(fetch_image, url)
            futures.append(future)

        for finished_future in as_completed(futures):
            print(finished_future.result())


start_time = perf_counter()
main()
end_time = perf_counter()
print(f"Time elapsed: {end_time-start_time}")
