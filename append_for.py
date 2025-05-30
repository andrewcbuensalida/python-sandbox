string1 = ["a", "b", "c"]
counter = 0

# for i in range(len(string1)): range doesn't change when appending
for c in string1:  # string1 changes when appending
    print(string1)
    print(c)
    string1.append(str(counter))
    string1[counter] = str(counter)
    counter += 1
    if counter > 20:
        break
