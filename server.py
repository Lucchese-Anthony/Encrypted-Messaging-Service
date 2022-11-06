import math
import struct
import database
from objects import message
from objects import user
import threading
import socket
import os
import time
import sys
import signal
import logging
import pickle
import random

letterConversions:dict = {
"A":"01","B":"02","C":"03","D":"04","E":"05",
"F":"06","G":"07","H":"08","I":"09","J":"10",
"K":"11","L":"12","M":"13","N":"14","O":"15",
"P":"16","Q":"17","R":"18","S":"19","T":"20",
"U":"21","V":"22","W":"23","X":"24","Y":"25",
"Z":"26"}

def main(n, phiOfN, e, d):
    # TODO query text file to see if user is new
    # TOOO send back the user's public key and keep it in the code
    # TODO accept all incoming messages from users

    host = "freebsd3.cs.scranton.edu"
    port = 30000
    allConnectedUsers = list()

    server = socket.socket()
    server.bind((host, port))
    logging.info("Allowing connections!")
    serverAccount = (n, e)
    newSocketConnectionThread = threading.Thread(target=newSocketConnection, args=(allConnectedUsers, server, serverAccount))
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(allConnectedUsers, server, serverAccount))
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
        if user.getUsername() == users.getUsername():
            return False
    return True

def sendErrorMessageBack(message:message, errorMessage:str):
    # TODO send error message back to user 
    message.setMesage(errorMessage)
    sendErrorMessageBack(message)

def incomingMessages(allConnectedUsers:list, server:socket, serverAccount:user):
    messageQueue = list()
    while(True):
        for connection in allConnectedUsers:
            try:
                sizeOfMessage = connection.recv(2048)
                if sizeOfMessage:
                    message:message = connection.recv(int(sizeOfMessage))
                    messageQueue.append((connection, message))
                    logging.info("Message has been received!")
                    connection[0].send(b'Message has been received!')
                    sendMassMessage(messageQueue, allConnectedUsers)
            except:
                continue
        time.sleep(1)


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
    d = findD(e, getPhiOfN(p, q))
    timeToComplete = time.time() - timeToComplete
    logging.info("time to complete d: " + str(timeToComplete))
    main(p*q,phiOfN, e, d)