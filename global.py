first_name = "Alice"


class Person:
    first_name = "John Doe"

    def say_hello(self):
        global first_name
        print(f"Hello, my name is {first_name} global!")
        print(f"Hello, my name is {self.first_name}!")


p = Person()
p.say_hello()  # Output: Hello, my name is Alice!

print(p.first_name)  # Output: John Doe
print(Person.first_name)  # Output: John Doe
print(p.__class__.first_name)  # Output: John Doe
