x: list[str] = ["a", "b", "c"]
z = (
    y for y in x if y != "a"
)  # looks like a list comprehension but it's a generator expression. This produces a generator object
for c in z:
    print(c)


g = (y for y in x if y != "a")
# or can use next
print(next(g))
print(next(g))
# print(next(g))  # This will error StopIteration because there's no more value to iterate


h = [y for y in x if y != "a"]  # this is a list comprehension
print(h)


i = next(y for y in x if y != "a")  # can do next straight away
print(i)


j = "k".join(
    y for y in x if y != "a"
)  # can use join on a generator which will act like a list
print(j)
