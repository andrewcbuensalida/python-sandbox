import asyncio
import time

async def fetch_data(id, delay):
    print(f"Fetching data for ID: {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for ID: {id}")
    return f"Data for ID: {id}"

async def main():
    task1 = asyncio.create_task(fetch_data(1, 2))
    task2 = asyncio.create_task(fetch_data(2, 1))

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