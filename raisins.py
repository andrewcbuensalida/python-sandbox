class TooManyRaisinsError(Exception):
    pass


try:
    # TooManyRaisinsError = Exception # could also do this instead of class
    raise TooManyRaisinsError("Too many raisins")
except Exception as e:
    print("In Error")
    print(e)