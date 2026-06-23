import sqlite3

conn = sqlite3.connect("aiapget.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM questions")
count = cursor.fetchone()[0]

print("Total questions in database:", count)

conn.close()