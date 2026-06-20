import hashlib
import sqlite3

# Create (or open) the database file
conn = sqlite3.connect("aiapget.db")

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create the students table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT
)
""")

# Save changes
conn.commit()

# Close the connection
conn.close()

print("Database and students table created successfully!")
def login_student(email, password):
    import sqlite3
    import hashlib

    conn = sqlite3.connect("aiapget.db")
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute(
        "SELECT * FROM students WHERE email=? AND password=?",
        (email, hashed_password)
    )

    student = cursor.fetchone()

    conn.close()

    return student
def register_student(name, email, password):
    import sqlite3
    import hashlib

    conn = sqlite3.connect("aiapget.db")
    cursor = conn.cursor()

    # Check if email exists
    cursor.execute(
        "SELECT * FROM students WHERE email=?",
        (email,)
    )

    if cursor.fetchone():
        conn.close()
        return False

    # Hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute(
        "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
        (name, email, hashed_password)
    )

    conn.commit()
    conn.close()

    return True
def save_result(email, subject, score, total):
    import sqlite3

    conn = sqlite3.connect("aiapget.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO results (email, subject, score, total)
        VALUES (?, ?, ?, ?)
        """,
        (email, subject, score, total)
    )

    conn.commit()
    conn.close()
def admin_login(username, password):
    # Temporary hard-coded admin credentials
    return username == "admin" and password == "admin123"
def save_result(email, subject, score, total):
    import sqlite3

    conn = sqlite3.connect("aiapget.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO results (email, subject, score, total)
        VALUES (?, ?, ?, ?)
        """,
        (email, subject, score, total)
    )

    conn.commit()
    conn.close()