import json
import threading
import socket
import sys
from equations import *

maxsize = 2147483647
# file near identical to /server.py, comments found in that file

def main(n: int, e: int, d: int):
    host: str = ""
    with open('ip.txt', 'r') as ip:
        host = ip.read().rstrip()
    port: int = 2049
    server = None
    try:
        server: socket = socket.create_connection(address=(host, port))
    except:
        print("connection to server refused")
        sys.exit(1)
    logging.info("Client is running!")
    server_account: tuple = sendUserInformation(server, n, e)
    time.sleep(2)

    incoming_messages_thread = threading.Thread(target=incoming_messages, args=(server, d, n))
    send_messages_thread = threading.Thread(target=sendMessages, args=(server, server_account))

    incoming_messages_thread.start()
    send_messages_thread.start()

    return


def sendMessages(client: socket, server: tuple):
    while True:
        message = input("Enter a message: ")
        encrypted_message: int = encrypt_message(message.upper(), server[1], server[0])
        logging.info("Encrypted Message: " + str(encrypted_message))
        client.send("sending Message".encode())
        send_message(client, encrypted_message)


def sendUserInformation(connection: socket, n: int, e: int) -> tuple:
    keys = receive_keys_over_socket(connection)
    send_keys_over_socket(connection, n, e)
    return keys


def incoming_messages(connection: socket, private_key: int, public_key: int):
    while True:
        size_of_message = connection.recv(2048).decode()
        if size_of_message != "":
            message = receive_message(connection)
            logging.info("Message has been received!")
            print("Encrypted message: " + str(message))
            print("Decrypted message: " + decrypt_message(message, private_key, public_key))

if __name__ == "__main__":
    logging.basicConfig(format='[CLIENT] %(asctime)s - %(message)s', level=logging.INFO)
    with open('pClient.txt', 'r') as file:
        p = int(file.read().rstrip())
    with open('qClient.txt', 'r') as file:
        q = int(file.read().rstrip())
    n, phi, e, d = generate_keys(p, q)
    main(n, e, d)
