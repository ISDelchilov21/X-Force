from .db import *

def get_theme_by_title(title:str):
    curr.execute("""SELECT * FROM theme WHERE lower(title) = %s""", (title.lower(),))
    theme = curr.fetchone()

    return theme


def get_theme_by_id(id:int):
    curr.execute("""SELECT * FROM theme WHERE id = %s""", id)
    theme = curr.fetchone()

    return theme


def create_themes( title:str, unique_info:str,  class_id:int, owner_id:int):
    if get_theme_by_title(title):
        return False
    
    curr.execute("""INSERT INTO theme (title, unit_info, classes_id, owner_id) VALUES(%s, %s, %s, %s)""", (title.lower(), unique_info.lower(), class_id, owner_id))
    conn.commit()
    return True



def add_theme_to_class(theme_id:int, class_id:int ):
    curr.execute("""INSERT INTO theme_class (theme_id, class_id) VALUES( %s, %s)""", (theme_id, class_id))
    conn.commit()
    return True


def delete_theme(title:str):
    curr.execute("""DELETE FROM theme WHERE title = %s""", (title.lower()))
    conn.commit()
    return True