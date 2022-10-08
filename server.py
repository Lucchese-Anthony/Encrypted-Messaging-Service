import math
import database
from objects import message
from objects import user
import threading

import asyncio
import signal
import os

import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        echo,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await stop


def main1():
    # TODO initialize server
    # TODO ask for username password
        # TODO query database for correct username and password
    # TOOO send back the user's public key and keep it in the code
    # TODO accept all incoming messages from users
    '''
    ws = create_connection("ws://myapp.herokuapp.com")
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()
    '''
    ws = create_connection("ws://myapp.herokuapp.com")
    allConnectedUsers = list()
    incomingSocketConnection = threading.Thread(target=newSocketConnection)
    incomingUserThread = threading.Thread(target=bufferIncomingUsers, args=(allConnectedUsers,))
    incomingMessagesThread = threading.Thread(target=incomingMessages, args=(allConnectedUsers,))
    # TODO place the user into a queue
    return

def newSocketConnection(allConnectedUsers:list, server_socket:socket):
    # TODO figure out sockets
    while(True):
        server_socket.listen(2)
        connection, address = server_socket.accept()
        print("Connection from: " + str(address))
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

    database.insertUser(username, password)
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
    asyncio.run(main())