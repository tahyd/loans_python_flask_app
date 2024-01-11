

from models.User import User
from dao.UserDao import *


def createUser(user:User) :
    existingUser = find(user.username)
    print(existingUser)
    if  existingUser :
        raise Exception('User Alread exists')
    if(save(user)):
        return 'User Creation Successfull'
    


def isValidLigin(username,password) :
    isLoginValid = False;
    
    user:User = find(username)
    if (user==None):
       raise Exception("Your details does not match with our database")
    if(user.password==password):
      isLoginValid=True
    return isLoginValid