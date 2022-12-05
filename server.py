import json
import sys
from objects import user
import threading
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
    logging.info("Server is running!")
    logging.info("Allowing connections!")
    public_key = {"n": n, "e": e}

    server.listen(1)
    connection, address = server.accept()
    logging.info("Connection from: " + str(address))
    connected_user = exchangeKeys(connection, public_key)
    time.sleep(2)
    incoming_messages_thread = threading.Thread(target=incoming_messages, args=(
        connected_user, connection, public_key, d)) 
    close_program_thread = threading.Thread(target=closeServer, args=(
        public_key,)) 
    send_messages_thread = threading.Thread(target=sendMessages, args=(
        connection, connected_user))

    send_messages_thread.start()
    incoming_messages_thread.start() 
    close_program_thread.start()
    while True:
        if not close_program_thread.is_alive():
            os._exit(os.EX_OK)  


def sendMessages(client: socket, client_keys: tuple):
    while True:  
        message = input("Enter a message: \n")
        encrypted_message: int = encrypt_message(message.upper(
        ), client_keys[1], client_keys[0]) 
        logging.info("Encrypted Message: " + str(encrypted_message))
        client.send("Sending Encrypted Message".encode())
        send_message(client, encrypted_message)  


def closeServer(server):
    end_program = ''

    while end_program != "e":
        end_program = input("")
    print('closing server')
    server.close()
    print('ending program')
    sys.exit()


def exchangeKeys(connection: socket, server_public_key: dict) -> user:
    send_keys_over_socket(
        connection,  server_public_key["n"], server_public_key["e"])
    return receive_keys_over_socket(connection)


def incoming_messages(connected_user, connection: socket, server: tuple, private_key: int):
    while True:
        size_of_message = connection.recv(2048).decode()
        if size_of_message != "":
            message = receive_message(connection)
            logging.info("Message has been received!")
            logging.info("Encrypted message: " + str(message))
            logging.info("Decrypted message: " +
                  decrypt_message(message, private_key, server["n"]))


if __name__ == "__main__":
    logging.basicConfig(
        format='[SERVER] %(asctime)s - %(message)s', level=logging.INFO)
    p = 0
    q = 0
    with open('pServer.txt', 'r') as file:
        p = int(file.read().rstrip()) 
    with open('qServer.txt', 'r') as file:
        q = int(file.read().rstrip()) 
    n, phi, e, d = generate_keys(p, q) 
    main(n, e, d)