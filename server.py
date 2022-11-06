import math
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

    newSocketConnectionThread = threading.Thread(target=newSocketConnection, args=(allConnectedUsers,server))
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(allConnectedUsers,server))
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


def newSocketConnection(allConnectedUsers:list, server:socket):
    while(True):
        server.listen(2)
        connection, address = server.accept()
        print("Connection from: " + str(address))
        connection.sendall(b'welcome!')
        incomingUser(allConnectedUsers, connection)

def incomingUser(allConnectedUsers:list, connection:socket):
    # TODO insert each newcoming user into the list
    # TODO pop the first user each time the new incoming user is ready
    newUser:user = pickle.loads(connection.recv(10000))
    logging.info("User has logged in with: " + newUser.getUsername())
    # deserialize the user
    if userExists(newUser):
        if verifyUser(newUser):
            print("User Exists!")
    else:
        createNewUser(user)
    allConnectedUsers.append(connection)

    return

def createNewUser(user:user):
    # TODO create new user with username and str pass
    # TODO insert into DB new username and pass

    database.insertUser(user.getUsername(), user.getPassword())
    return

def userExists(user:user):
    # TODO connect socket to user
    return True
    #return True if database.queryUsername(user.getUsername()).getUsername() == user.getUsername() else False

def verifyUser(userInfo:user):
    return userInfo == user("username", "password")

def sendMessage(message:message):
    # TODO send message from fromUsername to toUsername 
    return

def validMessage(message:message):
    # TODO check validity of message being sent
    return True
    # dbResult = database.queryUsername(message.getToUser)
    # return True if dbResult != None else False

def sendErrorMessageBack(message:message, errorMessage:str):
    # TODO send error message back to user 
    message.setMesage(errorMessage)
    sendErrorMessageBack(message)


def incomingMessages(allConnectedUsers:list, server:socket):
    messageQueue = list()
    while(True):
        for connection in allConnectedUsers:
            try:
                message = connection.recv(1024)
                messageQueue.append(message)
                message = parseMessage(recievedMessage)
                # TODO accept in tuple of (fromUsername, toUsername, message)
                # check if message can be sent to the given user
                if validMessage(message):
                    sendMessage(fromUsername, toUsername, message)
                    database.storeMessage(newMessage)
                else:
                    sendErrorMessageBack(newMessage.getFromUser, "Unable to send message!")
            except:
                None

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


def parseMessage(message:str):
    # TODO parse message into a message object
    return message

if __name__ == "__main__":
    logging.basicConfig(format='[SERVER]%(asctime)s - %(message)s',level=logging.INFO)
    p = 0
    q = 0
    with open('p.txt', 'r') as file:
        p = int(file.read().rstrip())
    with open('q.txt', 'r') as file:
        q = int(file.read().rstrip())
    n = p*q
    phiOfN = getPhiOfN(p, q)
    e = generateE(p, q)
    d = findD(e, phiOfN)
    main(p*q,phiOfN, e, d)