from .db import *
from passlib.hash import bcrypt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def auth_user(username:str, password:str):

    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user

def get_user(username:str):
    curr.execute("""SELECT * FROM users WHERE lower(username) = %s""", (username.lower(),))
    user = curr.fetchone()


    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)




def create_user( email:str, role:str, username:str, password:str):
    if get_user(username):
        return False
    
    hashed_password = bcrypt.hash(password)
    curr.execute("""INSERT INTO users (email, role, username, password) VALUES(%s, %s, %s, %s)""", (email.lower(),role, username.lower(), hashed_password))
    conn.commit()
    return True