import math
import struct
import threading
import socket
import os
from objects import user
import logging
import sys
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
    time.sleep(2)
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(client,n,e,d))
    sendMessagesThread = threading.Thread(target=sendMessages, args=(client,n,e,d, serverAccount))

    incomingMessagesThread.start()
    sendMessagesThread.start()

    return

def sendMessages(client:socket, n:int, e:int, d:int, server:tuple):
    while(True):
        message = input("")
        encryptedMessage:int = encryptMessage(message, server[0], server[1])
        client.send(struct.pack("B", encryptedMessage))

def sendUserInformation(client:socket, n, e) -> tuple:
    logging.info("Connected to server!")
    newUser = user(n, e)
    print(len(str(n)))
    print(str(n) + "\n")
    print(str(math.floor(n / sys.maxsize)) + "\n")
    print(str(n % sys.maxsize) + "\n")

    # send the user object
    sizeOfE = len(str(e))
    client.send(bytes(str(sizeOfE), 'utf-8'))
    client.send(bytes(str(e / sys.maxsize), 'utf-8'))
    sizeOfN = len(str(n / sys.maxsize))
    client.send(bytes(str(sizeOfN), 'utf-8'))
    client.send(bytes(str(n), 'utf-8'))
    # recieve the server's public key
    sizeOfUserE = client.recv(4086)
    print(sizeOfUserE.decode())
    userE = int.from_bytes(client.recv(sizeOfUserE.decode()), byteorder='big') * sys.maxsize
    sizeOfUserN = client.recv(4086)
    logging.info("E: " + str(userE.decode()))
    userN = int.from_bytes(client.recv(sizeOfUserN.decode()), byteorder='big') * sys.maxsize
    logging.info("User information has been recieved!")
    logging.info("User's public key is: " + str(userE))

    return (userN, userE)

def incomingMessages(client:socket,n:int,d:int):
    while(True):
        data = client.recv(2048)
        print("Encrypted message: " + str(data))
        decryptedMessage = decryptMessage(int.from_bytes(data, byteorder='big'), n, d)
        print("Decrypted Message: " + decryptedMessage)

if __name__ == "__main__":
    logging.basicConfig(format='[CLIENT] %(asctime)s - %(message)s',level=logging.INFO)
    p = 0
    q = 0
    with open('pClient.txt', 'r') as file:
        p = int(file.read().rstrip())
    with open('qClient.txt', 'r') as file:
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