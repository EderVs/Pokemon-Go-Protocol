"""
    Pokemon Go Protocol Client
"""

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = str(input("Server hostname or ip? "))
port = int(input("Server port? "))
sock.connect((host, port))
while True:
    data = str(input("Message: ")).encode('utf-8')
    sock.send(data)
    print("Response: ", sock.recv(1024))
