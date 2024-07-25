from .db import *


def get_grade_by_id(id: int):
    curr.execute("""SELECT * FROM grades WHERE id = %s""", (id,))
    grade = curr.fetchone()

    return grade


def get_user_grade(user_id: int):
    curr.execute("""SELECT * FROM grades WHERE user_id = %s""", (user_id,))
    grade = curr.fetchall()

    return grade


def get_report(report_id: int):
    curr.execute("""SELECT report FROM grades WHERE report_id = %s""", (report_id,))
    report = curr.fetchone()

    return report


def get_user_report(user_id: int):
    curr.execute("""SELECT report FROM grades WHERE user_id = %s""", (user_id,))
    report = curr.fetchall()

    return report


def create_grade(grade: int, report: str, homework_id: int, user_id: int):

    curr.execute(
        """INSERT INTO grades (grade, report, homework_id, user_id) VALUES(%s, %s, %s, %s)""",
        (grade, report.lower(), homework_id, user_id),
    )
    conn.commit()
    return True


def create_statistics(class_id: int):
    try:

        curr.execute(
            """
            SELECT COUNT(g.grade) AS sum_grades,
                   AVG(g.grade) AS average_grade
            FROM grades g
            JOIN homeworks h ON g.homework_id = h.id
            WHERE h.class_id = %s
            GROUP BY h.class_id
        """,
            (class_id,),
        )

        result = curr.fetchone()
        print(f"Debug: Result for class_id {class_id} - {result}")

        if result:
            sum_grades = result["sum_grades"] if result["sum_grades"] is not None else 0
            average_grade = (
                float(result["average_grade"])
                if result["average_grade"] is not None
                else 0.0
            )
            curr.execute(
                """
                INSERT INTO statistics (class_id, sum_grades, average_grade)
                VALUES (%s, %s, %s)
                ON CONFLICT (class_id) 
                DO UPDATE SET sum_grades = EXCLUDED.sum_grades, average_grade = EXCLUDED.average_grade
            """,
                (class_id, sum_grades, average_grade),
            )
            conn.commit()
            return True
        else:
            print(f"No statistics found for class_id {class_id}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return False


def update_grade(grade_id: int, grade: int, report: str, homework_id: int):
    if not get_grade_by_id(grade_id):
        return False

    curr.execute(
        """UPDATE grades SET grade = %s, report = %s, homework_id = %s WHERE id = %s""",
        (grade, report.lower(), homework_id, grade_id),
    )
    conn.commit()
    return True


def get_grade_homework(homework_id: int):
    curr.execute("""SELECT grade FROM grades WHERE homework_id = %s""", (homework_id,))
    grade = curr.fetchall()

    return grade
