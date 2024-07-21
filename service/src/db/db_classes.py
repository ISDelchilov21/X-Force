from .db import *



def get_class_by_name(name:str):
    curr.execute("""SELECT * FROM classes WHERE lower(name) = %s""", (name.lower(),))
    classes = curr.fetchone()

    return classes

def get_class_by_subject(subject:str):
    curr.execute("""SELECT * FROM classes WHERE lower(subject) = %s""", (subject.lower(),))
    classes = curr.fetchone()

    return classes

def get_class_by_id(id:int):
    curr.execute("""SELECT * FROM classes WHERE id = %s""", (id,))
    classes = curr.fetchone()

    return classes

def get_class_by_code(entry_code:str):
    curr.execute("""SELECT * FROM classes WHERE lower(entry_code) = %s""", (entry_code.lower(),))
    classes = curr.fetchone()

    return classes



def create_class( name:str, subject:str, entry_code:str,  org_id:int, owner_id:int):
    if get_class_by_name(name):
        return False
    
    curr.execute("""INSERT INTO classes (name, subject, entry_code, org_id, owner_id) VALUES(%s, %s, %s, %s, %s)""", (name.lower(), subject.lower(), entry_code, org_id, owner_id))
    conn.commit()
    return True



def add_user_to_class(user_id:int, user_role:str, class_id:int, class_name:str, class_subject:str ):
    curr.execute("""INSERT INTO users_classes (class_id, class_name, class_subject, user_id, user_role) VALUES(%s, %s, %s, %s, %s)""", (class_id, class_name, class_subject, user_id, user_role))
    conn.commit()
    return True

def add_class_to_organisation(organisation_id:int, class_id:int):
    curr.execute("""INSERT INTO organisations_classes (organisation_id, class_id) VALUES(%s, %s)""", (organisation_id, class_id ))
    conn.commit()
    return True

def get_classes():
    curr.execute("""SELECT * FROM classes """)
    classes = curr.fetchall()

    return classes

def get_students_in_class(class_id:int):
    curr.execute("""SELECT user_id FROM users_classes WHERE class_id = %s AND user_role = 'student' """, (class_id,))
    classes = curr.fetchall()

    return classes

def get_teachers_in_class(class_id:int):
    curr.execute("""SELECT user_id FROM users_classes WHERE class_id = %s AND user_role = 'teacher' """, (class_id,))
    classes = curr.fetchall()

    return classes


def delete_students(user_id:int, class_id:int):
    curr.execute("""DELETE FROM users_classes WHERE user_id = %s AND class_id = %s AND user_role = 'student'""", (user_id, class_id))
    conn.commit()
    return True

def delete_teachers(user_id:int, class_id:int):
    curr.execute("""DELETE FROM users_classes WHERE user_id = %s AND class_id = %s AND user_role = 'teacher'""", (user_id, class_id))
    conn.commit()
    return True

def delete_class(name:str):
    curr.execute("""DELETE FROM classess WHERE name = %s""", (name.lower()))
    conn.commit()
    return True