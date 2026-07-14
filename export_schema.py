import sqlite3

conn = sqlite3.connect("aiapget.db")
cursor = conn.cursor()

cursor.execute("""
SELECT sql
FROM sqlite_master
WHERE type='table'
ORDER BY name;
""")

print("\n========== SQLITE SCHEMA ==========\n")

for row in cursor.fetchall():
    if row[0]:
        print(row[0])
        print()

conn.close()
