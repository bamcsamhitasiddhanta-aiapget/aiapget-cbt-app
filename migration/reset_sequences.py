import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

sequences = [
    ("students", "id"),
    ("questions", "id"),
    ("results", "id"),
    ("test_attempts", "attempt_id"),
    ("student_responses", "response_id"),
]

for table, column in sequences:
    cur.execute(f"""
        SELECT setval(
            pg_get_serial_sequence('{table}', '{column}'),
            COALESCE((SELECT MAX({column}) FROM {table}), 1),
            true
        );
    """)

    print(f"✓ {table} sequence updated")

conn.commit()

cur.close()
conn.close()

print("\n🎉 All sequences updated successfully!")
