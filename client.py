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

letterConversions:dict = {
"A":"01","B":"02","C":"03","D":"04","E":"05",
"F":"06","G":"07","H":"08","I":"09","J":"10",
"K":"11","L":"12","M":"13","N":"14","O":"15",
"P":"16","Q":"17","R":"18","S":"19","T":"20",
"U":"21","V":"22","W":"23","X":"24","Y":"25",
"Z":"26"}


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

def findD(e:int, phiOfN:int, n:int) -> int:
    return findExponentModN(e, phiOfN-1, n)

def findExponentModN(number:int, exponent:int, n:int) -> int:
    returnNum:int = 0
    result = bin(exponent)[2:]
    for i in range(len(result)):
        number = (number * number) % n
        if result[i] == "1":
            returnNum = number * number % n
    return returnNum % n

def decryptMessage(message:int, privateKey:int, n:int) -> str:
    return convertNumberToString(findExponentModN(int(message), privateKey, n))

def encryptMessage(message:str, serverPublicKey:int, n:int) -> int:
    return findExponentModN(convertStringToNumber(message), serverPublicKey, n)

def convertNumberToString(number:int) -> str:
    string = ""
    number = str(number)
    if len(number) % 2 != 0:
        number = "0" + number
    for i in range(0, len(number), 2):
        string += list(letterConversions.keys())[list(letterConversions.values()).index(number[i:i+2])]
    return string

def convertStringToNumber(string:str) -> int:
    number = ""
    for i in range(len(string)):
        number += letterConversions[string[i]]
    return int(number)

def getPhiOfN(p, q):
    return (p-1)*(q-1)

def generateE(p, q):
    while(True):
        e:int = random.randint(11,100)
        if EuclideanAlgorithm(getPhiOfN(p, q), e) == 1:
            return e

def EuclideanAlgorithm(top:int, bottom:int) -> int:
    if bottom > top:
        temp = bottom
        bottom = top
        top = temp
    sequence = [top, bottom]
    while(sequence[-1] != 0):
        rem = top % bottom
        sequence.append(rem)
        top = bottom
        bottom = rem
    return sequence[-2]

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