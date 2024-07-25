from .db import *
from passlib.hash import bcrypt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def auth_user(username: str, password: str):

    user = get_user_by_username(username)
    if not user:
        print(f"Atesh{user}")
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def get_user_by_username(username: str):
    curr.execute(
        """SELECT * FROM users WHERE lower(username) = %s""", (username.lower(),)
    )
    user = curr.fetchone()

    return user


def get_user_by_id(id: int):
    curr.execute("""SELECT * FROM users WHERE id =%s""", (id,))
    user = curr.fetchone()

    return user


def get_users():
    curr.execute("""SELECT * FROM users""")
    users = curr.fetchall()

    return users


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_user(email: str, role: str, username: str, password: str):
    if get_user_by_username(username):
        return False

    hashed_password = bcrypt.hash(password)
    curr.execute(
        """INSERT INTO users (email, role, username, password) VALUES(%s, %s, %s, %s)""",
        (email.lower(), role, username.lower(), hashed_password),
    )
    conn.commit()
    return True


def update_user(email: str, role: str, username: str, password: str, user_id: int):
    if not get_user_by_id(user_id):
        return False

    hashed_password = bcrypt.hash(password)

    curr.execute(
        """UPDATE users SET email = %s, role= %s, username= %s, password= %s WHERE id = %s""",
        (email.lower(), role, username.lower(), hashed_password, user_id),
    )
    conn.commit()
    return True


def delete_user(id: int):
    curr.execute("""DELETE FROM users WHERE id = %s""", (id,))
    conn.commit()
    return True
