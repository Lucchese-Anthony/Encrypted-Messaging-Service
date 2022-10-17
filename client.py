import math
import database
import threading
import socket
import os

def main():
    host = ""
    with open('ip.txt', 'r') as file:
        host = file.read().rstrip()
    port = 1022

    client = socket.create_connection(address=(host, port))
    client.send(b'User Information')
    response = client.recv(2048)
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