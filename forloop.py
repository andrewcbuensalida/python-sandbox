a = ['b','c','d','e','f','g','h']
for letter in range(len(a)):
    print(a[letter] + ' is at index ' + str(letter) + ' in the list a')


for i, l in enumerate(a):
    print(l + ' is at index ' + str(i) + ' in the list a')