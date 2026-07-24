import os
import random

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


def get_connection():

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row,
    )


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

    tag_name = tag_name.strip().title()

    execute(
        cur,
        """
        INSERT INTO question_tags
        (question_uid, tag_name)
        VALUES (?, ?)
        ON CONFLICT (question_uid, tag_name) DO NOTHING
        """,
        (question_uid, tag_name),
    )

    conn.commit()
    cur.close()
    conn.close()


def get_question_tags(question_uid):

    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT tag_name
        FROM question_tags
        WHERE question_uid = ?
        ORDER BY tag_name
        """,
        (question_uid,),
    )

    tags = [row["tag_name"] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return tags


def remove_all_question_tags(question_uid):
    conn = get_connection()
    cur = conn.cursor()

    execute(
        cur,
        """
        DELETE FROM question_tags
        WHERE question_uid = ?
        """,
        (question_uid,),
    )
    conn.commit()

    cur.close()
    conn.close()


def get_questions_by_tag(tag_name):
    conn = get_connection()
    cur = conn.cursor()

    execute(
        cur,
        """
        SELECT q.*
        FROM questions q
        JOIN question_tags qt
           ON q.question_uid = qt.question_uid
        WHERE qt.tag_name = ?
        """,
        (tag_name,),
    )

    questions = cur.fetchall()

    cur.close()
    conn.close()

    return questions


def get_all_tags():
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT DISTINCT tag_name
        FROM question_tags
        ORDER BY tag_name
        """,
    )

    tags = [row["tag_name"] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return tags


def remove_question_tag(question_uid, tag_name):

    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        DELETE
        FROM question_tags
        WHERE question_uid = ?
        AND tag_name = ?
        """,
        (question_uid, tag_name),
    )

    conn.commit()
    conn.close()


def get_all_questions():

    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT
            question_uid,
            subject,
            question,
            option1,
            option2,
            option3,
            option4,
            answer,
            explanation,
            image
        FROM questions
        ORDER BY subject
        """,
    )

    rows = cursor.fetchall()

    conn.close()

    questions = []

    for row in rows:
        questions.append(
            {
                "question_uid": row["question_uid"],
                "subject": row["subject"],
                "question": row["question"],
                "options": [
                    row["option1"],
                    row["option2"],
                    row["option3"],
                    row["option4"],
                ],
                "answer": row["answer"],
                "explanation": row["explanation"],
                "image": row["image"],
            }
        )

    return questions


def get_subjects():

    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT DISTINCT subject
        FROM questions
        ORDER BY subject
        """,
    )

    subjects = [row["subject"] for row in cursor.fetchall()]

    conn.close()

    return subjects


def get_questions_by_subject(subject):

    questions = get_all_questions()

    return [q for q in questions if q["subject"] == subject]


def get_mock_questions(limit=100):

    questions = get_all_questions()

    random.shuffle(questions)

    return questions[:limit]


def get_classical_texts():
    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT DISTINCT tag_name
        FROM question_tags
        WHERE tag_name IN (
            'Charaka Samhita',
            'Sushruta Samhita',
            'Ashtanga Hridaya',
            'Ashtanga Sangraha',
            'Madhava Nidana',
            'Bhavaprakasha',
            'Sharangadhara Samhita',
            'Yoga Ratnakara'
        )
        ORDER BY tag_name
        """,
    )

    texts = [row["tag_name"] for row in cursor.fetchall()]

    conn.close()

    return texts


def get_sections(text_name):

    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT DISTINCT qt2.tag_name

        FROM question_tags qt1

        JOIN question_tags qt2
            ON qt1.question_uid = qt2.question_uid

        WHERE qt1.tag_name = ?

        AND qt2.tag_name LIKE '%Sthana'

        ORDER BY qt2.tag_name
        """,
        (text_name,),
    )

    sections = [row["tag_name"] for row in cursor.fetchall()]

    conn.close()

    return sections


def get_questions_by_text_and_section(text_name, section_name):

    conn = get_connection()
    cursor = conn.cursor()

    execute(
        cursor,
        """
        SELECT
            q.question_uid,
            q.subject,
            q.question,
            q.option1,
            q.option2,
            q.option3,
            q.option4,
            q.answer,
            q.explanation,
            q.image

        FROM questions q

        JOIN question_tags qt1
            ON q.question_uid = qt1.question_uid

        JOIN question_tags qt2
            ON q.question_uid = qt2.question_uid

        WHERE
            qt1.tag_name = ?
        AND
            qt2.tag_name = ?

        ORDER BY q.question_uid
        """,
        (text_name, section_name),
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    questions = []

    for row in rows:
        questions.append(
            {
                "question_uid": row["question_uid"],
                "subject": row["subject"],
                "question": row["question"],
                "options": [
                    row["option1"],
                    row["option2"],
                    row["option3"],
                    row["option4"],
                ],
                "answer": row["answer"],
                "explanation": row["explanation"],
                "image": row["image"],
            }
        )

    return questions
