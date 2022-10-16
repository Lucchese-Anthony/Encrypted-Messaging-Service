import math
import database
import threading
import socket
import os

def main():
    host = ""
    with open('ip.txt', 'r') as file:
        host = file.read().rstrip()
    port = 9001

    client = socket.create_connection(address=(host, port))
    client.sendall(b'Hello, world')
    response = client.recv(1024)
    print('Received', repr(response))
    return

def incomingMessageThread():
    # TODO incoming threads
    return

def outgoingMesssageThread():
    # TODO outgoing threads
    return

def MessageEncryption():
    # TODO Message Encryption
    return

def MessageDecryption():
    # TODO Message Decryption
    return

if __name__ == "__main__":
    main()