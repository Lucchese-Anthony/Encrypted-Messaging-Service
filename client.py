import math
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
    host = ""
    with open('ip.txt', 'r') as file:
        host = file.read().rstrip()
    port = 30000
    
    try: 
        client = socket.create_connection(address=(host, port))
    except:
        print("Server connection refused")
        sys.exit(1)
    logging.info("Connected to server!")
    username = input("Enter a Username: ")
    password = input("Enter a Password: ")
    newUser = user(username, password, n, e)
    # TODO serialize newUser
    client.send(pickle.dumps(newUser))
    #generatePublicKey()
    print("Sent User Information!")
    data = client.recv(1024)
    print("Received message: " + data.decode("utf-8"))

    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(client,))
    closeProgramThread = threading.Thread(target=closeServer, args=(client,))

    incomingMessagesThread.start()
    closeProgramThread.start()

    while True:
        if not closeProgramThread.isAlive():
            os._exit(os.EX_OK)

def incomingMessages(client:socket):
    while(True):
        encryptedMessage = client.recv(2048).decode("utf-8")
        print(encryptedMessage)
        decryptedMessage = decryptMessage(encryptedMessage, privateKey)
        print(decryptedMessage)

def closeServer(server):
    endProgram = ''
    
    while endProgram != "e":
        endProgram = input("")
    print('closing server')
    server.close()
    print('ending program')
    sys.exit()

def incomingMessageThread():
    # TODO incoming threads
    return

def outgoingMesssageThread():
    # TODO outgoing threads
    return

def findD(e:int, phiOfN:int) -> int:
    return findExponentModN(e, phiOfN-1)

def findExponentModN(number:int, exponent:int) -> int:
    returnNum:int = 0
    result = bin(exponent)[2:]
    for i in range(len(result)):
        number = (number * number) % n
        if result[i] == "1":
            returnNum = number * number % n
    return returnNum % n

def decryptMessage(message:str, privateKey:int) -> str:
    return convertNumberToString(findExponentModN(int(message), privateKey))

def encryptMessage(message:str, serverPublicKey:int) -> str:
    return findExponentModN(convertStringToNumber(message), serverPublicKey)

def getPhiOfN(p, q):
    n = p*q
    return (p-1)*(q-1)
def generateE(p, q):
    while(True):
        e:int = random.randint(11,100)
        if EuclideanAlgorithm(getPhiOfN(p, q), e) == 1:
            return e

def convertStringToNumber(string:str) -> int:
    number = ""
    for i in range(len(string)):
        number += letterConversions[string[i]]
    return int(number)

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
    d = findD(e, getPhiOfN(p, q))
    timeToComplete = time.time() - timeToComplete
    logging.info("time to complete d: " + str(timeToComplete))
    
    main(n, phiOfN, e, d)