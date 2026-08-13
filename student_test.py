import os
import time

import streamlit as st

from exam_db import (
    get_previous_attempts,
)
from exam_ui.dashboard import render_dashboard
from exam_ui.exam_state import (
    clear_answer,
    get_question_state,
    save_answer,
    toggle_review,
)
from exam_ui.navigation import render_navigation
from exam_ui.options import render_options
from exam_ui.question import render_question
from exam_ui.submit import submit_exam
from exam_ui.summary import show_submit_confirmation
from pages.exam.timer import render_timer
from pages.result import show_result

# ---------------- Timer Configuration ---------------- #

SECONDS_PER_QUESTION = 60

FULL_MOCK_QUESTIONS = 120
FULL_MOCK_TIME = 2 * 60 * 60  # 7200 seconds

MINI_MOCK_QUESTIONS = 60
MINI_MOCK_TIME = 60 * 60  # 3600 seconds


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
        "end_time": None,
        "current_q": 0,
        "question_state": {},
        "submitted": False,
        "result_saved": False,
        "result": None,
        "review_attempt_id": None,
        "attempt_review_q": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.test_state == "home":
        show_home(
            questions,
            selected_subject,
            student_name,
            student_email,
        )
        return
    if st.session_state.test_state == "running":
        show_running(
            questions,
            selected_subject,
            student_name,
            student_email,
        )
        return
    if st.session_state.test_state == "confirm_submit":
        action = show_submit_confirmation(
            questions,
            get_question_state,
        )

        if action == "back":
            st.session_state.test_state = "running"
            st.rerun()

        elif action == "submit":
            submit_exam(
                questions,
                selected_subject,
                student_name,
                student_email,
            )
    if st.session_state.test_state == "result":
        show_result()
        return

    if st.session_state.test_state == "review":
        show_review()
        return

    if st.session_state.test_state == "attempt_review":
        if (
            "review_attempt_id" not in st.session_state
            or st.session_state.review_attempt_id is None
        ):
            st.session_state.test_state = "home"
            st.rerun()

        from pages.attempt_review import show_attempt_review

        show_attempt_review(
            st.session_state.review_attempt_id,
        )

        return


def show_home(
    questions,
    selected_subject,
    student_name,
    student_email,
):

    from exam_db import get_student_dashboard

    previous_attempts = get_previous_attempts(student_email)

    dashboard = get_student_dashboard(student_email)

    overall = dashboard.get("overall")

    if overall is None:
        overall = {}
    elif not isinstance(overall, dict):
        overall = dict(overall)

    st.title("🏠 AIAPGET CBT")

    st.success(f"👋 Welcome {student_name}")

    # ==================================================
    # Instructions
    # ==================================================

    st.divider()

    st.subheader("📝 Instructions")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Questions", len(questions))

    with c2:
        st.metric("Subject Test", "30 min")

    with c3:
        st.metric("Full Mock", "2 hrs")

    st.info("Do not refresh the browser during the examination.")

    start_clicked = st.button(
        "🚀 Start Test",
        use_container_width=True,
        disabled=(selected_subject is None),
    )

    if start_clicked:
        st.session_state.submitted = False
        st.session_state.test_state = "running"
        st.session_state.start_time = time.time()

        test_type = st.session_state.get("test_type", "subject")

        if test_type == "full_mock":
            total_time = FULL_MOCK_TIME

        elif test_type == "mini_mock":
            total_time = MINI_MOCK_TIME

        else:
            total_time = len(questions) * SECONDS_PER_QUESTION

        st.session_state.total_time = total_time
        st.session_state.end_time = st.session_state.start_time + total_time

        st.session_state.current_q = 0
        st.rerun()

    # ==================================================
    # Statistics
    # ==================================================

    # ==================================================
    # Recent Attempts
    # ==================================================

    st.divider()

    st.subheader("🔥 Recent Attempts")

    recent_attempts = dashboard["recent_attempts"]

    if recent_attempts:
        for attempt in recent_attempts:
            subject = attempt["subject"]
            score = attempt["score"]
            percentage = attempt["percentage"]
            submitted = attempt["submitted_at"]
            if submitted:
                submitted = submitted[:10]

            st.write(f"📚 **{subject}** | 🎯 {percentage:.2f}% | 📅 {submitted}")

    else:
        st.info("No recent attempts.")

    # ==================================================
    # Previous Attempts
    # ==================================================

    # ==================================================
    # Subject Performance
    # ==================================================

    # ==================================================
    # Logout
    # ==================================================

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True,
    ):
        st.session_state.clear()
        st.rerun()


def option_selector(q_no, options):

    state = get_question_state(q_no)

    current = state["answer"]

    for option in options:
        checked = option == current
        icon = "🔘" if checked else "⚪"

        if st.button(
            f"{icon} {option}",
            key=f"option_{q_no}_{option}",
        ):
            st.success("CLICKED")
            return option

    return current


def option_selector(q_no, options):

    state = get_question_state(q_no)

    current = state["answer"]

    for option in options:
        checked = option == current
        icon = "🔘" if checked else "⚪"

        if st.button(
            f"{icon} {option}",
            key=f"option_{q_no}_{option}",
            use_container_width=False,
        ):
            save_answer(q_no, option)
            st.rerun()

    return state["answer"]


def show_running(
    questions,
    selected_subject,
    student_name,
    student_email,
):

    left_col, right_col = st.columns(
        [2.7, 1.3],
        gap="medium",
    )

    # =========================================
    # LEFT SIDE — QUESTION
    # =========================================

    with left_col:
        state = get_question_state(st.session_state.current_q)

        state["visited"] = True

        render_question(
            questions,
            st.session_state.current_q,
        )

        q = questions[st.session_state.current_q]

        answer = render_options(
            current_q=st.session_state.current_q,
            options=q["options"],
            get_question_state=get_question_state,
            option_selector=option_selector,
        )

        render_navigation(
            answer=answer,
            total_questions=len(questions),
            save_answer=save_answer,
            clear_answer=clear_answer,
            toggle_review=toggle_review,
        )

    # =========================================
    # RIGHT SIDE — TIMER + DASHBOARD
    # =========================================

    with right_col:
        remaining, expired = render_timer(selected_subject)

        if expired:
            if not st.session_state.submitted:
                submit_exam(
                    questions,
                    selected_subject,
                    student_name,
                    student_email,
                )
            st.stop()

        submit = render_dashboard(
            questions,
            get_question_state,
        )

        if submit:
            st.session_state.test_state = "confirm_submit"
            st.rerun()


def show_review():

    rows = st.session_state.review_data

    q = rows[st.session_state.review_q]

    st.title("📖 Review Answers")

    st.write(f"### Question {q['question_no']}")

    st.info(q["question"])

    st.subheader("Question Palette")

    cols = st.columns(10)

    for i in range(len(rows)):
        with cols[i % 10]:
            if st.button(
                str(i + 1),
                key=f"review_{i}",
                use_container_width=True,
            ):
                st.session_state.review_q = i
                st.rerun()

    # Image
    if q["image"]:
        if os.path.exists(q["image"]):
            st.image(q["image"], width=450)

    options = [
        q["option1"],
        q["option2"],
        q["option3"],
        q["option4"],
    ]

    student_answer = q["selected_answer"]
    correct_answer = q["correct_answer"]

    st.write("### Options")

    for option in options:
        if option == correct_answer:
            st.success(f"✅ {option}")

        elif option == student_answer:
            st.error(f"❌ {option}")

        else:
            st.write(f"⚪ {option}")

    st.divider()

    st.subheader("📘 Explanation")

    if q["explanation"]:
        st.info(q["explanation"])
    else:
        st.info("No explanation available.")

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("⬅ Previous"):
            if st.session_state.review_q > 0:
                st.session_state.review_q -= 1
                st.rerun()

    with c2:
        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
        ):
            st.session_state.review_q = 0
            st.session_state.review_data = None

            reset_exam_session()

            st.session_state.student_page = "dashboard"

            st.rerun()

    with c3:
        if st.button("Next ➡"):
            if st.session_state.review_q < len(rows) - 1:
                st.session_state.review_q += 1
                st.rerun()


def reset_exam_session():

    st.session_state.start_time = None
    st.session_state.submitted = False

    st.session_state.answers = {}
    st.session_state.review = {}

    st.session_state.current_q = 0
    st.session_state.result_saved = False

    st.session_state.mock_questions = None
    st.session_state.last_subject = None

    st.session_state.result = None
    st.session_state.question_state = {}
    st.session_state.test_state = "home"
    if "mock_name" in st.session_state:
        del st.session_state["mock_name"]
