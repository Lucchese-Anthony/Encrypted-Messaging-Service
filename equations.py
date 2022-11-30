import json
import random
import logging
import socket
import time
import textwrap
from sympy.ntheory.factor_ import totient

letterConversions: dict = {
    "A": "01", "B": "02", "C": "03", "D": "04", "E": "05",
    "F": "06", "G": "07", "H": "08", "I": "09", "J": "10",
    "K": "11", "L": "12", "M": "13", "N": "14", "O": "15",
    "P": "16", "Q": "17", "R": "18", "S": "19", "T": "20",
    "U": "21", "V": "22", "W": "23", "X": "24", "Y": "25",
    "Z": "26", " ": "27", ".": "28", ",": "29", "?": "30",
    "!": "31", "'": "32", '"': "33", "(": "34", ")": "35",
    "[": "36", "]": "37", "{": "38", "}": "39", "<": "40",
    ">": "41", "/": "42", "\\": "43", ":": "44", ";": "45",
    "@": "46", "#": "47", "$": "48", "%": "49", "^": "50",
    "&": "51", "*": "52", "+": "53", "-": "54", "_": "55",
    "=": "56", "`": "57", "~": "58", "0": "59", "1": "60",
    "2": "61", "3": "62", "4": "63", "5": "64", "6": "65",
    "7": "66", "8": "67", "9": "68"
}


def get_phi_of_a_prime(p, q):
    return (p - 1) * (q - 1)


def phi(a):
    return totient(a)


def generate_e(p, q):
    while True:
        e: int = random.randint(10 ** 20, 10 ** 40)
        if euclidean_algorithm(get_phi_of_a_prime(p, q), e) == 1:
            return e


def euclidean_algorithm(top: int, bottom: int) -> int:
    if bottom > top:
        temp = bottom
        bottom = top
        top = temp
    sequence = [top, bottom]
    while sequence[-1] != 0:
        rem = top % bottom
        sequence.append(rem)
        top = bottom
        bottom = rem
    return sequence[-2]


def find_exponent_modulo_n(number: int, exponent: int, n: int) -> int:
    return_num: int = 1
    result = (bin(exponent)[2:])[::-1]
    temp = number % n
    for i in range(0, len(result)):

        if i != 0:
            temp = (temp * temp) % n
        if result[i] == '1':
            return_num = (return_num * temp) % n
    return return_num


def find_d(e: int, phi_of_n: int) -> int:
    return find_exponent_modulo_n(e, phi(phi_of_n) - 1, phi_of_n)


def encrypt_message(message: str, public_key: int, n: int) -> int:
    return find_exponent_modulo_n(convertStringToNumber(message), public_key, n)


def decrypt_message(message: str, private_key: int, n: int) -> str:
    decrypted_message = find_exponent_modulo_n(int(message), private_key, n)
    return convertNumberToString(decrypted_message)


def separate_number_into_n_chunks(number: int, num_of_chunks: int) -> list:
    chunks = textwrap.wrap(str(number), num_of_chunks)
    for i in range(len(chunks)): chunks[i] = int(chunks[i])
    return chunks


def convert_to_array(num: int) -> list:
    array = list()
    for i in str(num): array.append(int(i))
    return array


def convert_to_int(num_list: list) -> int:
    # might be an issue with the length of the numbers
    return int("".join(num_list))


def send_keys_over_socket(connection: socket, n: int, e: int) -> tuple:
    # send the server object
    n_array = convert_to_array(n)
    e_array = convert_to_array(e)
    data = json.dumps({"n": n_array, "e": e_array})
    connection.send(data.encode())
    logging.info("User information has been received!")


def receive_message(connection: socket):
    message_array = json.loads(connection.recv(2048).decode())
    return convert_to_int(message_array.get("m"))


def send_message(connection: socket, message: int):
    message_array = convert_to_array(message)
    data = json.dumps({"m": message_array})
    connection.send(data.encode())


def receive_keys_over_socket(connection: socket):
    incoming_data = json.loads(connection.recv(2048).decode())
    user_n = convert_to_int(incoming_data.get('n'))
    user_e = convert_to_int(incoming_data.get('e'))
    logging.info("User information has been received!")
    logging.info("User's public key is: " + str(user_e))
    logging.info("User's n value is " + str(user_n))
    return user_n, user_e

def generate_keys(p: int, q: int):
    phi = get_phi_of_a_prime(p, q)
    n = p * q
    time_to_complete = time.time()
    e = generate_e(p, q)
    time_to_complete = time.time() - time_to_complete
    logging.info("time to complete e: " + str(time_to_complete))

    time_to_complete = time.time()
    d = find_d(e, get_phi_of_a_prime(p, q))
    time_to_complete = time.time() - time_to_complete
    logging.info("time to complete d: " + str(time_to_complete))
    logging.info("e: " + str(e))
    logging.info("n: " + str(n))
    logging.info("d: " + str(d))
    return n, phi, e, d


def combineNumbersIntoOneNumber(number: list) -> int:
    result = 0
    result = (int(number[9])) * (10 ** 100) + (int(number[8])) * (10 ** 90) + (int(number[7])) * (10 ** 80) + (
        int(number[7])) * (10 ** 70) + (int(number[6])) * (10 ** 60) + (int(number[5])) * (10 ** 50) + (
                 int(number[4])) * (10 ** 40) + (int(number[3])) * (10 ** 30) + (int(number[2])) * (10 ** 20) + (
                 int(number[1])) * (10 ** 10) + (int(number[0])) * (10 ** 0)
    print(result)
    return int(result)


def convertNumberToString(number: int) -> str:
    string = ""
    number = str(number)
    if len(number) % 2 != 0:
        number = "0" + number
    for i in range(0, len(number), 2):
        string += list(letterConversions.keys())[list(letterConversions.values()).index(number[i:i + 2])]
    return string


def convertStringToNumber(string: str) -> int:
    number = ""
    string = string.upper()
    for i in range(len(string)):
        number += letterConversions[string[i]]
    return int(number)
