ages = {
    "age1": "100",
    "age2": "10",
    "age3": "b",
    "age4": "1",
    "age5": "a",
}

ages_list = list(ages.items())
print(ages_list)
ages_list.sort(key=lambda age: age[1])
print(ages_list)
new_dict = dict(ages_list)
print(new_dict)


print("a" < "b")
# print('a'<1) error

print(sorted(new_dict.items(), key=lambda age: age[0], reverse=True))
print(new_dict)
