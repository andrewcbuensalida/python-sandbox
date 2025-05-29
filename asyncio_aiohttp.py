import asyncio
import time
import aiohttp

async def fetch_data(session, id):
    """Async function to fetch data using aiohttp"""
    url = f"https://jsonplaceholder.typicode.com/posts/{id}"
    print(f"Fetching data for ID: {id}")
    
    async with session.get(url) as response:
        response.raise_for_status()  # Raise an exception for bad status codes
        data = await response.json()
        print(f"Data fetched for ID: {id}")
        return data

async def main():
    async with aiohttp.ClientSession() as session:
        task1 = asyncio.create_task(fetch_data(session, 1))
        task2 = asyncio.create_task(fetch_data(session, 2))

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