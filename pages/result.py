import streamlit as st

from ui import section_title


def format_duration(seconds):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    return f"{minutes:02d}:{secs:02d}"


def show_result():

    result = st.session_state.result

    duration = format_duration(result["duration_seconds"])

    section_title("🧠 AIAPGET CBT RESULT")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**👤 Student :** {result['student_name']}")
        st.write(f"**📧 Email :** {result['student_email']}")

    with col2:
        st.write(f"**📚 Subject :** {result['subject']}")
        st.write(f"**⏱ Time Taken :** {duration}")

    from time_utils import format_timestamp

    st.caption(f"Completed on {format_timestamp(result['submitted_at'])}")

    st.divider()
    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("✅", "Correct", result["correct"]),
        ("❌", "Wrong", result["wrong"]),
        ("🟡", "Not Answered", result["not_answered"]),
        ("🎯", "Accuracy", f"{result['percentage']}%"),
    ]

    for col, (icon, title, value) in zip([c1, c2, c3, c4], cards):
        with col:
            with st.container(border=True):
                st.markdown(f"## {icon}")
                st.markdown(f"# {value}")
                st.caption(title)
    st.divider()

    st.markdown("### 📋 Test Summary")

    i1, i2, i3 = st.columns(3)

    with i1:
        st.metric("Questions", result["total_questions"])

    with i2:
        st.metric("Attempted", result["correct"] + result["wrong"])

    with i3:
        st.metric("Skipped", result["not_answered"])

    # Performance Message
    if result["percentage"] >= 95:
        st.success("🌟 Outstanding Performance! You are exam ready.")
    elif result["percentage"] >= 85:
        st.success("🎉 Excellent Work! Keep up the consistency.")
    elif result["percentage"] >= 70:
        st.info("👏 Good Performance! A little more practice will help.")
    elif result["percentage"] >= 50:
        st.warning("📚 Fair Performance. Focus on your weak areas.")
    else:
        st.error("💪 Keep Practicing! Every test is a step toward improvement.")

    with st.container(border=True):
        st.markdown("## 🏆 FINAL SCORE")
        st.markdown(f"### {result['percentage']}% Accuracy")

        st.markdown(
            f"""
    # {result["score"]} / {result["total_questions"]}
    """
        )

        st.progress(result["percentage"] / 100)

    st.divider()

    b1, b2 = st.columns(2)

    with b1:
        if st.button(
            "📄 Review Answers ",
            use_container_width=True,
        ):
            from exam_db import get_attempt_review

            st.session_state.review_data = get_attempt_review(
                st.session_state.attempt_id
            )

            st.session_state.review_q = 0

            st.session_state.test_state = "review"

            st.rerun()
    with b2:
        if st.button(
            "🏠 Back to Dashboard",
            use_container_width=True,
        ):
            from student_test import reset_exam_session

            reset_exam_session()

            st.session_state.result = None
            st.session_state.question_state = {}

            # Return to Student Dashboard
            st.session_state.student_page = "dashboard"

            st.rerun()
