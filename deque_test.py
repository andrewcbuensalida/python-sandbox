from queue import deque

x:deque = deque(['a','b'])
x.append('c')
y = {
    'first_name':'andrew'
}
x.append(y)
x.remove(y)
class Person:
    def __init__(self,first_name):
        self.first_name = first_name

p = Person('John')
x.append(p)
x.remove(p)
x.remove('b')

print(x)


z = ['a','b']
z.remove('b')
print(z)