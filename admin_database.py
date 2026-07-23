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


from database import execute


def block_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        "UPDATE students SET is_blocked = TRUE WHERE id = ?",
        (student_id,),
    )

    conn.commit()
    conn.close()


def unblock_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        "UPDATE students SET is_blocked = FALSE WHERE id = ?",
        (student_id,),
    )

    conn.commit()
    conn.close()


def get_maintenance_mode():
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT setting_value
        FROM system_settings
        WHERE setting_name=?
        """,
        ("maintenance_mode",),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return False

    try:
        return row["setting_value"].lower() == "true"
    except Exception:
        return row[0].lower() == "true"


def set_maintenance_mode(enabled):
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        UPDATE system_settings
        SET setting_value=?
        WHERE setting_name='maintenance_mode'
        """,
        ("true" if enabled else "false",),
    )

    conn.commit()
    conn.close()


def get_registration_enabled():
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT setting_value
        FROM system_settings
        WHERE setting_name=?
        """,
        ("registration_enabled",),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return True

    try:
        return row["setting_value"].lower() == "true"
    except Exception:
        return row[0].lower() == "true"


def set_registration_enabled(enabled):
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        UPDATE system_settings
        SET setting_value=?
        WHERE setting_name='registration_enabled'
        """,
        ("true" if enabled else "false",),
    )

    conn.commit()
    conn.close()
