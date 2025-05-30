#!/usr/bin/python3
import socket

print("starting....")
# Creating the socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()  # Host is the server IP
port = 444  # Port to listen on

# Binding to socket
serversocket.bind(
    (host, port)
)  # Host will be replaced/substitued with IP, if changed and not running on host

# Starting TCP listener
serversocket.listen(3)

clientsocket, address = serversocket.accept()  # This is blocking
print("received connection from %s" % str(address))
message = "hello! Thank you for connecting to the server" + "\r\n"

clientsocket.send(message.encode("ascii"))
while True:
    #     # Starting the connection

    # Message sent to client after successful connection
    client_message = clientsocket.recv(1024).decode("ascii")
    print("*********Example client_message: ", client_message)
    clientsocket.send("".join(["Your message is this", client_message]).encode("ascii"))
    if client_message == "exit":
        clientsocket.close()
