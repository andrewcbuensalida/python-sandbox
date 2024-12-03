# def x(**z):
#     print(z)  # {'a': 10,'b':20}


# x(a=10,b=20)
# ================================
# def x(**z):
#     print(z)  # {}


# x()
# ================================
# def x(**z):
#     print(z)  # {'a': 'b}

# x(**{"a": "b"})


# ================================
# def x(*z):
#     print(z)  # ()


# x()
# ================================
# def x(*z):
#     print(z)  # ('a',)


# x('a')
# # ================================
# def x(*z):
#     print(z)  # ('a','b')


# x(*['a','b'])
# # ================================
# def x(*z):
#     print(z)  # ('a',)


# x(*{'a':'b'})
# # ================================
# def x(z):
#     print(z)  # a


# x(*['a'])
# # ================================
# def x(z):
#     print(z)  # a


# x(*{'a':'b'})
# ================================
# def x(z):
#     print(z)  # b


# x(**{'z':'b'})
# ================================
# def x(z,**a):
#     print(z)  # b
#     print(a)  # {}


# x('b')
# ================================
# def x(z,**a):
#     print(z)  # b
#     print(a)  # {'c':'d'}


# x('b',**{'c':'d'})
# # ================================
# def x(z, **a):
#     print(z)  # c
#     print(a)  # {}


# x( *{"c": "d"})
# # ================================
# def x(z, **a):
#     print(z)  # {"c": "d"}
#     print(a)  # {}


# x({"c": "d"})
# ================================
# def x(*z, **a):
#     print(z)  # ({'c': 'd'},)
#     print(a)  # {}


# x({"c": "d"})
# ================================
# def x(*z, **a):
#     print(z)  # ()
#     print(a)  # {'c': 'd'}


# x(**{"c": "d"})
# ================================
# def x(*z, **a):
#     print(z)  # ()
#     print(a)  # {'c': 'd'}


# x(*['b'])
# ================================
# print(*{'a':'b','c':'d'}) # a c
# print('a','c') # a c
# print(*['a','c']) # a c
# ================================
# print("abc\rz")


x = {
    "a": 1,
    "b": 2,
    "c": 3
}

a,b = x
print(a)  # a c