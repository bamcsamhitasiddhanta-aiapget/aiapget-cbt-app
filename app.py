import streamlit as st
from dotenv import find_dotenv, load_dotenv

import admin
import samhita_tests
import student_dashboard
import student_test
import subject_tests
from admin_database import get_maintenance_mode, get_registration_enabled
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

# Student Navigation
if "student_page" not in st.session_state:
    st.session_state.student_page = "dashboard"
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

                # First page after login
                st.session_state.student_page = "dashboard"

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


# ================= STUDENT ROUTER =================

if st.session_state.student_page == "dashboard":
    student_dashboard.show_student_dashboard(st.session_state.student_name)

elif st.session_state.student_page == "subject_tests":
    subject_tests.show_subject_tests()

elif st.session_state.student_page == "mock_tests":
    st.info("🚧 Mock Tests - Coming Soon")

elif st.session_state.student_page == "samhita_tests":
    samhita_tests.show_samhita_tests()

elif st.session_state.student_page == "my_results":
    from pages import my_results

    my_results.show_my_results()


end_page_timer()
show_monitor()
st.stop()
