from datetime import datetime

import streamlit as st

from exam_db import get_previous_attempts, get_student_dashboard, get_student_summary
from utils import format_duration


def show_my_results():
    st.title("📊 My Results")
    st.caption("View your test history, previous attempts and performance.")
    st.divider()
    summary = get_student_summary(st.session_state.student_email)
    summary = get_student_summary(st.session_state.student_email)
    previous_attempts = get_previous_attempts(st.session_state.student_email)
    dashboard = get_student_dashboard(st.session_state.student_email)
    overall = dashboard.get("overall")

    if overall is None:
        overall = {}
    elif not isinstance(overall, dict):
        overall = dict(overall)

    tests_taken = overall.get("total_tests", 0) or 0
    best_accuracy = float(overall.get("highest_percentage", 0) or 0)
    average_accuracy = float(overall.get("average_percentage", 0) or 0)
    average_time = int(overall.get("average_duration", 0) or 0)

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
    # ==================================================
    # Statistics
    # ==================================================

    st.divider()

    st.subheader("📊 Your Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Tests Taken", tests_taken)

    with c2:
        st.metric("Best Accuracy", f"{best_accuracy:.2f}%")

    with c3:
        st.metric("Average Accuracy", f"{average_accuracy:.2f}%")

    with c4:
        st.metric("Average Time", format_duration(average_time))

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
    st.divider()
    st.subheader("📂 Previous Attempts")

    if previous_attempts:
        for attempt in previous_attempts:
            attempt_id = attempt["attempt_id"]
            subject = attempt["subject"]
            percentage = attempt["percentage"]
            duration = format_duration(attempt["duration_seconds"])
            date = attempt["submitted_at"][:10] if attempt["submitted_at"] else "-"

            col1, col2 = st.columns([6, 1])

            with col1:
                st.write(
                    f"📚 **{subject}** | "
                    f"🎯 {percentage:.2f}% | "
                    f"⏱ {duration} | "
                    f"📅 {date}"
                )

            with col2:
                if st.button(
                    "👁",
                    key=f"attempt_{attempt_id}",
                ):
                    st.session_state.review_attempt_id = attempt_id
                    st.session_state.attempt_review_q = 0
                    st.session_state.test_state = "attempt_review"
                    st.session_state.student_page = "subject_tests"
                    st.rerun()

    else:
        st.info("No previous attempts.")

    # ==================================================
    # Subject Performance
    # ==================================================

    st.divider()

    st.subheader("📈 Subject Performance")

    subject_performance = dashboard["subject_performance"]

    if subject_performance:
        for row in subject_performance:
            subject = row["subject"]
            percentage = float(row["average_percentage"])
            st.write(f"📚 {subject}")

            st.progress(percentage / 100)

            st.caption(f"{percentage:.2f}%")

    else:
        st.info("No subject performance available.")
