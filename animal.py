class Animal:
    def __init__(self, animal_type) -> None:
        self.animal_type = animal_type

    def eat(self):
        print(f"The {self.animal_type} is eating")


class Dog(Animal):
    def __init__(self) -> None:
        super().__init__("dog")

    def walk(self):
        print("dog walking")


class Cat(Animal):
    def walk(self):
        print("cat walking")


dog1 = Dog()
dog1.walk()
dog1.eat()
