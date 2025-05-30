class Exam:

    def __init__(self, code, year):
        self.code = code
        self.year = year
        self._score = None
        self.__grade = 100

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        print("""*********Example value:\n""", value)
        if not 0 <= value <= 100:
            raise ValueError("Invalid exam score")
        self._score = value


e = Exam("CSC102", 2019)
# print(e.__grade) # AttributeError: 'Exam' object has no attribute '__grade'
e.score = 90
print(e.score)


if 0 < 1 < 2 < 3:
    print("True")
else:
    print("False")
