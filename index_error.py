test = ["a", "b", "c"]

try:
    print(test[3])
except Exception as e:
    print("That index does not exist!")
    print(e)
