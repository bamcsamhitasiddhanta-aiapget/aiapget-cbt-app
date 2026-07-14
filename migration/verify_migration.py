import os
import sqlite3

import psycopg
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB = "aiapget.db"
POSTGRES_URL = os.getenv("DATABASE_URL")

sqlite_conn = sqlite3.connect(SQLITE_DB)
sqlite_cur = sqlite_conn.cursor()

pg_conn = psycopg.connect(POSTGRES_URL)
pg_cur = pg_conn.cursor()

tables = [
    "students",
    "questions",
    "results",
    "test_attempts",
    "student_responses",
]

print("\n========== MIGRATION VERIFICATION ==========\n")

all_ok = True

for table in tables:
    sqlite_cur.execute(f"SELECT COUNT(*) FROM {table}")
    sqlite_count = sqlite_cur.fetchone()[0]

    pg_cur.execute(f"SELECT COUNT(*) FROM {table}")
    postgres_count = pg_cur.fetchone()[0]

    if sqlite_count == postgres_count:
        status = "✅ OK"
    else:
        status = "❌ MISMATCH"
        all_ok = False

    print(
        f"{table:<20} SQLite: {sqlite_count:<6} PostgreSQL: {postgres_count:<6} {status}"
    )

sqlite_conn.close()
pg_conn.close()

print("\n------------------------------------------")

if all_ok:
    print("🎉 ALL TABLES VERIFIED SUCCESSFULLY!")
else:
    print("⚠️ Migration verification failed. Please investigate the mismatched tables.")
