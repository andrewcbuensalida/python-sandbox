class LStr:
    def __init__(self, s):
        self.s = s
        self.index = -1

    def __eq__(self, other):
        return self.s.lower() == other.lower()

    def __next__(self):
        self.index += 1
        if self.index >= len(self.s):
            raise StopIteration
        return self.s[self.index]

    def __iter__(self):
        return self


x = LStr("Python")

for i in x:
    print(i)
