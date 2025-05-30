import asyncio
import time

import httpx


async def fetch_data(client, id):
    """Async function to fetch data using httpx"""
    url = f"https://jsonplaceholder.typicode.com/posts/{id}"
    print(f"Fetching data for ID: {id}")

    response = await client.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()
    print(f"Data fetched for ID: {id}")
    return data


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(fetch_data(client, i)) for i in range(1, 100)]
        results = await asyncio.gather(*tasks)


start_time = time.perf_counter()
asyncio.run(main())
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds")
