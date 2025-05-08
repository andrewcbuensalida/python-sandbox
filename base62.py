import string

BASE62_CHARACTERS = 'abc'

def encode_base62(number):
    if number == 0:
        return BASE62_CHARACTERS[0]
    
    base62_string = ''
    while number > 0:
        remainder = number % 3
        base62_string = BASE62_CHARACTERS[remainder] + base62_string
        number //= 3
    return base62_string

def decode_base62(base62_string):
    number = 0
    for char in base62_string:
        number = number * 3 + BASE62_CHARACTERS.index(char)
    return number

# Example usage
number = 21
encoded_string = encode_base62(number)
print(f"Encoded: {encoded_string}")

decoded_number = decode_base62(encoded_string)
print(f"Decoded: {decoded_number}")