class class_1:
    """class 1 desc"""

    y = "y value"

    def __init__(self, x) -> None:
        self.x = x

    def hello_1(self):
        print("hello 1")

    def __call__(self):
        print("calling class 1")


class class_2(class_1):
    """class 2 desc"""

    def __init__(self, x) -> None:
        super().__init__(x)

    def hello_2(self):
        print("hello 2")

    # def __call__(self):
    #     print("calling class 2")


instance_1 = class_1(100)
instance_1.y
print("""*********Example instance_1.y:\n""", instance_1.y)
# instance_1['y'] # This doesn't work because it needs a __getitem__ method
instance_2 = class_2(200)
print("""*********Example instance_1.x:\n""", instance_1.x)
print("""*********Example instance_2.x:\n""", instance_2.x)


def call_modified():
    print("calling class 2 modified")


# instance_2.__call__ = call_modified
instance_2.__call__ = call_modified
instance_2()
