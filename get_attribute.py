def test_get(self):
    print('in test_get')
    return self["name"]

def test_getitem(self, key):
    print('in test_getitem')
    return self[key]


test = {
    "name":"andrew",
    # "get": test_get,
    "__getattr__": test_getitem
}

# print(test["name"]) # andrew
print(test["name"]) # andrew

test_getitem.name