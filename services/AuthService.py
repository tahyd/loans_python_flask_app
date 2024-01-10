from models.User import User
from dao.UserDao import *
from flask_jwt_extended import create_access_token

def getToken(username,password):
    user:User = find(username);
    if user is None :
        raise Exception('User details not fount')
    if user.password != password :
        raise Exception("Invalid credentials ")
    token = create_access_token(identity=username)
    return token 
     
