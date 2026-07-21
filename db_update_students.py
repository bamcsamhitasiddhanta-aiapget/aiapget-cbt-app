from database import get_connection

conn = get_connection()
cur = conn.cursor()

queries = [
    "ALTER TABLE students ADD COLUMN IF NOT EXISTS is_blocked BOOLEAN DEFAULT FALSE;",
    "ALTER TABLE students ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;",
    "ALTER TABLE students ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;",
    "ALTER TABLE students ADD COLUMN IF NOT EXISTS phone VARCHAR(20);",
]

for q in queries:
    cur.execute(q)

conn.commit()

print("Students table updated successfully.")

cur.close()
conn.close()
