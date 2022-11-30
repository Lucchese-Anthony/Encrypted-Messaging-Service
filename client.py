import json
import threading
import socket
import sys
from equations import *

maxsize = 2147483647


def main(n: int, e: int, d: int):
    host: str = ""
    with open('ip.txt', 'r') as ip:
        host = ip.read().rstrip()
    port: int = 2049
    client = None
    try:
        client: socket = socket.create_connection(address=(host, port))
    except:
        print("Server connection refused")
        sys.exit(1)
    time.sleep(.5)
    server_account: tuple = sendUserInformation(client, n, e)
    time.sleep(2)
    incoming_messages_thread = threading.Thread(target=incomingMessages, args=(client, n, d))
    send_messages_thread = threading.Thread(target=sendMessages, args=(client, n, e, d, server_account))

    incoming_messages_thread.start()
    send_messages_thread.start()

    return


def sendMessages(client: socket, server: tuple):
    while True:
        message = input("Enter a message:")
        encrypted_message: int = encrypt_message(message.upper(), server[1], server[0])
        logging.info("Message: " + message)
        logging.info("Encrypted Message: " + str(encrypted_message))
        client.send("sending Message".encode())
        send_message(client, message)


def sendUserInformation(connection: socket, n: int, e: int) -> tuple:
    keys = receive_keys_over_socket(connection)
    send_keys_over_socket(connection, n, e)
    return keys


def incomingMessages(client: socket, n: int, d: int):
    while True:
        data = receive_message(client)
        print("Encrypted message: " + str(data))
        decrypted_message = decrypt_message(int.from_bytes(data, byteorder='big'), n, d)
        print("Decrypted Message: " + decrypted_message)


if __name__ == "__main__":
    logging.basicConfig(format='[CLIENT] %(asctime)s - %(message)s', level=logging.INFO)
    with open('pClient.txt', 'r') as file:
        p = int(file.read().rstrip())
    with open('qClient.txt', 'r') as file:
        q = int(file.read().rstrip())
    n, phi, e, d = generate_keys(p, q)
    encrypt = encrypt_message("Hello!", e, n)
    main(n, e, d)

