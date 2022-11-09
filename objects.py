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
    def __init__(self, n:str, e:str):

        self.n = n
        self.e = e
    def getN(self) -> str:
        return self.n
    def getE(self) -> str:
        return self.e