class Person:
    def __init__(self,first_name):
        self.first_name = first_name

p = Person('Andrew')
p2 = Person('Buen')
meta = {
    p2:'last'
}

# doesn't work if p is a dict
meta[p] = 'Yes'

print(meta)