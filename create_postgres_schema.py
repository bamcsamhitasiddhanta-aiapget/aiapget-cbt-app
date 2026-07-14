from database import get_connection

conn = get_connection()
cur = conn.cursor()

print("Creating PostgreSQL tables...\n")

# -------------------------
# STUDENTS
# -------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

print("✓ students")

# -------------------------
# QUESTIONS
# -------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    subject TEXT NOT NULL,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT,
    image TEXT,
    question_uid TEXT
);
""")

print("✓ questions")

# -------------------------
# RESULTS
# -------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

print("✓ results")

# -------------------------
# TEST ATTEMPTS
# -------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS test_attempts (

    attempt_id SERIAL PRIMARY KEY,

    student_email TEXT,
    student_name TEXT,

    subject TEXT,

    total_questions INTEGER,

    answered INTEGER,
    not_answered INTEGER,

    review INTEGER,
    answered_review INTEGER,

    correct INTEGER,
    wrong INTEGER,

    score DOUBLE PRECISION,
    percentage DOUBLE PRECISION,

    started_at TEXT,
    submitted_at TEXT,

    duration_seconds INTEGER
);
""")

print("✓ test_attempts")

# -------------------------
# STUDENT RESPONSES
# -------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS student_responses (

    response_id SERIAL PRIMARY KEY,

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
);
""")

print("✓ student_responses")

conn.commit()

cur.close()
conn.close()

print("\n🎉 PostgreSQL schema created successfully!")
