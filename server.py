import math
import database
from objects import message
from objects import user
import threading
import socket
import asyncio
import signal
import os
import time

def main():
    # TODO initialize server
    # TODO ask for username password
        # TODO query database for correct username and password
    # TOOO send back the user's public key and keep it in the code
    # TODO accept all incoming messages from users

    # get the hostname
    host = "0.0.0.0"
    port = 1022  # initiate port no above 1024
    # look closely. The bind() function takes tuple as argument


    server = socket.socket()
    time.sleep(1)
    server.bind((host, port))
    allConnectedUsers = list()
    print("Allowing connections!")
    newSocketConnectionThread = threading.Thread(target=newSocketConnection, args=(allConnectedUsers,server))
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(allConnectedUsers,server))
    incomingMessagesThread.start()
    newSocketConnectionThread.start()
    # TODO place the user into a queue
    print(server)
    return

def newSocketConnection(allConnectedUsers:list, server:socket):
    # TODO figure out sockets
    while(True):
        server.listen(2)
        connection, address = server.accept()
        print("Connection from: " + str(address))
        allConnectedUsers.append(connection)
        connection.sendall(b'welcome!')
        incomingUser(connection)
        # TODO attempt at basic socketing

def incomingUser(connection):
    # TODO insert each newcoming user into the list
    # TODO pop the first user each time the new incoming user is ready
    userInfo = connection.recv(1024)
    print(userInfo)
    incomingUser = user("username", "password")
    while(True):
        if userExists(user):
            verifyUser(user)
        else:
            createNewUser(user)
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

def verifyUser(user:user):
    return 
    # return user == database.queryUser(user.getUsername())

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