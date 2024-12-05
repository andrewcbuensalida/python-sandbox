x = {
    "a": 1,
}

class test1:
    def __init__(self,a):
        self.a = a

print(x['a'])
# print(x['b']) # KeyError: 'b'
print(x.get('b')) # None


t1 = test1(1)

# print(t1['a']) # TypeError: 'test1' object is not subscriptable
# print(t1.get('a')) # AttributeError: 'test1' object has no attribute 'get'
print(t1.a) # 1