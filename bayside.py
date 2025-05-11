"""
//Andrew
Implement a RunningAverage class in Python to calculate the running average of integer values added. The class should support concurrent additions and allow retrieval of the current running average using Python's threading features.

Example 1:

```python
ra = RunningAverage()
ra.add(1)
ra.add(2)
ra.add(3)
print(ra.get_average())  # Output: 2.0
```

Output: 2.0
Explanation: The running average after adding 1, 2, and 3 is (1+2+3)/3=2.0.

Example 2:

```python
ra = RunningAverage()
ra.add(5)
ra.add(10)
print(ra.get_average())  # Output: 7.5
ra.add(15)
print(ra.get_average())  # Output: 10.0

Output: 7.5, 10.0
```

Explanation:

After adding 5 and 10, the running average is (5+10)/2=7.5.
After adding 15, it becomes (5+10+15)/3=10.0.

Example 3:

```python
ra = RunningAverage()
print(ra.get_average())  # Output: 0.0
```

Output: 0.0
Explanation: The initial running average is 0.0 before any values are added.
Constraints:

The add method should be thread-safe.
The get_average method should return a float representing the running average.
The class should handle a large number of additions efficiently.
The implementation should leverage Python's threading primitives.
"""

import threading

class RunningAverage:
    def __init__(self):
        self.total = 0
        self.count = 0
        self.lock = threading.Lock()  # Add a lock for thread safety

    def add(self, number):
        with self.lock:  # Ensure thread-safe access to shared resources
            self.total += number
            self.count += 1

    def get_average(self):
        with self.lock:  # Ensure thread-safe access to shared resources
            if self.count == 0:
                return 0.0  # Handle division by zero
            return self.total / self.count

# Test cases with threading
if __name__ == "__main__":
    ra = RunningAverage()

    def add_numbers():
        for i in range(1, 101):
            ra.add(i)
            
    # threads = [threading.Thread(target=add_numbers) for _ in range(5)]
    threads = []
    for i in range(5):
        thread = threading.Thread(target=add_numbers)
        threads.append(thread)

    print('threads:', threads)
    
    for thread in threads:
        thread.start()

    print('threads:', threads)

    for thread in threads:
        thread.join()
    
    print('threads:', threads)

    print(ra.get_average())  # Should output the correct running average after all threads complete