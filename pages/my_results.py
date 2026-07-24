from datetime import datetime

import streamlit as st

from exam_db import get_previous_attempts, get_student_summary


def show_my_results():
    st.title("📊 My Results")
    st.write("Welcome to My Results")
    summary = get_student_summary(st.session_state.student_email)
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

            with st.container(border=True):
                c1, c2, c3 = st.columns([4, 1, 2])

                with c1:
                    st.write(f"**{row['subject']}**")

                with c2:
                    st.write(f"**{row['percentage']}%**")

                with c3:
                    st.write(submitted)
