import math
import random
import sys

letterConversions:dict = {
"A":"01","B":"02","C":"03","D":"04","E":"05",
"F":"06","G":"07","H":"08","I":"09","J":"10",
"K":"11","L":"12","M":"13","N":"14","O":"15",
"P":"16","Q":"17","R":"18","S":"19","T":"20",
"U":"21","V":"22","W":"23","X":"24","Y":"25",
"Z":"26", " ":"27", ".":"28", ",":"29", "?":"30", 
"!":"31", "'":"32", '"':"33", "(":"34", ")":"35",
"[":"36", "]":"37", "{":"38", "}":"39", "<":"40",
">":"41", "/":"42", "\\":"43", ":":"44", ";":"45",
"@":"46", "#":"47", "$":"48", "%":"49", "^":"50",
"&":"51", "*":"52", "+":"53", "-":"54", "_":"55",
"=":"56", "`":"57", "~":"58", "0":"59", "1":"60",
"2":"61", "3":"62", "4":"63", "5":"64", "6":"65",
"7":"66", "8":"67", "9":"68"
}


def getPhiOfN(p, q):
    return (p-1)*(q-1)

def generateE(p, q):
    while(True):
        e:int = random.randint(10**(3), 10**(4))
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
    returnNum:int = 1
    result = (bin(exponent)[2:])[::-1]
    temp = number % n
    print(result)
    print(len(result))
    for i in range(0, len(result)):
        if i != 0:
            temp = (temp * temp) % n
            print(temp)
        if result[i] == '1':
            returnNum = (returnNum * temp) % n
    return returnNum

def findD(e:int, phiOfN:int, n:int) -> int:
    return findExponentModN(e, phiOfN-1, n)

def convertNumberToString(number:int) -> str:
    string = ""
    number = str(number)
    if len(number) % 2 != 0:
        number = "0" + number
    for i in range(0, len(number), 2):
        print(i)
        string += list(letterConversions.keys())[list(letterConversions.values()).index(number[i:i+2])]
    return string

def convertStringToNumber(string:str) -> int:
    number = ""
    for i in range(len(string)):
        number += letterConversions[string[i]]
    return int(number)

def shrinkIntToSendOverSocket(number:int):
    return (str(math.floor(number / sys.maxsize)), str(number % sys.maxsize))

def decryptMessage(message:str, privateKey:int, n:int) -> str:
    return convertNumberToString(message**privateKey % n)
    # return convertNumberToString(findExponentModN(int(message), privateKey, n))

def encryptMessage(message:str, serverPublicKey:int, n:int) -> str:
    return findExponentModN(convertStringToNumber(message), serverPublicKey, n)

