import os
import time

import streamlit as st


def show_test(
    questions,
    selected_subject,
    student_name,
    student_email,
):

    st.title("AIAPGET-CBT-TEST")
    defaults = {
        "test_state": "home",
        "start_time": None,
        "current_q": 0,
        # NEW
        "question_state": {},
        "submitted": False,
        "result_saved": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.test_state == "home":
        show_home(questions)
        return
    if st.session_state.test_state == "running":
        show_running(
            questions,
            selected_subject,
            student_name,
            student_email,
        )
        return


def show_home(questions):

    st.subheader("Instructions")

    st.write(f"Total Questions : {len(questions)}")
    st.write("Subject Test : 30 Minutes")
    st.write("Full Mock : 2 Hours")

    st.info("Do not refresh the browser during the examination.")

    if st.button(
        "🚀 Start Test",
        use_container_width=True,
    ):
        st.session_state.test_state = "running"

        st.session_state.start_time = time.time()

        st.session_state.current_q = 0

        st.rerun()


def show_running(
    questions,
    selected_subject,
    student_name,
    student_email,
):
    # Timer
    if selected_subject == "Full Mock Test":
        total_time = 7200
    else:
        total_time = 1800

    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(total_time - elapsed))

    mins = remaining // 60
    secs = remaining % 60

    st.markdown(f"## ⏳ Time Left: {mins}:{secs:02d}")

    q = questions[st.session_state.current_q]

    st.markdown(f"## Q{st.session_state.current_q + 1}")

    st.write(q["question"])

    if q.get("image"):
        if os.path.exists(q["image"]):
            st.image(q["image"], width=450)
    current_state = st.session_state.question_state.get(
        st.session_state.current_q,
        {},
    )

    saved_answer = current_state.get("answer", None)

    index = None

    if saved_answer in q["options"]:
        index = q["options"].index(saved_answer)

    answer = st.radio(
        "",
        q["options"],
        index=index,
        key=f"q_{st.session_state.current_q}",
    )

    if answer is not None:
        st.session_state.question_state[st.session_state.current_q] = {
            "visited": True,
            "answer": answer,
            "review": current_state.get("review", False),
        }
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Previous", use_container_width=True):
            if st.session_state.current_q > 0:
                st.session_state.current_q -= 1
                st.rerun()

    with col2:
        review_text = "⭐ Mark for Review"

        if st.session_state.current_q in st.session_state.review:
            review_text = "⭐ Remove Review"

        if st.button(review_text, use_container_width=True):
            if st.session_state.current_q in st.session_state.review:
                del st.session_state.review[st.session_state.current_q]

            else:
                st.session_state.review[st.session_state.current_q] = True

            st.rerun()

    with col3:
        if st.button("Next ➡", use_container_width=True):
            if st.session_state.current_q < len(questions) - 1:
                st.session_state.current_q += 1
                st.rerun()
    st.divider()

    st.subheader("🗂 Question Palette")

    NUM_COLS = 5

    for start in range(0, len(questions), NUM_COLS):
        cols = st.columns(NUM_COLS)

        for i in range(NUM_COLS):
            q_no = start + i

            if q_no >= len(questions):
                continue

            state = st.session_state.question_state.get(q_no, {})

            # Current Question
            if q_no == st.session_state.current_q:
                icon = "🔵"

            # Answered + Review
            elif state.get("answer") is not None and state.get("review", False):
                icon = "🟣🟢"

            # Review
            elif state.get("review", False):
                icon = "🟣"

            # Answered
            elif state.get("answer") is not None:
                icon = "🟩"

            # Visited but Not Answered
            elif state.get("visited", False):
                icon = "🟧"

            # Not Visited
            else:
                icon = "⬜"

            if cols[i].button(
                f"{icon} {q_no + 1}",
                key=f"palette_{q_no}",
                use_container_width=True,
            ):
                st.session_state.current_q = q_no
                st.rerun()
