from datetime import datetime

import streamlit as st

from exam_db import get_previous_attempts, get_student_summary


def dashboard_card(icon, title, description, button_text, page_key):

    st.markdown(
        f"""
        <div style="
            border:1px solid #ddd;
            border-radius:12px;
            padding:20px;
            margin-bottom:15px;
            background-color:#fafafa;
        ">
            <h3>{icon} {title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(button_text, key=page_key, use_container_width=True):
        st.session_state.student_page = page_key
        st.rerun()


def show_student_dashboard(student_name):

    st.title("🎓 AIAPGET CBT Practice Test")

    st.markdown(
        f"""
### Welcome, **{student_name}**

Practice consistently. Success in AIAPGET comes one test at a time.
"""
    )

    st.divider()

    summary = get_student_summary(st.session_state.student_email)

    total_tests = summary["total_tests"] or 0
    average_score = summary["average_percentage"] or 0
    highest_score = summary["highest_percentage"] or 0

    last_test = summary["last_test"]

    if last_test:
        # If PostgreSQL returns a string
        if isinstance(last_test, str):
            last_test = datetime.fromisoformat(last_test).strftime("%d-%m-%Y")
        else:
            # If it returns a datetime object
            last_test = last_test.strftime("%d-%m-%Y")
    else:
        last_test = "-"

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Tests Attempted", total_tests)

    with c2:
        st.metric("Average Score", f"{average_score}%")

    with c3:
        st.metric("Highest Score", f"{highest_score}%")

    with c4:
        st.metric("Last Test", last_test)
        st.divider()

    col1, col2 = st.columns(2)

    with col1:
        dashboard_card(
            "📘",
            "Subject Tests",
            "Practice individual subjects with a timed CBT examination.",
            "Start Subject Tests",
            "subject_tests",
        )

    with col2:
        dashboard_card(
            "📖",
            "Samhita Tests",
            "Practice Charaka, Sushruta, Ashtanga Hridaya and other Samhitas.",
            "Start Samhita Tests",
            "samhita_tests",
        )

    col3, col4 = st.columns(2)

    with col3:
        dashboard_card(
            "🎯",
            "Mock Tests",
            "Attempt a complete AIAPGET-style mock examination.",
            "Start Mock Test",
            "mock_tests",
        )

    with col4:
        dashboard_card(
            "📊",
            "My Results",
            "View your previous test attempts and performance.",
            "View Results",
            "my_results",
        )

        st.divider()
        st.subheader("📜 Recent Activity")
        attempts = get_previous_attempts(st.session_state.student_email)
        if not attempts:
            st.info("No tests attempted yet.")
        else:
            for row in attempts[:5]:
                submitted = row["submitted_at"]

                if submitted:
                    if isinstance(submitted, str):
                        submitted = datetime.fromisoformat(submitted)
                    submitted = submitted.strftime("%d-%m-%Y %I:%M %p")
                else:
                    submitted = "-"

                st.container(border=True)

                c1, c2, c3 = st.columns([4, 1, 2])

                with c1:
                    st.write(f"**{row['subject']}**")

                with c2:
                    st.write(f"**{row['percentage']}%**")

                with c3:
                    st.write(submitted)

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.student_page = None
        st.rerun()
