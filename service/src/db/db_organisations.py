from .db import *


def get_org_by_name(name: str):
    curr.execute(
        """SELECT * FROM organisation WHERE lower(name) = %s""", (name.lower(),)
    )
    org = curr.fetchone()

    return org


def get_org_by_id(id: int):
    curr.execute("""SELECT * FROM organisation WHERE id = %s""", id)
    org = curr.fetchone()

    return org


def get_org_by_code(entry_code: str):
    curr.execute(
        """SELECT * FROM organisation WHERE lower(entry_code) = %s""",
        (entry_code.lower(),),
    )
    org = curr.fetchone()

    return org


def create_org(name: str, entry_code: str, owner_id: int, role: str):
    if get_org_by_name(name):
        return False

    curr.execute(
        """INSERT INTO organisation (name, entry_code, owner_id, user_role) VALUES(%s, %s, %s, %s)""",
        (name.lower(), entry_code, owner_id, role),
    )
    conn.commit()
    return True


def add_user_to_organisation(user_id: int, user_role: str, org_id: int, org_name: str):
    curr.execute(
        """INSERT INTO organisations_users (organisation_id, organisation_name,user_id, user_role) VALUES(%s, %s, %s, %s)""",
        (org_id, org_name, user_id, user_role),
    )
    conn.commit()
    return True


def delete_organisation(name: str):
    curr.execute("""DELETE FROM organisation WHERE name = %s""", (name.lower()))
    conn.commit()
    return True
