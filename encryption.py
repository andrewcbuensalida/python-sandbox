import base64
import getpass

password = getpass.getpass("Password: ")

print(password)


def encrypt(password: str):
    encrypted = base64.b64encode(password.encode())
    print(encrypted)
    return encrypted


def decode(password: bytes):
    decrypted = base64.b64decode(password)
    print(decrypted.decode())
    return decrypted


encrypted = encrypt(password)

decrypted = decode(encrypted)
