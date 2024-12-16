# Using the update() method
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

combined_dict = dict1.copy()
combined_dict.update(dict2)
print(combined_dict)  # Output: {'a': 1, 'b': 3, 'c': 4}

# Using the {**dict1, **dict2} syntax
combined_dict = {**dict1, **dict2}
print(combined_dict)  # Output: {'a': 1, 'b': 3, 'c': 4}