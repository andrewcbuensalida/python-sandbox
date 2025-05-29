import asyncio
import time
import requests

def sync_fetch_data(id):
    """Synchronous function to fetch data using requests"""
    url = f"https://jsonplaceholder.typicode.com/posts/{id}"
    print(f"Fetching data for ID: {id}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()
    print(f"Data fetched for ID: {id}")
    return data

async def fetch_data(id):
    """Async wrapper that runs the sync function in a thread"""
    return await asyncio.to_thread(sync_fetch_data, id)

async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    print("Tasks created, waiting for results...")

    result1 = await task1
    print("Task 1 completed")
    result2 = await task2
    
    print(result1)
    print(result2)

start_time = time.perf_counter()
asyncio.run(main())
end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time} seconds")