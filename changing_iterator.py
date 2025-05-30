# x = ['a','b','c']
# counter = 0

# for item in x:
#     x.append(counter)
#     print(x)
#     print(item)
#     if counter == 5:
#         break
#     counter += 1


# x = ['a','b','c']
# counter = 0

# for item in x:
#     x.pop()

#     print(x)
#     print(item)
#     if counter == 10:
#         break
#     counter += 1


x = set(["a", "b", "c"])
counter = 0

for item in x:
    x.pop()

    print(x)
    print(item)
    if counter == 10:
        break
    counter += 1
