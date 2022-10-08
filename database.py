import math
from objects import message
from objects import user

def insertUser(username:str, password:str):
    # TODO insert new user
    # TODO create a public key for the user and send it to their session
    return
def queryUser(username:str, password:str):
    # TODO check if username and password is correct
    return
def storeMessage(message:message):
    # TODO query message database for all messages from sender to sender and return the first 10
    return
def queryUsername(username:str):
    # TODO query IF user exists
    '''
    IF DATABASE_PRINCIPAL_ID('IIS APPPOOL\MyWebApi AppPool') IS NULL
BEGIN
    CREATE USER [IIS APPPOOL\MyWebApi AppPool] 
    FOR LOGIN [IIS APPPOOL\MyWebApi AppPool] WITH DEFAULT_SCHEMA=[dbo]
END
ALTER ROLE [db_owner] ADD MEMBER [IIS APPPOOL\MyWebApi AppPool]
GO
'''
    return