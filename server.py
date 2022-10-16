import math
import database
from objects import message
from objects import user
import threading
import socket
import asyncio
import signal
import os

def main():
    # TODO initialize server
    # TODO ask for username password
        # TODO query database for correct username and password
    # TOOO send back the user's public key and keep it in the code
    # TODO accept all incoming messages from users

    # get the hostname
    host = socket.gethostname()
    port = 9001  # initiate port no above 1024
    # look closely. The bind() function takes tuple as argument


    server = socket.socket()
    server.bind((host, port))
    allConnectedUsers = list()
    incomingSocketConnection = threading.Thread(target=newSocketConnection, args=(allConnectedUsers, server))
    print("Allowing connections!")
    incomingUserThread = threading.Thread(target=bufferIncomingUsers, args=(allConnectedUsers,))
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(allConnectedUsers,))
    incomingMessagesThread.start()
    incomingUserThread.start()
    incomingSocketConnection.start()
    # TODO place the user into a queue
    print(server)
    while True:
        None
    return

def newSocketConnection(allConnectedUsers:list, server:socket):
    # TODO figure out sockets
    while(True):
        print("hello@")
        server.listen(2)
        connection, address = server.accept()
        print("Connection from: " + str(address))
        connection.sendall(b'Hello, world')
        allConnectedUsers.append(connection)
        # TODO attempt at basic socketing

def bufferIncomingUsers(allConnectedUsers:list):
    # TODO insert each newcoming use rinto the list
    # TODO pop the first user each time the new incoming user is ready
    while(True):
        if userExists():
            verifyUser()
        else:
            createNewUser()
    return

def createNewUser(user:user):
    # TODO create new user with username and str pass
    # TODO insert into DB new username and pass

    database.insertUser(user.getUsername(), user.getPassword())
    return

def userExists():
    # TODO connect socket to user
    database.queryUsername(username)
    return
def verifyUser(mess):
    database.queryUser(username, password)
def sendMessage(message:message):
    # TODO send message from fromUsername to toUsername 
    return

def validMessage(message:message):
    # TODO check validity of message being sent
    dbResult = database.queryUsername(message.getToUser)
    return True if dbResult != None else False

def sendErrorMessageBack(message:message, errorMessage:str):
    # TODO send error message back to user 
    message.setMesage(errorMessage)
    sendErrorMessageBack(message)


def incomingMessages(allConnectedUsers:list):
    messageQueue = list()
    while(True):
        newMessage = message(fromUser, toUser, message)
        # TODO accept in tuple of (fromUsername, toUsername, message)
        # check if message can be sent to the given user
        if validMessage():
            sendMessage(fromUsername, toUsername, message)
            database.storeMessage(newMessage)
        else:
            sendErrorMessageBack(newMessage.getFromUser, "Unable to send message!")


if __name__ == "__main__":
    main()