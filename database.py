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

    # increment_connection()

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

    # increment_query()

    query = adapt_query(query)

    return cursor.execute(query, params)


def add_question_tag(question_uid, tag_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO question_tags (question_uid, tag_name)
        VALUES (%s, %s)
        ON CONFLICT (question_uid, tag_name) DO NOTHING
        """,
        (question_uid, tag_name),
    )

    conn.commit()
    cur.close()
    conn.close()


def get_question_tags(question_uid):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT tag_name
        FROM question_tags
        WHERE question_uid = %s
        ORDER BY tag_name
        """,
        (question_uid,),
    )

    tags = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return tags


def remove_question_tags(question_uid):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM question_tags
        WHERE question_uid = %s
        """,
        (question_uid,),
    )

    conn.commit()

    cur.close()
    conn.close()


def get_questions_by_tag(tag_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT q.*
        FROM questions q
        JOIN question_tags qt
            ON q.question_uid = qt.question_uid
        WHERE qt.tag_name = %s
        """,
        (tag_name,),
    )

    questions = cur.fetchall()

    cur.close()
    conn.close()

    return questions


def add_question_tag(question_uid, tag_name):
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        INSERT INTO question_tags
        (question_uid, tag_name)
        VALUES (?, ?)
        ON CONFLICT (question_uid, tag_name) DO NOTHING
        """,
        (question_uid, tag_name),
    )

    conn.commit()
    conn.close()
