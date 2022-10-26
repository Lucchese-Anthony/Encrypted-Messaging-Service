import math
import database
import threading
import socket
import os
from objects import message, user

def main():
    host = ""
    with open('ip.txt', 'r') as file:
        host = file.read().rstrip()
    port = 30000

    client = socket.create_connection(address=(host, port))
    print("Connected to server!")
    username = input("Enter a Username: ")
    client.send(bytes(username, 'utf-8'))
    password = input("Enter a Password: ")
    client.send(bytes(password, 'utf-8'))

    print("Sent User Information!")
    data = client.recv(1024)
    print("Received message: " + repr(data))
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