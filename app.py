import os
import time

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

import admin
import db_utils
import exam_db
import student_test
from db_utils import login_student, register_student

print(student_test.__file__)


st.set_page_config(page_title="AIAPGET CBT", layout="wide")

exam_db.create_exam_tables()
# Login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
st.markdown(
    """
<style>
div.stButton > button {
    width: 100%;
    padding: 4px;
    font-size: 11px;
}
</style>
""",
    unsafe_allow_html=True,
)
# ================= LOGIN / REGISTER =================

if not st.session_state.logged_in:
    st.title("🧠 AIAPGET CBT Login")

    tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "👨‍💼 Admin"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            student = login_student(email, password)

            if student:
                st.session_state.logged_in = True
                st.session_state.student_email = student[2]  # email
                st.session_state.student_name = student[1]  # name
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid email or password")

    with tab2:
        name = st.text_input("Full Name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register"):
            if register_student(name, reg_email, reg_password):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Email already registered.")
    with tab3:
        admin_user = st.text_input("Admin Username", key="admin_user")

        admin_pass = st.text_input("Admin Password", type="password", key="admin_pass")

        if st.button("Admin Login", key="admin_login_btn"):
            if admin_user == "admin" and admin_pass == "admin123":
                st.session_state.logged_in = True
                st.session_state.is_admin = True
                st.success("Admin login successful!")
                st.rerun()
            else:
                st.error("Invalid admin credentials")
    st.stop()


if st.session_state.get("is_admin", False):
    admin.show_admin_dashboard()
    st.stop()

# ====================================================
# Load questions from folder

import sqlite3

conn = sqlite3.connect("aiapget.db")
cursor = conn.cursor()

cursor.execute("""
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
""")

rows = cursor.fetchall()
conn.close()

questions = []

for row in rows:
    questions.append(
        {
            "question_uid": row[0],
            "subject": row[1],
            "question": row[2],
            "options": [row[3], row[4], row[5], row[6]],
            "answer": row[7],
            "explanation": row[8],
            "image": row[9],
        }
    )
# Get unique subjects
subjects = sorted(list(set(q["subject"] for q in questions)))

subjects.insert(0, "Select Subject")

subjects.append("Full Mock Test")
# Single selectbox ONLY
import random

selected_subject = st.selectbox(
    "Select Subject",
    subjects,
    key="subject_select",
    disabled=st.session_state.get("test_state", "home") != "home",
)
# Reset test state when subject changes
if "last_subject" not in st.session_state:
    st.session_state.last_subject = selected_subject

if st.session_state.last_subject != selected_subject:
    st.session_state.last_subject = selected_subject

    st.session_state.start_time = None
    st.session_state.submitted = False
    st.session_state.answers = {}
    st.session_state.review = {}
    st.session_state.current_q = 0
    st.session_state.result_saved = False

    # Reset mock questions if needed
    if selected_subject != "Full Mock Test":
        st.session_state.mock_questions = None

    st.rerun()

# Filter logic
if selected_subject == "Full Mock Test":
    if (
        "mock_questions" not in st.session_state
        or st.session_state.mock_questions is None
    ):
        temp = questions.copy()
        random.shuffle(temp)
        st.session_state.mock_questions = temp[:100]

    questions = st.session_state.mock_questions

else:
    questions = [q for q in questions if q["subject"] == selected_subject]
    st.session_state.mock_questions = None


student_test.show_test(
    questions=questions,
    selected_subject=selected_subject,
    student_name=st.session_state.student_name,
    student_email=st.session_state.student_email,
)

st.stop()
st.title("🧠 AIAPGET CBT Practice Test")
# Session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "review" not in st.session_state:
    st.session_state.review = {}
if "review" not in st.session_state:
    st.session_state.review = {}
if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

# Start screen
if not st.session_state.get("test_started", False):
    st.write("### Instructions:")
    st.write("- Total Questions:", len(questions))
    st.write("- Time: 10 minutes (demo)")
    st.write("- Do not refresh during test")

    if st.button("🚀 Start Test"):
        st.session_state.test_started = True
        st.session_state.start_time = time.time()
        st.session_state.current_q = 0

        st.rerun()
# Refresh page every second
if st.session_state.start_time is not None and not st.session_state.submitted:
    st_autorefresh(interval=1000, key="timer_refresh")
# Timer
# Different timer for mock vs subject
if selected_subject == "Full Mock Test":
    TOTAL_TIME = 7200  # 2 hours
else:
    TOTAL_TIME = 1800  # 30 minutes
if st.session_state.start_time is None:
    st.stop()

elapsed = time.time() - st.session_state.start_time
remaining = int(TOTAL_TIME - elapsed)

if remaining <= 0:
    st.session_state.submitted = True
    st.warning("⏰ Time Up! Auto Submitted")
    st.session_state.test_started = False
    st.session_state.start_time = None

mins = remaining // 60
secs = remaining % 60
# Timer display with warning
timer_placeholder = st.empty()

if remaining <= 300:
    timer_placeholder.markdown(
        f"<h2 style='color:red;'>⏳ Time Left: {mins}:{secs:02d}</h2>",
        unsafe_allow_html=True,
    )
    st.warning("⚠️ Only 5 minutes left!")
else:
    timer_placeholder.markdown(f"## ⏳ Time Left: {mins}:{secs:02d}")

if remaining <= 60:
    st.error("🚨 Last 1 minute!")
# Layout
col1 = st.container()

# adjust for smaller screens manually

if not st.session_state.submitted:
    # Default question index
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0

    # Show current question
    q = questions[st.session_state.current_q]

    with col1:
        # Question number
        st.markdown(f"### Q{st.session_state.current_q + 1}")

    # Question text
    question_text = q["question"].replace("\n", " ").strip()
    st.markdown(question_text)
    # Display Question Image
    if q.get("image"):
        if os.path.exists(q["image"]):
            st.image(
                q["image"],
                width=450,
            )

    # Options
    options = [opt.replace("\n", " ").strip() for opt in q["options"]]

    # Radio
    current_key = f"q_{st.session_state.current_q}"

choice = st.radio(
    "",
    options,
    index=None,  # 🔥 IMPORTANT
    key=current_key,
    label_visibility="collapsed",
)
# Mark for Review (toggle button)
if st.button("⭐ Mark / Unmark Review"):
    if st.session_state.current_q in st.session_state.review:
        del st.session_state.review[st.session_state.current_q]
    else:
        st.session_state.review[st.session_state.current_q] = True

# Show review status
if st.session_state.current_q in st.session_state.review:
    st.info("Marked for Review ⭐")
# Save answer only when user interacts
if choice is not None:
    st.session_state.answers[st.session_state.current_q] = choice

# Navigation buttons (FINAL FIX)
col_prev, col_next = st.columns(2)

with col_prev:
    if st.button("⬅ Previous"):
        if st.session_state.current_q > 0:
            st.session_state.current_q -= 1
            st.rerun()

with col_next:
    if st.button("Next ➡"):
        if st.session_state.current_q < len(questions) - 1:
            st.session_state.current_q += 1
            st.rerun()
# Floating palette (FINAL FIXED)
st.markdown("---")
st.markdown("### Questions")

num_cols = 5  # better layout

rows = (len(questions) + num_cols - 1) // num_cols

for r in range(rows):
    cols = st.columns(num_cols)

    for c in range(num_cols):
        q_index = r * num_cols + c

        if q_index < len(questions):
            # ✅ Color logic (INSIDE block)
            if q_index in st.session_state.review:
                label = f"🟨 {q_index + 1}"
            elif (
                q_index in st.session_state.answers
                and st.session_state.answers.get(q_index) is not None
            ):
                label = f"🟩 {q_index + 1}"
            else:
                label = f"🟥 {q_index + 1}"

            # ✅ Button also INSIDE
            if cols[c].button(label, key=f"nav{q_index}"):
                st.session_state.current_q = q_index
                st.rerun()
                st.markdown("---")
st.subheader("📋 Test Summary")

answered = len(st.session_state.answers)
reviewed = len(st.session_state.review)

# Questions marked for review are still counted as answered if an answer was selected
not_answered = len(questions) - answered

col1, col2, col3 = st.columns(3)

with col1:
    st.success(f"🟩 Answered: {answered}")

with col2:
    st.warning(f"🟨 Review: {reviewed}")

with col3:
    st.error(f"🟥 Not Answered: {not_answered}")
    # Submit
confirm_submit = st.checkbox("✅ I have reviewed my answers and want to submit.")

if confirm_submit and st.button("🚀 Submit Test"):
    st.session_state.submitted = True

    st.session_state.test_started = False

    st.session_state.start_time = None
if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

if st.session_state.submitted:
    st.subheader("📊 Results")

    score = 0

    for i, q in enumerate(questions):
        user_ans = st.session_state.answers.get(i)
        correct = q["answer"]

        if user_ans == correct:
            score += 1
            st.success(f"Q{i + 1}: Correct")
        else:
            st.error(f"Q{i + 1}: Wrong")

        st.write(f"Your Answer: {user_ans}")
        st.write(f"Correct Answer: {correct}")
        st.info(f"Explanation: {q['explanation']}")
        st.write("---")

    st.write(f"## 🎯 Score: {score} / {len(questions)}")

    if not st.session_state.result_saved:
        db_utils.save_result(
            st.session_state.student_name,
            st.session_state.student_email,
            selected_subject,
            score,
            len(questions),
        )
        st.session_state.result_saved = True


if "show_leaderboard" not in st.session_state:
    st.session_state.show_leaderboard = False

if st.button("📋 My Test History"):
    import sqlite3

    conn = sqlite3.connect("aiapget.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT subject, score, total, test_date
        FROM results
        WHERE email = ?
        ORDER BY test_date DESC
        """,
        (st.session_state.student_email,),
    )

    history = cursor.fetchall()
    conn.close()

    st.subheader("📋 My Test History")

    if history:
        history_df = pd.DataFrame(
            history, columns=["Subject", "Score", "Total", "Date"]
        )
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No test history found.")
if "show_leaderboard" not in st.session_state:
    st.session_state.show_leaderboard = False

if st.button("🏆 Show Leaderboard"):
    st.session_state.show_leaderboard = True

if st.session_state.show_leaderboard:
    import sqlite3

    conn = sqlite3.connect("aiapget.db")

    query = """
    SELECT
        name AS Student,
        subject AS Subject,
        score AS Score,
        total AS Total,
        ROUND(score * 100.0 / total, 2) AS Percentage,
        test_date AS Date
    FROM results
    ORDER BY Percentage DESC, Score DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    st.subheader("🏆 Leaderboard")

    if df.empty:
        st.info("No results available yet.")
    else:
        st.dataframe(df, use_container_width=True)

