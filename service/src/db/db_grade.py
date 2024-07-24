from .db import *

def get_grade_by_id(id:int):
    curr.execute("""SELECT * FROM grades WHERE id = %s""", (id,))
    grade = curr.fetchone()

    return grade


def get_user_grade(user_id:int):
    curr.execute("""SELECT * FROM grades WHERE user_id = %s""", (user_id,))
    grade = curr.fetchall()

    return grade

def get_report(report_id:int):
    curr.execute("""SELECT report FROM grades WHERE report_id = %s""", (report_id,))
    report = curr.fetchone()

    return report

def get_user_report(user_id:int):
    curr.execute("""SELECT report FROM grades WHERE user_id = %s""", (user_id,))
    report = curr.fetchall()

    return report

def create_grade(grade:int, report:str, homework_id:int, user_id:int):
    
    curr.execute("""INSERT INTO grades (grade, report, homework_id, user_id) VALUES(%s, %s, %s, %s)""", (grade, report.lower(), homework_id,  user_id))
    conn.commit()
    return True

def create_statistics(class_id:int):
    curr.execute("""
        SELECT SUM(grades.grade) AS sum_grades,
               AVG(grades.grade) AS average_grade
        FROM grades
        JOIN homework ON grades.homework_id = homework.id
        WHERE homework.class_id = %s
        GROUP BY homework.class_id
    """, (class_id,))
    
    result = curr.fetchone()
    print(f"Debug: Result for class_id {class_id} - {result}")
    
    if result:
        curr.execute("""
            INSERT INTO statistics (class_id, sum_grades, average_grade)
            VALUES (%s, %s, %s)
        """, (class_id, result[0], result[1]))
        conn.commit()
        return True
    else:
        return False
    

def update_grade(grade_id:int, grade:int, report:str, homework_id:int):
    if not get_grade_by_id(grade_id):
        return False
    

    curr.execute("""UPDATE grades SET grade = %s, report = %s, homework_id = %s WHERE id = %s""", (grade, report.lower() ,homework_id, grade_id ))
    conn.commit()
    return True

def get_grade_homework(homework_id:int):
    curr.execute("""SELECT grade FROM grades WHERE homework_id = %s""", (homework_id,))
    grade = curr.fetchall()

    return grade
