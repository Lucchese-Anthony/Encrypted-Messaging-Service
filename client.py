import math
import database
import threading
import socket
import os

def main():
    host = "127.0.0.1"
    port = 9001

    client = socket.create_connection(address=(host, port))
    client.sendall(b'Hello, world')
    response = client.recv(1024)
    print('Received', repr(response))
    return

if __name__ == "__main__":
    main()