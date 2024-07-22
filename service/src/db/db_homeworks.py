from .db import *


def get_homework_by_id(id:int):
    curr.execute("""SELECT * FROM homeworks WHERE id = %s""", (id,))
    classes = curr.fetchone()

    return classes

def get_homework_by_title(title:str):
    curr.execute("""SELECT * FROM homeworks WHERE title = %s""", (title.lower(),))
    classes = curr.fetchone()

    return classes

def get_homeworks():
    curr.execute("""SELECT * FROM homeworks """)
    classes = curr.fetchall()

    return classes


def get_homeworks_in_class(class_id:int):
    curr.execute("""SELECT * FROM homeworks WHERE class_id = %s""", (class_id,))
    classes = curr.fetchall()

    return classes

def get_user_homework(user_id:int):
    curr.execute("""SELECT * FROM user_homeworks WHERE user_id = %s""", (user_id,))
    classes = curr.fetchall()

    return classes


def create_homework(title:str, type_homework:str, info:str, class_id:int):
    if get_homework_by_title(title):
        return False
    
    curr.execute("""INSERT INTO homeworks (title, type_of_homework, homework_info, class_id) VALUES(%s, %s, %s, %s)""", (title.lower(), type_homework.lower(), info.lower(), class_id))
    conn.commit()
    return True


def add_homework_to_class( class_id:int, homework_id:int ):
    curr.execute("""INSERT INTO classes_homeworks (class_id, homework_id) VALUES(%s, %s)""", (class_id, homework_id))
    conn.commit()
    return True

def add_homework_to_user(user_id:int, homework_id:int,  ):
    curr.execute("""INSERT INTO user_homeworks (user_id, homework_id) VALUES(%s, %s)""", (user_id, homework_id))
    conn.commit()
    return True

def add_homework_attachment(homework_id:str, user_id:int, text_info:str, link:str):
    curr.execute("""INSERT INTO homework_attachment (user_id, homework_id, text_info, link) VALUES(%s, %s, %s, %s)""", (user_id, homework_id, text_info, link))
    conn.commit()
    return True

def update_homework(title:str, type_homework:str, info:str, class_id:str, homework_id:int):
    if not get_homework_by_id(homework_id):
        return False
    

    curr.execute("""UPDATE homeworks SET title = %s, homework_info = %s, type_of_homework = %s, class_id= %s WHERE id = %s""", (title.lower(), info.lower() ,type_homework.lower(), class_id, homework_id ))
    conn.commit()
    return True


def delete_homework_by_title(title:str):
    curr.execute("""DELETE FROM homewroks WHERE title = %s""", (title.lower()))
    conn.commit()
    return True

def delete_homework_by_id(id:int):
    curr.execute("""DELETE FROM homewroks WHERE id = %s""", (id,))
    conn.commit()
    return True