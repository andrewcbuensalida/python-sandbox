# Need to run this file with
#   type words.txt | python fuzzer.py
# type is the command prompt version of cat in linux

import sys

import requests  # Don't name this file requests.py or else will get this error: AttributeError: partially initialized module 'requests' has no attribute 'get' (most likely due to a circular import)

print("start")

# This is <_io.TextIOWrapper name='<stdin>' mode='r' encoding='cp1252'>
# print(sys.stdin)

for word in sys.stdin:
    print("\n==============This is word: " + word)
    try:
        response = requests.get(url=f"https://swapi.dev/api/{word}")
        print("This is response")
        print(response)  # <Response [200]>
        if response.ok:
            print("This is response.json() ")
            print(response.json())
        else:
            print("In else")
            raise TypeError("Sorry!!")  # This Sorry!! is useless
    except TypeError:
        print("In TypeError")
