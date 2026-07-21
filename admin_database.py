from database import get_connection


def get_all_students():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            email,
            phone,
            is_blocked,
            created_at,
            last_login
        FROM students
        ORDER BY id
    """)

    students = cur.fetchall()

    cur.close()
    conn.close()

    return students
