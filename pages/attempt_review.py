import streamlit as st

from exam_db import get_attempt_review
from ui import question_status, review_option


def show_attempt_review(attempt_id):

    rows = get_attempt_review(attempt_id)

    if not rows:
        st.error("No questions found for this attempt.")
        return

    if "attempt_review_q" not in st.session_state:
        st.session_state.attempt_review_q = 0

    if st.session_state.attempt_review_q >= len(rows):
        st.session_state.attempt_review_q = 0

    st.title("📖 Attempt Review")
    st.write(f"Attempt ID : {attempt_id}")

    st.divider()

    if st.button(
        "🏠 Back to Dashboard",
        use_container_width=True,
    ):
        st.session_state.review_attempt_id = None
        st.session_state.attempt_review_q = 0
        st.session_state.test_state = "home"
        st.rerun()

    q = rows[st.session_state.attempt_review_q]
    subject = q["subject"]
    question = q["question"]

    option1 = q["option1"]
    option2 = q["option2"]
    option3 = q["option3"]
    option4 = q["option4"]

    student_answer = q["selected_answer"]
    correct_answer = q["correct_answer"]

    is_correct = q["is_correct"]
    explanation = q["explanation"]

    st.caption(f"📚 {subject}")

    question_status(is_correct)

    st.subheader(f"Question {st.session_state.attempt_review_q + 1} of {len(rows)}")

    st.write(question)

    options = [
        option1,
        option2,
        option3,
        option4,
    ]

    for option in options:
        review_option(
            option,
            student_answer,
            correct_answer,
        )

    st.write("### 📘 Explanation")

    st.write(explanation)

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("⬅ Previous"):
            if st.session_state.attempt_review_q > 0:
                st.session_state.attempt_review_q -= 1
                st.rerun()

    with c2:
        if st.button("🏠 Home"):
            st.session_state.review_attempt_id = None
            st.session_state.attempt_review_q = 0
            st.session_state.test_state = "home"
            st.rerun()

    with c3:
        if st.button("Next ➡"):
            if st.session_state.attempt_review_q < len(rows) - 1:
                st.session_state.attempt_review_q += 1
                st.rerun()

    st.divider()

    st.subheader("🗂 Question Palette")

    NUM_COLS = 5

    for start in range(0, len(rows), NUM_COLS):
        cols = st.columns(NUM_COLS)

        for i in range(NUM_COLS):
            q_no = start + i

            if q_no >= len(rows):
                continue

            if cols[i].button(
                str(q_no + 1),
                key=f"attempt_palette_{q_no}",
                use_container_width=True,
            ):
                st.session_state.attempt_review_q = q_no
                st.rerun()
