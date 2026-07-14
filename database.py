import os
import sqlite3

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "aiapget.db")
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():

    if DATABASE_TYPE == "postgres":
        conn = psycopg.connect(
            DATABASE_URL,
            row_factory=psycopg.rows.dict_row,
        )

        return conn

    else:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row

        return conn
