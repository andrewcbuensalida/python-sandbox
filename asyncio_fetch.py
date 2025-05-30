import asyncio
import time

import requests


async def fetch_data(id, delay):
    print(f"Fetching data for ID: {id}")
    # This still blocks
    requests.get(f"https://jsonplaceholder.typicode.com/posts/{id}")
    print(f"Data fetched for ID: {id}")
    return f"Data for ID: {id}"


async def main():
    tasks = [asyncio.create_task(fetch_data(i, 1)) for i in range(1, 100)]
    results = await asyncio.gather(*tasks)


start_time = time.perf_counter()
asyncio.run(main())
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds")
