import os
import sqlite3

import psycopg
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB = "aiapget.db"
POSTGRES_URL = os.getenv("DATABASE_URL")


sqlite_conn = sqlite3.connect(SQLITE_DB)
sqlite_conn.row_factory = sqlite3.Row

pg_conn = psycopg.connect(POSTGRES_URL)

sqlite_cur = sqlite_conn.cursor()
pg_cur = pg_conn.cursor()
# Clear existing data (child tables first)
print("Clearing existing PostgreSQL data...")

pg_cur.execute("""
TRUNCATE TABLE
    student_responses,
    test_attempts,
    results,
    questions,
    students
RESTART IDENTITY CASCADE;
""")

print("✓ PostgreSQL tables cleared")


def migrate_table(
    table_name,
    columns,
):
    print(f"\nMigrating {table_name}...")

    sqlite_cur.execute(f"SELECT {columns} FROM {table_name}")

    rows = sqlite_cur.fetchall()

    if not rows:
        print("No rows found.")
        return

    placeholders = ",".join(["%s"] * len(rows[0]))

    insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    count = 0

    for row in rows:
        pg_cur.execute(
            insert_sql,
            tuple(row),
        )

        count += 1

    print(f"✓ {count} rows copied")


try:
    pg_conn.autocommit = False

    migrate_table(
        "students",
        "id,name,email,password",
    )

    migrate_table(
        "questions",
        "id,subject,question,option1,option2,option3,option4,answer,explanation,image,question_uid",
    )

    migrate_table(
        "results",
        "id,name,email,subject,score,total,test_date",
    )

    migrate_table(
        "test_attempts",
        """attempt_id,
student_email,
student_name,
subject,
total_questions,
answered,
not_answered,
review,
answered_review,
correct,
wrong,
score,
percentage,
started_at,
submitted_at,
duration_seconds""",
    )

    migrate_table(
        "student_responses",
        """response_id,
attempt_id,
question_uid,
question_no,
subject,
selected_answer,
correct_answer,
is_correct,
review,
visited""",
    )

    pg_conn.commit()

    print("\n🎉 Migration Completed Successfully!")

except Exception as e:
    pg_conn.rollback()

    print("\n❌ Migration Failed")

    print(e)

finally:
    sqlite_conn.close()

    pg_conn.close()
