import json
import sys
from objects import user
import threading
import os
from equations import *

maxsize = 2147483647  # max int size of the Raspberry Pi


def main(n, e, d):
    host: str = ""
    with open('ip.txt', 'r') as ip:
        # reads in the IP from a text file, so the IP isnt public on GitHub
        host = ip.read().rstrip()
    port: int = 2049  # port attached to
    # socket library python https://docs.python.org/3/library/socket.html
    server = socket.socket()
    server.bind((host, port))  # binds to the port and IP
    logging.info("Server is running!")
    logging.info("Allowing connections!")
    # n value and e value generated at the bottom of the file
    public_key = {"n": n, "e": e}

    server.listen(1)  # waiting for a client to connect
    # client connected, getting the connection session and address from which they connected to
    connection, address = server.accept()
    logging.info("Connection from: " + str(address))
    # n, e values from the connected client
    connected_user = exchangeKeys(connection, public_key)
    time.sleep(2)
    incoming_messages_thread = threading.Thread(target=incoming_messages, args=(
        connected_user, connection, public_key, d))  # thread to listen for incoming messages
    close_program_thread = threading.Thread(target=closeServer, args=(
        public_key,))  # thread to listen to close the program
    send_messages_thread = threading.Thread(target=sendMessages, args=(
        connection, connected_user))  # thread to send messages

    send_messages_thread.start()
    incoming_messages_thread.start()  # start the threads
    close_program_thread.start()
    while True:
        if not close_program_thread.is_alive():
            os._exit(os.EX_OK)  # close the program


# method to send messages to the client
def sendMessages(client: socket, client_keys: tuple):
    while True:  # loop over iterative messages that want to be sent
        message = input("Enter a message: ")
        encrypted_message: int = encrypt_message(message.upper(
        ), client_keys[1], client_keys[0])  # encrypts the message using the clients keys
        logging.info("Encrypted Message: " + str(encrypted_message))
        client.send("sending Message".encode())
        send_message(client, encrypted_message)  # method to send the message


def closeServer(server):
    end_program = ''

    while end_program != "e":
        end_program = input("")
    print('closing server')  # closes program
    server.close()
    print('ending program')
    sys.exit()


# exchange keys between server and client
def exchangeKeys(connection: socket, server_public_key: dict) -> user:
    # sends keys to the client
    send_keys_over_socket(
        connection,  server_public_key["n"], server_public_key["e"])
    # recieves keys from the client
    return receive_keys_over_socket(connection)


# thread to listen for incoming messaghes
def incoming_messages(connected_user, connection: socket, server: tuple, private_key: int):
    while True:
        # waits for a message that isnt blank
        size_of_message = connection.recv(2048).decode()
        if size_of_message != "":
            # recieves a message from the
            message = receive_message(connection)
            logging.info("Message has been received!")
            print("Encrypted message: " + str(message))
            print("Decrypted message: " +
                  decrypt_message(message, private_key, server["n"]))


if __name__ == "__main__":
    logging.basicConfig(
        format='[SERVER] %(asctime)s - %(message)s', level=logging.INFO)
    p = 0
    q = 0
    with open('pServer.txt', 'r') as file:
        p = int(file.read().rstrip()) # imports a prime number from a file 
    with open('qServer.txt', 'r') as file:
        q = int(file.read().rstrip()) # imports another prime number from a file
    n, phi, e, d = generate_keys(p, q) # generates phi, e, and d given p and q
    main(n, e, d)
