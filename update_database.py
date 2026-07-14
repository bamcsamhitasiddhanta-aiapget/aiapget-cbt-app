import sqlite3

from database import get_connection

conn = get_connection()
cursor = conn.cursor()
try:
    cursor.execute("""
        ALTER TABLE questions
        ADD COLUMN image TEXT
    """)
    print("✅ Image column added successfully.")
except sqlite3.OperationalError as e:
    print(e)

conn.commit()
conn.close()
