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
    return (p - 1) * (q - 1) # proof shown in the writeup, but a simpler return method than phi() if n is a product of two primes


def phi(a) -> int:
    # utilizes the sympy totient library to find the totient of a number, documentation is in the readme.md
    return totient(a)


def generate_e(p, q) -> int: # generates the e value given p and q, proof is shown in the writeup
    while True:
        e: int = random.randint(10 ** 20, 10 ** 40) # pick a random number between 10^20 and 10^40
        if euclidean_algorithm(get_phi_of_a_prime(p, q), e) == 1: # if the gcd(rand, phi(n)) = 1, return e
            return e


def euclidean_algorithm(top: int, bottom: int) -> int: # eulers euclidean algorithm, proof shown in writeup
    if bottom > top: # if statement to switch the numbers in case the second is larger than the first number
        temp = bottom
        bottom = top
        top = temp
    sequence = [top, bottom]
    while sequence[-1] != 0: # while the sequence isnt complete (last number is 0)
        rem = top % bottom # find remainder 
        sequence.append(rem) # take the remainder of top % bottom and add to list
        top = bottom # switch the 1st num with the 2nd num
        bottom = rem # 2nd num replaced with remainder
    return sequence[-2] # return the gcd between the two numbers


def find_exponent_modulo_n(number: int, exponent: int, n: int) -> int: # finds n^e mod n
    return_num: int = 1 
    binary = (bin(exponent)[2:])[::-1] # binary number of the exponent (bin() converts to binary)
    temp = number % n # temporary rewrite variable 
    for i in range(0, len(binary)): # for the length of the binary num
        if i != 0: # fencepost error fix for if i=0 
            temp = (temp * temp) % n
        if binary[i] == '1': # if 2^n is 1, then we multiply the number by temp * 2^n
            return_num = (return_num * temp) % n
    return return_num # return the number


def find_d(e: int, phi_of_n: int) -> int:
    return find_exponent_modulo_n(e, phi(phi_of_n) - 1, phi_of_n) # ed = 1 mod phi(n) => d = e^phi(phi(n)) mod phi(n)


def encrypt_message(message: str, public_key: int, n: int) -> int:
    return find_exponent_modulo_n(convertStringToNumber(message), public_key, n) # m^e mod n = s


def decrypt_message(message: str, private_key: int, n: int) -> str:
    decrypted_message = find_exponent_modulo_n(int(message), private_key, n) # s^d => (m^e)^d = m mod n
    return convertNumberToString(decrypted_message)


def convert_to_array(num: int) -> list: # method that converts 12345 to [1, 2, 3, 4, 5] (useful for socket / bytearrays)
    array = list() # initialise empty list
    for i in str(num): # for each character in the string of numbers
        array.append(int(i)) # append the character to the array
    return array # return the array of numbers


def convert_to_int(num_list: list) -> int: # reverse of above
    num = 0
    for i in range(len(num_list)): # for the length of the number array
        num += num_list[i] * (10**((len(num_list) - 1) - i)) # number += (array at index i) * 10^(length - i)
    return num # return the converted int


def receive_message(connection: socket): # recieves the message from the user
    message_array = json.loads(connection.recv(2048).decode()) # recieves, decodes, then unhashes the JSON message
    return convert_to_int(message_array.get("m")) # converts the message from JSON to integer message


def send_message(connection: socket, message: int): # sends the message to the user
    message_array = convert_to_array(message) # converts the integer to an array of single integers
    data = json.dumps({"m": message_array}) # hashes the message into a JSON file
    connection.send(data.encode()) # encodes and sends the message


def send_keys_over_socket(connection: socket, n: int, e: int) -> tuple: # sends the keys over the unencrypted channel
    # send the server object
    n_array = convert_to_array(n) # converts n into an array
    e_array = convert_to_array(e) # converts e into an array
    data = json.dumps({"n": n_array, "e": e_array}) # JSON-ifies the arrays and converts them to bytes
    connection.send(data.encode()) # encodes and sends the message to the desired user
    logging.info("User information has been sent!")


def receive_keys_over_socket(connection: socket): # receives the keys from the user
    incoming_data = json.loads(connection.recv(2048).decode()) # decodes the message from the user, and converts from bytes
    user_n = convert_to_int(incoming_data.get('n')) # gets the n value from JSON and converts the array to an int
    user_e = convert_to_int(incoming_data.get('e')) # gets the e value from JSON and converts the array to an int
    logging.info("User information has been received!")
    logging.info("User's public key is: " + str(user_e))
    logging.info("User's n value is " + str(user_n))
    return user_n, user_e # returns the value


def generate_keys(p: int, q: int): # generates / calls the methods to generate phi, e, and d 
    phi = get_phi_of_a_prime(p, q) # gets phi of n
    n = p * q # gets n
    time_to_complete = time.time() # times the completion of finding an e value that works
    e = generate_e(p, q) # method that generates and e value
    time_to_complete = time.time() - time_to_complete 
    logging.info("time to complete e: " + str(time_to_complete))

    time_to_complete = time.time()
    d = find_d(e, get_phi_of_a_prime(p, q)) # finds the d value given e and phi(n)
    time_to_complete = time.time() - time_to_complete
    logging.info("time to complete d: " + str(time_to_complete))
    logging.info("e value: " + str(e))
    logging.info("n value: " + str(n))
    logging.info("d value: " + str(d))
    return n, phi, e, d # returns n, phi(n), public and private keys


def convertNumberToString(number: int) -> str: # given a number, it converts it to a string of letters
    string = ""
    number = str(number) # convert the number to a string
    if len(number) % 2 != 0: # if the length of the string is odd, add a zero to the front
        number = "0" + number
    for i in range(0, len(number), 2): # for every pair of characters
        string += list(letterConversions.keys()
                       )[list(letterConversions.values()).index(number[i:i + 2])] # replace the 2 characters with the letter corresponding with the pair in the dictionary above
    return string # return the converted string


def convertStringToNumber(string: str) -> int: # given a string, converts it to a string of numbers
    number = ""
    string = string.upper() # send the message uppercase
    for i in range(len(string)): # for every character in the string
        number += letterConversions[string[i]] # replace the character with a pair of numbers
    logging.info("Message converted to numbers: " + str(number))
    return int(number) # return the string as an integer
