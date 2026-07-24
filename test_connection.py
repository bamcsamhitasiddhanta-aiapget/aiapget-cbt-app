from database import get_connection

print("Connecting...")

conn = get_connection()

print("Connected successfully!")

conn.close()

print("Connection closed.")
