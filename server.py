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

def main(n, e, d):

    host = "freebsd3.cs.scranton.edu"
    port = 30000

    server = socket.socket()
    server.bind((host, port))
    logging.info("Allowing connections!")
    publicKey = {"n": n, "e": e}

    server.listen(2)
    connection, address = server.accept()
    print("Connection from: " + str(address))
    connectedUser = exchangeKeys(connection, publicKey)  

    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(connectedUser, connection, publicKey, d))
    closeProgramThread = threading.Thread(target=closeServer, args=(publicKey,))

    incomingMessagesThread.start()
    closeProgramThread.start()

    logging.info(server)
    logging.info("Server is running!")
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

    sizeOfUserE = connection.recv(4086)
    print(sizeOfUserE.decode())
    userE = connection.recv(int.from_bytes(sizeOfUserE, byteorder='big')) * sys.maxsize
    sizeOfUserN = connection.recv(4086)
    logging.info("E: " + str(userE.decode()))
    userN = connection.recv(int.from_bytes(sizeOfUserN, byteorder='big')) * sys.maxsize
    logging.info("N: " + str(userN.decode()))
    logging.info("User information has been recieved!")
    logging.info("User's public key is: " + str(userE))

    sizeOfE = len(str(serverPublicKey["e"]))
    connection.send(bytes(str(sizeOfE), 'utf-8'))
    connection.send(bytes(str(serverPublicKey["e"]), 'utf-8'))
    sizeOfN = len(str(serverPublicKey["n"]))
    connection.send(bytes(str(sizeOfN), 'utf-8'))
    connection.send(bytes(str(serverPublicKey["n"]), 'utf-8'))

    logging.info("Sent server's public key to user!")

    # deserialize the user
    return user


def incomingMessages(connection:socket, server:tuple, privateKey:int):
    while(True):
        sizeOfMessage = connection.recv(2048)
        message = connection.recv(int(sizeOfMessage))
        logging.info("Message has been received!")
        print("Encrypted message: " + str(message))
        print("Decrypted message: " + decryptMessage(message, privateKey, server))
        
if __name__ == "__main__":
    logging.basicConfig(format='[SERVER] %(asctime)s - %(message)s',level=logging.INFO)
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
    logging.info("e: " + str(e))
    logging.info("d: " + str(d))
    main(n, e, d)