l1 = []
index = 4
if index >= len(l1):
    l1.extend([None] * (index + 1 - len(l1)))

l1[index] = 100

print(l1)
