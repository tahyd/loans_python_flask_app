

from flask import Blueprint, Flask

import mysql.connector

from models.User import User


#connection = mysql.connector.connect(host='localhost',user='root',password='root',database="flaskdb",port=3306)

connection = mysql.connector.connect(host='loans-flask-db.cra2cuaw4rxi.us-east-1.rds.amazonaws.com',user='root',password='Maddela12345',database="flaskdb",port=3306)
def createUserTable():
    cursor = connection.cursor();
    cursor.execute('''drop table if exists user_tbl''')
    cursor.execute('''CREATE TABLE user_tbl(userid int primary key auto_increment,fullname varchar(200),email varchar(200),username varchar(20) unique,password varchar(20))''')

def save(user:User):
    isUserCreated = False
    cursor =connection.cursor()
    cursor.execute(''' insert into user_tbl(fullname,email,username,password) values(%s,%s,%s,%s)''',(user.fullname,user.email,user.username,user.password))
    
    
    connection.commit();

    if(cursor.rowcount >= 1):
         isUserCreated=True
           
    cursor.close();
    return isUserCreated

def find(username):
     cursor =connection.cursor()
     cursor.execute(''' select * from user_tbl where username=%s ''',[(username)])
     result = cursor.fetchone()
     if cursor.rowcount==1 :
      return User(result[1],result[2],result[3],result[4]);
     else :
         return None;