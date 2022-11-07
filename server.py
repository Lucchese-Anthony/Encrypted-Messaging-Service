from objects import message
from objects import user
import threading
import socket
import os
import time
import sys
import logging
import pickle
import random
import math
from equations import *

def main(n, phiOfN, e, d):

    host = "freebsd3.cs.scranton.edu"
    port = 30000
    allConnectedUsers = list()

    server = socket.socket()
    server.bind((host, port))
    logging.info("Allowing connections!")
    serverAccount = (n, e)

    newSocketConnectionThread = threading.Thread(target=newSocketConnection, args=(allConnectedUsers, server, serverAccount))
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(allConnectedUsers, server, d))
    closeProgramThread = threading.Thread(target=closeServer, args=(server,))

    incomingMessagesThread.start()
    newSocketConnectionThread.start()
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


def newSocketConnection(allConnectedUsers:list, server:socket, serverAccount:tuple):
    while(True):
        server.listen(2)
        connection, address = server.accept()
        print("Connection from: " + str(address))
        connection.sendall(b'welcome!')
        incomingUser(allConnectedUsers, connection, serverAccount)

def incomingUser(allConnectedUsers:list, connection:socket, serverAccount:tuple):
    # TODO insert each newcoming user into the list
    # TODO pop the first user each time the new incoming user is ready
    sizeOfUser = connection.recv(2048)
    newUser:user = pickle.loads(connection.recv(int.from_bytes(sizeOfUser, byteorder='big')))
    logging.info("User has logged in with: " + newUser.getUsername())
    # deserialize the user
    if isNewUser(newUser, allConnectedUsers):
        createNewUser(newUser, allConnectedUsers, connection)
        connection.send(bytes(str(serverAccount[0]), 'utf-8'))
        connection.send(bytes(str(serverAccount[1]), 'utf-8'))
    else:
        logging.info("User is already in the list of users!")
        connection.send(b'User is already in the list of users!')
    return

def createNewUser(user:user, allConnectedUsers:list, connection:socket):
    allConnectedUsers.append((connection, user))
    logging.info("User has been added to the list of users!")
    connection.send(b'Successfully added to the server!')

def isNewUser(user:user, allConnectedUsers:list) -> bool:
    for users in allConnectedUsers:
        if user.getUsername() == users[1].getUsername():
            return False
    return True

def sendErrorMessageBack(message:message, errorMessage:str):
    # TODO send error message back to user 
    message.setMesage(errorMessage)
    sendErrorMessageBack(message)

def incomingMessages(allConnectedUsers:list, serverAccount:tuple, privateKey:int):
    messageQueue = list()
    while(True):
        for connection in allConnectedUsers:
            try:
                sizeOfMessage = connection[0].recv(2048)
                if sizeOfMessage:
                    message = connection[0].recv(int(sizeOfMessage))
                    messageQueue.append((connection[0], decryptMessage(message, privateKey)))
                    logging.info("Message has been received!")
                    connection[0].send(b'Message has been received!')
                    sendMassMessage(messageQueue, allConnectedUsers, serverAccount)
            except:
                continue
        time.sleep(1)

def sendMassMessage(messageQueue:list, allConnectedUsers:list):
    while(len(messageQueue) > 0):
        message = messageQueue.pop(0)
        for connection in allConnectedUsers:
            if connection[0] != message[0]:
                connection.send(bytes(encryptMessage(message[1], user.getE())), 'utf-8')
                logging.info("Message has been sent to the receiver!")
                connection.send(b'Message has been sent to the receiver!')
                break

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
    main(p*q,phiOfN, e, d)