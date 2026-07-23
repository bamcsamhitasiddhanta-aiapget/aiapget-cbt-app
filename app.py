import streamlit as st
from dotenv import find_dotenv, load_dotenv

import admin
import student_test
from admin_database import get_maintenance_mode, get_registration_enabled
from database import get_connection
from db_utils import admin_login, login_student, register_student
from developer_monitor import *

dotenv_path = find_dotenv()


load_dotenv(dotenv_path, override=True)


print(student_test.__file__)


st.set_page_config(
    page_title="AIAPGET CBT",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from theme import apply_theme

apply_theme()
# exam_db.create_exam_tables()
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

reset_monitor()
start_page_timer()

if not st.session_state.logged_in:
    st.title("🧠 AIAPGET CBT Login")

    tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "👨‍💼 Admin"])

    with tab1:
        maintenance = get_maintenance_mode()

        if maintenance:
            st.warning("🚧 Scheduled Maintenance")

            st.info(
                """
                The AIAPGET CBT Platform is currently undergoing scheduled maintenance.

                Student login is temporarily disabled.

                Please try again later.
                """
            )

        email = st.text_input(
            "Email",
            key="login_email",
            disabled=maintenance,
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
            disabled=maintenance,
        )

        if st.button(
            "🔐 Login",
            disabled=maintenance,
            use_container_width=True,
        ):
            student = login_student(email, password)

            if student == "BLOCKED":
                st.error(
                    "🚫 Your account has been blocked. Please contact the administrator."
                )

            elif student:
                st.session_state.logged_in = True
                st.session_state.student_email = student["email"]
                st.session_state.student_name = student["name"]
                st.success("Login Successful!")
                st.rerun()

            else:
                st.error("Invalid email or password")

    with tab2:
        if not get_registration_enabled():
            st.warning("📝 New registrations are temporarily disabled.")
            st.info("Please contact the administrator or try again later.")

        else:
            name = st.text_input("Full Name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input(
                "Password", type="password", key="reg_password"
            )

            if st.button("Register"):
                if register_student(name, reg_email, reg_password):
                    st.success("Registration successful! Please log in.")
                else:
                    st.errors("Email already registered.")
    with tab3:
        admin_user = st.text_input("Admin Username", key="admin_user")

        admin_pass = st.text_input("Admin Password", type="password", key="admin_pass")

        if st.button("Admin Login", key="admin_login_btn"):
            if admin_login(admin_user, admin_pass):
                st.session_state.logged_in = True
                st.session_state.is_admin = True

                st.success("Admin login successful!")
                st.rerun()

            else:
                st.error("Invalid admin credentials")
    end_page_timer()
    show_monitor()
    st.stop()


if st.session_state.get("is_admin", False):
    admin.show_admin_dashboard()
    st.stop()

    end_page_timer()
    show_monitor()
# ====================================================
# Load questions from folder


conn = get_connection()
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
# Get unique subjects
subjects = sorted({q["subject"] for q in questions})
subjects.append("Full Mock Test")

import random

selected_subject = st.selectbox(
    "Select Subject",
    subjects,
    index=None,
    placeholder="Select Subject",
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
if selected_subject is None:
    questions = []

elif selected_subject == "Full Mock Test":
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

end_page_timer()
show_monitor()
st.stop()
