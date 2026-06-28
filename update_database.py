import sqlite3

conn = sqlite3.connect("aiapget.db")
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
