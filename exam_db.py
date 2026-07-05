import sqlite3
from datetime import datetime

DB_NAME = "aiapget.db"
DB_VERSION = 1


def create_exam_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Exam Attempts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_attempts (

        attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_email TEXT,
        student_name TEXT,

        subject TEXT,
        status TEXT,           

        total_questions INTEGER,

        answered INTEGER,
        not_answered INTEGER,

        review INTEGER,
        answered_review INTEGER,

        correct INTEGER,
        wrong INTEGER,

        score REAL,
        percentage REAL,

        started_at TEXT,
        submitted_at TEXT,

        duration_seconds INTEGER
    )
    """)

    # Student Responses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_responses (

        response_id INTEGER PRIMARY KEY AUTOINCREMENT,

        attempt_id INTEGER,

        question_uid TEXT,
        question_no INTEGER,

        subject TEXT,

        selected_answer TEXT,
        correct_answer TEXT,

        is_correct INTEGER,

        review INTEGER,
        visited INTEGER,

        FOREIGN KEY(attempt_id)
        REFERENCES test_attempts(attempt_id)
    )
    """)

    conn.commit()
    conn.close()


DB_NAME = "aiapget.db"


def create_attempt(
    student_email,
    student_name,
    subject,
    total_questions,
    answered,
    not_answered,
    review,
    answered_review,
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO test_attempts
        (
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

            duration_seconds
        )

        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_email,
            student_name,
            subject,
            total_questions,
            answered,
            not_answered,
            review,
            answered_review,
            0,
            0,
            0,
            0,
            datetime.now().isoformat(),
            None,
            0,
        ),
    )

    conn.commit()

    attempt_id = cursor.lastrowid

    conn.close()

    return attempt_id


def save_response(
    attempt_id,
    question_uid,
    question_no,
    subject,
    selected_answer,
    correct_answer,
    is_correct,
    review,
    visited,
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO student_responses
        (
            attempt_id,
            question_uid,
            question_no,
            subject,
            selected_answer,
            correct_answer,
            is_correct,
            review,
            visited
        )

        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            attempt_id,
            question_uid,
            question_no,
            subject,
            selected_answer,
            correct_answer,
            is_correct,
            int(review),
            int(visited),
        ),
    )

    conn.commit()
    conn.close()


def finish_attempt(
    attempt_id,
    answered,
    not_answered,
    correct,
    wrong,
    score,
    percentage,
    duration_seconds,
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE test_attempts
        SET
            answered=?,
            not_answered=?,
            correct=?,
            wrong=?,
            score=?,
            percentage=?,
            submitted_at=?,
            duration_seconds=?
        WHERE attempt_id=?
        """,
        (
            answered,
            not_answered,
            correct,
            wrong,
            score,
            percentage,
            datetime.now().isoformat(),
            duration_seconds,
            attempt_id,
        ),
    )

    conn.commit()
    conn.close()
