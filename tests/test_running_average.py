import unittest
from bayside import RunningAverage

class TestRunningAverage(unittest.TestCase):

    def test_initial_average(self):
        ra = RunningAverage()
        self.assertEqual(ra.get_average(), 0.0, "Initial average should be 0.0")

    def test_single_addition(self):
        ra = RunningAverage()
        ra.add(10)
        self.assertEqual(ra.get_average(), 10.0, "Average after adding 10 should be 10.0")

    def test_multiple_additions(self):
        ra = RunningAverage()
        ra.add(10)
        ra.add(20)
        ra.add(30)
        self.assertEqual(ra.get_average(), 20.0, "Average after adding 10, 20, 30 should be 20.0")

    def test_thread_safety(self):
        import threading

        ra = RunningAverage()

        def add_numbers():
            for i in range(1, 101):
                ra.add(i)

        threads = [threading.Thread(target=add_numbers) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        expected_average = sum(range(1, 101)) / 100 
        print(expected_average) # Average of numbers 1 to 100
        self.assertAlmostEqual(ra.get_average(), expected_average, places=5, 
                               msg="Thread-safe average calculation failed")

if __name__ == "__main__":
    unittest.main()