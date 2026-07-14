from database import get_connection

try:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()

    print("\n✅ Connected Successfully!\n")
    print(version)

    conn.close()

except Exception as e:
    print("\n❌ Connection Failed\n")
    print(e)
