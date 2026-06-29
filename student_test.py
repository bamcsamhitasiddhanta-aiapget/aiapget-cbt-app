import time

import streamlit as st


def show_test(
    questions,
    selected_subject,
    student_name,
    student_email,
):
    st.error("student_test.py is running")
    st.title("🧠 AIAPGET CBT Practice Test")
    defaults = {
        "test_state": "home",
        "start_time": None,
        "current_q": 0,
        "answers": {},
        "review": {},
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
    saved_answer = st.session_state.answers.get(
        st.session_state.current_q,
        None,
    )

    index = None

    if saved_answer in q["options"]:
        index = q["options"].index(saved_answer)

    answer = st.radio(
        "",
        q["options"],
        index=index,
        key=f"q_{st.session_state.current_q}",
    )

    st.session_state.answers[st.session_state.current_q] = answer

    st.session_state.answers[st.session_state.current_q] = answer
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Previous", use_container_width=True):
            if st.session_state.current_q > 0:
                st.session_state.current_q -= 1
                st.rerun()

    with col2:
        if st.button("Next ➡", use_container_width=True):
            if st.session_state.current_q < len(questions) - 1:
                st.session_state.current_q += 1
                st.rerun()
