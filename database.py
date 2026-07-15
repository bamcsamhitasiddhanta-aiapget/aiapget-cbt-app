import os
import sqlite3

import psycopg
from dotenv import find_dotenv, load_dotenv
from psycopg.rows import dict_row

dotenv_path = find_dotenv()

print("DOTENV PATH:", dotenv_path)

loaded = load_dotenv(dotenv_path)

print("DOTENV LOADED:", loaded)
print("DATABASE_TYPE FROM ENV:", os.getenv("DATABASE_TYPE"))
print("DATABASE_URL EXISTS:", os.getenv("DATABASE_URL") is not None)

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "aiapget.db")
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():

    print("DATABASE_TYPE =", DATABASE_TYPE)
    print("DATABASE_URL =", DATABASE_URL[:30] + "..." if DATABASE_URL else "None")

    if DATABASE_TYPE == "postgres":
        print("CONNECTING TO POSTGRES")
        return psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
        )

    print("CONNECTING TO SQLITE")

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def adapt_query(query):
    """
    Convert SQLite placeholders (?) into PostgreSQL placeholders (%s)
    """
    if DATABASE_TYPE == "postgres":
        return query.replace("?", "%s")
    return query


def execute(cursor, query, params=()):
    query = adapt_query(query)
    return cursor.execute(query, params)
