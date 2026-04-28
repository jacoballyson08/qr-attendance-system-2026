from models import (
    create_user,
    find_user,
    save_attendance,
    get_attendance
)


# REGISTER USER

def register_user(student_id, name, password):
    create_user(student_id, name, password)


# LOGIN USER

def login_user(student_id, password):
    user = find_user(student_id)

    if not user:
        return None

    if user["password"] != password:
        return None

    return user


# SCAN ATTENDANCE

def scan_attendance(student_id):
    user = find_user(student_id)

    if not user:
        return None

    save_attendance(user["student_id"], user["name"])

    return user


# GET RECORDS

def attendance_records():
    return get_attendance()