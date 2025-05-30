class Placeholder:
    def __init__(self, value):
        self.value = value


p = Placeholder("hello")
x = "hello"
y = x * 3
print(y)  # Output: hellohellohello
# print(p * 3)  # Output: unsupported operand type(s) for *: 'Placeholder' and 'int'

z = ["bye"]
a = z * 3
print(a)  # Output: [100, 100, 100]
b = ", ".join(a)
print(b)  # Output: 100, 100, 100
