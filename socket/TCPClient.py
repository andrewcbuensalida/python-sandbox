#!/usr/bin/python3
# have to run TCPServer.py first
import socket


# Create socket object
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host = '192.168.1.104'
host = socket.gethostname()

port = 444

clientsocket.connect((host, port))
while True:
    # Receiving a maximum of 1024 bytes
    message = clientsocket.recv(1024)
    print(message.decode("ascii"))
    user_input = input("What's your message?: ")

    if user_input == "exit":
        clientsocket.close()
        break
    else:
        clientsocket.send(user_input.encode('ascii'))