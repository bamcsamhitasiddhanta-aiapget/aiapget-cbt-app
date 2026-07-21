from database import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT * FROM students LIMIT 1")

print("Columns:")
print([desc[0] for desc in cur.description])

print("\nFirst Row:")
print(cur.fetchone())

cur.close()
conn.close()
