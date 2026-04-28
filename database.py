import os
import psycopg2
import mysql.connector
from psycopg2.extras import RealDictCursor


# -----------------------------
# SWITCH MODE
# -----------------------------
USE_CLOUD = True  # True = Supabase | False = XAMPP


# -----------------------------
# LOCAL XAMPP DATABASE (MySQL)
# -----------------------------
LOCAL_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "qr_attendance_db"
}


# -----------------------------
# SUPABASE DATABASE URL
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")


# -----------------------------
# GET DATABASE CONNECTION
# -----------------------------
def get_db():

    if USE_CLOUD:
        # 🌐 SUPABASE POSTGRESQL

        conn = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=RealDictCursor
        )

        return conn

    else:
        # 🏠 LOCAL XAMPP MYSQL

        conn = mysql.connector.connect(
            **LOCAL_DB_CONFIG
        )

        return conn