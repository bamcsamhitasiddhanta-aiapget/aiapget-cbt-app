import os
import sqlite3

import psycopg
from dotenv import find_dotenv, load_dotenv
from psycopg.rows import dict_row

from developer_monitor import *

dotenv_path = find_dotenv()

print("DOTENV PATH:", dotenv_path)

loaded = load_dotenv(dotenv_path)

print("DOTENV LOADED:", loaded)
print("DATABASE_TYPE FROM ENV:", os.getenv("DATABASE_TYPE"))
print("DATABASE_URL EXISTS:", os.getenv("DATABASE_URL") is not None)

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "aiapget.db")
DATABASE_URL = os.getenv("DATABASE_URL")


import time


def get_connection():

    increment_connection()

    start = time.perf_counter()

    if DATABASE_TYPE == "postgres":
        conn = psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
        )
    else:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row

    print(f"Connection opened in {time.perf_counter() - start:.4f} sec")

    return conn


def adapt_query(query):
    """
    Convert SQLite placeholders (?) into PostgreSQL placeholders (%s)
    """
    if DATABASE_TYPE == "postgres":
        return query.replace("?", "%s")
    return query


def execute(cursor, query, params=()):

    increment_query()

    query = adapt_query(query)

    return cursor.execute(query, params)
