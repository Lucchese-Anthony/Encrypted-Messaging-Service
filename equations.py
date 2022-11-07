import math
import struct
import socket
import random

letterConversions:dict = {
"A":"01","B":"02","C":"03","D":"04","E":"05",
"F":"06","G":"07","H":"08","I":"09","J":"10",
"K":"11","L":"12","M":"13","N":"14","O":"15",
"P":"16","Q":"17","R":"18","S":"19","T":"20",
"U":"21","V":"22","W":"23","X":"24","Y":"25",
"Z":"26"}


def getPhiOfN(p, q):
    return (p-1)*(q-1)

def generateE(p, q):
    while(True):
        e:int = random.randint(11,100)
        if EuclideanAlgorithm(getPhiOfN(p, q), e) == 1:
            return e

def EuclideanAlgorithm(top:int, bottom:int) -> int:
    if bottom > top:
        temp = bottom
        bottom = top
        top = temp
    sequence = [top, bottom]
    while(sequence[-1] != 0):
        rem = top % bottom
        sequence.append(rem)
        top = bottom
        bottom = rem
    return sequence[-2]

def findExponentModN(number:int, exponent:int, n:int) -> int:
    returnNum:int = 0
    result = bin(exponent)[2:]
    for i in range(len(result)):
        number = (number * number) % n
        if result[i] == "1":
            returnNum = number * number % n
    return returnNum % n

def findD(e:int, phiOfN:int, n:int) -> int:
    return findExponentModN(e, phiOfN-1, n)

def convertNumberToString(number:int) -> str:
    string = ""
    number = str(number)
    if len(number) % 2 != 0:
        number = "0" + number
    for i in range(0, len(number), 2):
        string += list(letterConversions.keys())[list(letterConversions.values()).index(number[i:i+2])]
    return string

def convertStringToNumber(string:str) -> int:
    number = ""
    for i in range(len(string)):
        number += letterConversions[string[i]]
    return int(number)

def decryptMessage(message:str, privateKey:int) -> str:
    return convertNumberToString(findExponentModN(int(message), privateKey))

def encryptMessage(message:str, serverPublicKey:int) -> str:
    return findExponentModN(convertStringToNumber(message), serverPublicKey)

