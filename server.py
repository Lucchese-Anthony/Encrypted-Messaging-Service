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

def main():
        # TODO query text file to see if user is new
    # TOOO send back the user's public key and keep it in the code
    # TODO accept all incoming messages from users

    host = "freebsd3.cs.scranton.edu"
    port = 30000
    server = socket.socket()
    server.bind((host, port))
    allConnectedUsers = list()
    print("Allowing connections!")
    newSocketConnectionThread = threading.Thread(target=newSocketConnection, args=(allConnectedUsers,server))
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(allConnectedUsers,server))
    closeProgramThread = threading.Thread(target=closeServer, args=(server,))
    incomingMessagesThread.start()
    newSocketConnectionThread.start()
    closeProgramThread.start()
    print(server)
    print("Server is running!")
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
        # TODO implement multiple people allowing to connect at the same time and managing that

def incomingUser(allConnectedUsers:list, connection:socket):
    # TODO insert each newcoming user into the list
    # TODO pop the first user each time the new incoming user is ready
    username = repr(connection.recv(1024))
    password = repr(connection.recv(1024))
    print(username)
    print(password)
    userInfo = user(username, password)
    incomingUser = user("username", "password")
    if userExists(userInfo):
        if verifyUser(userInfo):
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
        

def parseMessage(message:str):
    # TODO parse message into a message object
    return message

if __name__ == "__main__":
    main()