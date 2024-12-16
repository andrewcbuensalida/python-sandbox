import json


d = {
    "name": "John",
    "age": 30,
}

s = "hello"
print(json.dumps(d)+s)