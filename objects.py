import math

class message:
    def __init__(self, fromUser:str, toUser:str, message:str):
        self._fromUser = fromUser
        self._toUser = toUser
        self._message = message
    def getMessage():
        return self._message
    def getFromUser():
        return self._fromUser
    def getToUser():
        return self._toUser
    def setMesage(newMessage:str):
        self._message = newMessage
class user:
    def __init__(self, username:str, password:str, n, e):
        self._username = username
        self._password = password
        self.n = n
        self.e = e
    def getUsername(self):
        return self._username
    def getN(self):
        return self.n
    def getE(self):
        return self.e