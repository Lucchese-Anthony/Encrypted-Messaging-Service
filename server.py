import json

from objects import user
import threading
import socket
import os
from equations import *

maxsize = 2147483647


def main(n, e, d):
    host: str = ""
    with open('ip.txt', 'r') as ip:
        host = ip.read().rstrip()
    port: int = 2049
    server = socket.socket()
    server.bind((host, port))
    logging.info(server)
    logging.info("Server is running!")
    logging.info("Allowing connections!")
    public_key = {"n": n, "e": e}

    server.listen(1)
    connection, address = server.accept()
    logging.info("Connection from: " + str(address))
    connectedUser = exchangeKeys(connection, public_key)
    time.sleep(5)
    incomingMessagesThread = threading.Thread(target=incoming_messages, args=(connectedUser, connection, public_key, d))
    closeProgramThread = threading.Thread(target=closeServer, args=(public_key,))

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


def exchangeKeys(connection: socket, server_public_key: dict) -> user:
    send_keys_over_socket(connection)
    return receive_keys_over_socket(connection, server_public_key["e"], server_public_key['n'])


def incoming_messages(connected_user, connection: socket, server: tuple, private_key: int):
    while True:
        size_of_message = connection.recv(2048).decode()
        if size_of_message != "":
            DivMessage = int(connection.recv(int(size_of_message)).decode())
            modMessageSize = connection.recv(2048).decode()
            modMessage = int(connection.recv(int(modMessageSize)).decode())
            message = (DivMessage * maxsize) + modMessage
            logging.info("Message has been received!")
            print("Encrypted message: " + str(message))
            print("Decrypted message: " + decrypt_message(message, private_key, server["n"]))


if __name__ == "__main__":
    logging.basicConfig(format='[SERVER] %(asctime)s - %(message)s', level=logging.INFO)
    p = 0
    q = 0
    with open('pServer.txt', 'r') as file:
        p = int(file.read().rstrip())
    with open('qServer.txt', 'r') as file:
        q = int(file.read().rstrip())
    n, phi, e, d = generate_keys(p, q)
    main(n, e, d)
