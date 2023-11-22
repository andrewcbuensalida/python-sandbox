# Need to run this file with
#   type words.txt | python fuzzer.py
# type is the command prompt version of cat in linux

import requests  # Don't name this file requests.py or else will get this error: AttributeError: partially initialized module 'requests' has no attribute 'get' (most likely due to a circular import)
import sys

print("start")

# This is <_io.TextIOWrapper name='<stdin>' mode='r' encoding='cp1252'>
print(sys.stdin)

for word in sys.stdin:
    print("This is word: " + word)
# response = requests.get(url="https://swapi.dev/api/people/40")

# print(response.json())
