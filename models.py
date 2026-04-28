from database import get_db
from datetime import datetime, timedelta
# CREATE USER

def create_user(student_id, name, password):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (student_id, name, password)
            VALUES (%s, %s, %s)
        """, (student_id, name, password))

        db.commit()

    except Exception as e:
        db.rollback()
        print("DB ERROR:", e)

    finally:
        db.close()

# FIND USER

def find_user(student_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE student_id=%s",
        (student_id,)
    )

    user = cursor.fetchone()
    db.close()

    return user


# SAVE ATTENDANCE

def save_attendance(student_id, name):
    db = get_db()
    cursor = db.cursor()

    # Philippine time (+8)
    ph_time = datetime.utcnow() + timedelta(hours=8)
    cursor.execute(
        """
        INSERT INTO attendance (student_id, name)
        VALUES (%s, %s)
        """,
        (student_id, name)
    )

    db.commit()
    db.close()


# GET ATTENDANCE

def get_attendance():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM attendance
        WHERE id IN (
            SELECT MAX(id)
            FROM attendance
            GROUP BY student_id
        )
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    db.close()
    return records