from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep, perf_counter

def fetch_image(url):
    sleep(1)  # Simulate a network delay
    return f"Fetched image from {url}"


urls = ['a','b','c','d']

def main():
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(fetch_image,urls)
        for result in results:
            print(result)


start_time = perf_counter()
main()
end_time = perf_counter()
print(f'Time elapsed: {end_time-start_time}')