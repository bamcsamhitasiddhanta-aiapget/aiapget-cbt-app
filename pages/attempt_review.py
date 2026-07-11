import streamlit as st

from exam_db import get_attempt_review


def show_attempt_review(
    attempt_id,
):
    rows = get_attempt_review(attempt_id)

    st.title("📖 Attempt Review")
    st.write(f"Attempt ID : {attempt_id}")

    st.divider()
    if st.button(
        "🏠 Back to Dashboard",
        use_container_width=True,
    ):
        st.session_state.test_state = "home"

        if "review_attempt_id" in st.session_state:
            del st.session_state.review_attempt_id

        st.rerun()

    for q in rows:
        st.subheader(f"Question {q[0]}")

        st.write(q[2])

        st.write("Your Answer :", q[7])

        st.write("Correct Answer :", q[8])

        st.write("Explanation :", q[10])

        st.divider()
