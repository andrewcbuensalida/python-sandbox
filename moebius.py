# def init_data(data=[]):
#     """Create a list containing the value 5."""
#     id(data)
#     print('''*********Example id(data):\n''', id(data))
#     data.append(5)
#     return data

# x = init_data()
# y = init_data()
# print(x,y)


# ## Question 4
# values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# if any([value % 2 for value in values]):
#     print('done')

# # or

# if any(False for value in values):
#     print('done')


## Question 5

# What is the equivalent of the following code without using decorator
# syntax? Does order matter when decorating a function multiple times?

# @bp.route('/info')
# @login_required
# def user_info():
#     return jsonify(current_user)

# Equivalent code without using decorator syntax
# def user_info():
#   return jsonify(current_user)

# user_info = login_required(user_info)
# user_info = bp.route('/info')(user_info)

# # Yes, the order matters when decorating a function multiple times.
# # The decorators are applied from the bottom up. In this case, `login_required`
# # is applied first, then `bp.route('/info')`.

# # MY Answer:
# class bp_class:
#     def route(self,args):
#         def login_required(func):
#             print('in login_required')
#             return func()
#         print(args)
#         return login_required

# def user_info():
#     print('hello')

# bp = bp_class()
# bp.route('/info')(user_info)


# another answer
# class bp_class:
#     def route(self,args):
#         def inner(func):
#             def wrapper():
#                 func()
#             return wrapper
#         return inner

# def login_required(func):
#     def wrapper():
#         return func()
#     return wrapper

# bp = bp_class()
# @bp.route('/info')
# def user_info():
#     print('in user_info')

# user_info()


# def my_decorator(args):
#   def inner(func):
#         def wrapper():
#             print("Something is happening before the function is called.")
#             print(args)
#             func()
#             print("Something is happening after the function is called.")
#         return wrapper
#   return inner

# def login_required(func):
#     def wrapper():
#         print('in login_required wrapper before')
#         func()
#         print('in login_required wrapper after')
#     return wrapper

# @my_decorator('abc')
# @login_required
# def say_whee():
#     print("Whee!")


# say_whee()


## Question 6

# A list contains instances of the following class. Write a function that
# will produce a sorted list ordered first by name descending, then id
# ascending.

# class User:
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name

# def sort_name_desc_id_asc(users:list[User]):
#     return sorted(users, key=lambda x: (-ord(x.name[0]), x.id))
#     # users.sort(key=lambda x: (-ord(x.name[0]), x.id))

# users = [User(1,'a'), User(4,'c'), User(2,'a'), User(3,'b')]
# sorted_users = sort_name_desc_id_asc(users)

# for user in sorted_users:
# # for user in users:
#     print(user.id, user.name)


## Bonus

# What does the following output, and why?

x = [1, 2, 3, 4]

for x[-1] in x:
    print(x)
