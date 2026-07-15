import hashlib
import os
import shutil
from datetime import datetime

from database import (
    execute,
    get_connection,
)

# Create (or open) the database file
# conn = get_connection()

# Create a cursor to execute SQL commands
# cursor = conn.cursor()

# Create the students table if it doesn't exist
# execute(
# cursor,
# """
# CREATE TABLE IF NOT EXISTS students (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# name TEXT NOT NULL,
# email TEXT UNIQUE NOT NULL,
# password TEXT NOT NULL
# )
# """,
# )
# execute(
# cursor,
# """
# CREATE TABLE IF NOT EXISTS results (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# name TEXT NOT NULL,
# email TEXT NOT NULL,
# subject TEXT NOT NULL,
# score INTEGER NOT NULL,
# total INTEGER NOT NULL,
# test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# )
# """,
# )
# execute(
# cursor,
##CREATE TABLE IF NOT EXISTS questions (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# subject TEXT NOT NULL,
# question TEXT NOT NULL,
# option1 TEXT NOT NULL,
# option2 TEXT NOT NULL,
# option3 TEXT NOT NULL,
# option4 TEXT NOT NULL,
# answer TEXT NOT NULL,
# explanation TEXT
# )
# """,
# )

# Save changes
# conn.commit()

# Close the connection
# conn.close()

print("Database and students table created successfully!")


def login_student(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    execute(
        cursor,
        "SELECT * FROM students WHERE email=? AND password=?",
        (email, hashed_password),
    )

    student = cursor.fetchone()

    conn.close()

    return student


def register_student(name, email, password):

    conn = get_connection()

    cursor = conn.cursor()

    # Check if email exists
    execute(
        cursor,
        "SELECT * FROM students WHERE email=?",
        (email,),
    )
    if cursor.fetchone():
        conn.close()
        return False

    # Hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    execute(
        cursor,
        "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
        (name, email, hashed_password),
    )

    conn.commit()
    conn.close()

    return True


def admin_login(username, password):
    # Temporary hard-coded admin credentials
    return username == "admin" and password == "admin123"


def save_result(name, email, subject, score, total):

    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        INSERT INTO results
        (name, email, subject, score, total)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, subject, score, total),
    )

    conn.commit()
    conn.close()


def backup_database():

    os.makedirs("backup", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_file = f"backup/aiapget_{timestamp}.db"

    shutil.copy2(
        "aiapget.db",
        backup_file,
    )

    return backup_file
