import struct
from objects import message
from objects import user
import threading
import socket
import os
import time
import sys
import logging
import random
import math
from equations import *

maxsize = 2147483647

def main(n, e, d):

    host:str = ""
    with open('ip.txt', 'r') as file:
        host = file.read().rstrip()
    port:int = 2049
    server = socket.socket()
    server.bind((host, port))
    logging.info(server)
    logging.info("Server is running!")
    logging.info("Allowing connections!")
    publicKey = {"n": n, "e": e}

    server.listen(1)
    connection, address = server.accept()
    logging.info("Connection from: " + str(address))
    connectedUser = exchangeKeys(connection, publicKey)  
    time.sleep(5)
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(connectedUser, connection, publicKey, d))
    closeProgramThread = threading.Thread(target=closeServer, args=(publicKey,))

    incomingMessagesThread.start()
    closeProgramThread.start()
    while True:
        if not closeProgramThread.isAlive():
            os._exit(os.EX_OK)

def closeServer(server):
    endProgram = ''
    
    while endProgram != "e":
        endProgram = input("")
    print('closing server')
    server.close()
    print('ending program')
    sys.exit()

def exchangeKeys(connection:socket, serverPublicKey:dict) -> user:
    sizeOfDividedNumber = int(connection.recv(1024).decode())
    DividesysE = int(connection.recv(sizeOfDividedNumber).decode())
    sizeOfModNumber = int(connection.recv(1024).decode())
    modSysE = int(connection.recv(sizeOfModNumber).decode())
    eValue = (DividesysE * sys.maxsize) + modSysE
    logging.info("E: " + str(eValue))

    sizeOfDividedNumber2 = int(connection.recv(1024).decode())
    DividesysN = int(connection.recv(sizeOfDividedNumber2).decode())
    sizeOfModNumber2 = int(connection.recv(1024).decode())
    modSysN = int(connection.recv(sizeOfModNumber2).decode())
    nValue = (DividesysN * sys.maxsize) + modSysN
    logging.info("N: " + str(nValue))

    logging.info("User information has been recieved!")
    logging.info("User's public key is: " + str(eValue))

    sendServerKey(connection, serverPublicKey)
    logging.info("Sent server's public key to user!")

    return (nValue, eValue)

def sendServerKey(connection:socket, serverPublicKey:dict)->user:
    shrinkE = shrinkIntToSendOverSocket(serverPublicKey['e'])
    shrinkN = shrinkIntToSendOverSocket(serverPublicKey['n'])

    connection.send(bytes(str(len(shrinkE[0])), 'utf-8'))
    time.sleep(.1)
    connection.send(bytes(str(shrinkE[0]), 'utf-8'))
    time.sleep(.1)
    connection.send(bytes(str(len(shrinkE[1])), 'utf-8'))
    time.sleep(.1)
    connection.send(bytes(str(shrinkE[1]), 'utf-8'))
    time.sleep(.1)
    connection.send(bytes(str(len(shrinkN[0])), 'utf-8'))
    time.sleep(.1)
    connection.send(bytes(str(shrinkN[0]), 'utf-8'))
    time.sleep(.1)
    connection.send(bytes(str(len(shrinkN[1])), 'utf-8'))
    time.sleep(.1)
    connection.send(bytes(str(shrinkN[1]), 'utf-8'))



def incomingMessages(connectedUser, connection:socket, server:tuple, privateKey:int):
    while(True):
        sizeOfMessage = connection.recv(2048).decode()
        if sizeOfMessage != "":
            message = connection.recv(int(sizeOfMessage)).decode()
            logging.info("Message has been received!")
            print("Encrypted message: " + str(message))
            print("Decrypted message: " + decryptMessage(message, privateKey, server["n"]))
        
if __name__ == "__main__":
    logging.basicConfig(format='[SERVER] %(asctime)s - %(message)s',level=logging.INFO)
    p = 0
    q = 0
    with open('pServer.txt', 'r') as file:
        p = int(file.read().rstrip())
    with open('qServer.txt', 'r') as file:
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
    logging.info("d: " + str(d))
    numbers = shrinkIntToSendOverSocket(e)
    print(e == (int(numbers[0]) * sys.maxsize) + int(numbers[1]))
    main(n, e, d)