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

maxsize = 2147483647

def main(n, phiOfN, e, d):
    host:str = ""
    with open('ip.txt', 'r') as file:
        host = file.read().rstrip()
    port:int = 2049
    client = None
    try: 
        client:socket = socket.create_connection(address=(host, port))
    except:
        print("Server connection refused")
        sys.exit(1)
    time.sleep(.5)
    serverAccount:tuple = sendUserInformation(client, n, e)
    time.sleep(2)
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(client,n,d))
    sendMessagesThread = threading.Thread(target=sendMessages, args=(client,n,e,d, serverAccount))

    incomingMessagesThread.start()
    sendMessagesThread.start()

    return

def sendMessages(client:socket, n:int, e:int, d:int, server:tuple):
    while(True):
        message = input("Enter a message:")
        encryptedMessage:int = encryptMessage(message.upper(), server[1], server[0])
        logging.info("Message: " + message)
        logging.info("Encrypted Message: "+ str(encryptedMessage))
        div = math.floor(encryptedMessage / maxsize)
        print(div)
        print(str(len(str(div))))
        mod = encryptedMessage % maxsize
        print(mod)
        print(maxsize > div)
        client.send(bytes(str(len(str(div))), 'utf-8'))
        time.sleep(.3)
        client.send(bytes(str(div),'utf-8'))
        time.sleep(.3)
        client.send(bytes(str(len(str(mod))), 'utf-8'))
        time.sleep(.3)
        client.send(bytes(str(mod),'utf-8'))

def sendUserInformation(connection:socket, n, e) -> tuple:
    logging.info("Connected to server!")
    newUser = user(n, e)
    # send the user object
    shrinkE = shrinkIntToSendOverSocket(e)
    shrinkN = shrinkIntToSendOverSocket(n)
    time.sleep(.3)
    connection.send(bytes(str(len(shrinkE[0])), 'utf-8'))
    time.sleep(.3)
    connection.send(bytes(str(shrinkE[0]), 'utf-8'))
    time.sleep(.3)
    connection.send(bytes(str(len(shrinkE[1])), 'utf-8'))
    time.sleep(.3)
    connection.send(bytes(str(shrinkE[1]), 'utf-8'))
    time.sleep(.3)
    connection.send(bytes(str(len(shrinkN[0])), 'utf-8'))
    time.sleep(.3)
    connection.send(bytes(str(shrinkN[0]), 'utf-8'))
    time.sleep(.3)
    connection.send(bytes(str(len(shrinkN[1])), 'utf-8'))
    time.sleep(.3)
    connection.send(bytes(str(shrinkN[1]), 'utf-8'))

    # recieve the server's public key
    sizeOfDividedNumber = int(connection.recv(1024).decode())
    DividesysE = int(connection.recv(sizeOfDividedNumber).decode())
    sizeOfModNumber = int(connection.recv(1024).decode())
    modSysE = int(connection.recv(sizeOfModNumber).decode())
    eValue = (DividesysE * maxsize) + modSysE
    logging.info("E: " + str(eValue))

    sizeOfDividedNumber = int(connection.recv(1024).decode())
    DividesysN = int(connection.recv(sizeOfDividedNumber).decode())
    sizeOfModNumber = int(connection.recv(1024).decode())
    modSysN = int(connection.recv(sizeOfModNumber).decode())
    nValue = (DividesysN * maxsize) + modSysN
    logging.info("N: " + str(nValue))

    logging.info("Server information has been recieved!")
    logging.info("Server's public key is: " + str(eValue))

    return (nValue, eValue)

def incomingMessages(client:socket,n:int,d:int):
    while(True):
        data = int(client.recv(2048).decode())
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
    logging.info("e: " + str(e))
    logging.info("n: "+ str(n))
    logging.info("d:" +str(d))
    main(n, phiOfN, e, d)