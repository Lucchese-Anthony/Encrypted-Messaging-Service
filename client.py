import math
import struct
import database
import threading
import socket
import os
from objects import message, user
import logging
import sys
import random
import pickle
import time
from equations import *


def main(n, phiOfN, e, d):
    host:str = ""
    with open('ip.txt', 'r') as file:
        host = file.read().rstrip()
    port:int = 30000
    client = None
    try: 
        client:socket = socket.create_connection(address=(host, port))
    except:
        print("Server connection refused")
        sys.exit(1)

    serverAccount:tuple = sendUserInformation(client, n, e)

    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(client,n,e,d))
    sendMessagesThread = threading.Thread(target=sendMessages, args=(client,n,e,d, serverAccount))

    incomingMessagesThread.start()
    sendMessagesThread.start()

    return

def sendMessages(client:socket, server:tuple):
    while(True):
        message = input("")
        encryptedMessage:int = encryptMessage(message, server[0], server[1])
        client.send(struct.pack("B", encryptedMessage))

def sendUserInformation(client:socket, n, e) -> tuple:
    logging.info("Connected to server!")
    username = input("Enter a Username: ")
    password = input("Enter a Password: ")
    newUser = user(username, password, n, e)

    sizeOfSerializedUser = len(pickle.dumps(newUser))
    client.send(struct.pack("B", sizeOfSerializedUser))
    client.send(pickle.dumps(newUser))
    data = client.recv(1024)

    if data.decode("utf-8") == "User is already in the list of users!":
        logging.info("User is already in the list of users!")
        sys.exit(1)
    logging.info("User has been verified!")

    serverKey = client.recv(2048)
    serverExponent = client.recv(2048)
    serverKey = serverKey.decode("utf-8")
    serverExponent = serverExponent.decode("utf-8")
    logging.info("Received server info: " + serverKey + " | " + serverExponent)
    return (serverKey, serverExponent)

def incomingMessages(client:socket):
    while(True):
        encryptedMessage = int(client.recv(2048))
        print("Encrypted Message: " + encryptedMessage)
        decryptedMessage = decryptMessage(encryptedMessage, d, n)
        print("Decrypted Message: " + decryptedMessage)

def closeServer(server):
    endProgram = ''
    
    while endProgram != "e":
        endProgram = input("")
    print('closing server')
    server.close()
    print('ending program')
    sys.exit()

if __name__ == "__main__":
    logging.basicConfig(format='[CLIENT] %(asctime)s - %(message)s',level=logging.INFO)
    p = 0
    q = 0
    with open('p.txt', 'r') as file:
        p = int(file.read().rstrip())
    with open('q.txt', 'r') as file:
        q = int(file.read().rstrip())
    n = p*q
    phiOfN = getPhiOfN(p, q)

    timeToComplete = time.time()
    e = generateE(p, q)
    timeToComplete = time.time() - timeToComplete
    logging.info("time to complete e: " + str(timeToComplete))
    
    timeToComplete = time.time()
    d = findD(e, getPhiOfN(p, q), n)
    timeToComplete = time.time() - timeToComplete
    logging.info("time to complete d: " + str(timeToComplete))
    
    main(n, phiOfN, e, d)