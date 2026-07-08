import os
import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from exam_db import (
    create_attempt,
    finish_attempt,
    save_response,
)
from pages.result import show_result


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
        "result": None,
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
    if st.session_state.test_state == "confirm_submit":
        show_submit_confirmation(
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
        st.session_state.submitted = False
        st.session_state.test_state = "running"

        st.session_state.start_time = time.time()

        st.session_state.current_q = 0

        st.rerun()


def get_question_state(q_no):
    """Return state for a question."""

    if q_no not in st.session_state.question_state:
        st.session_state.question_state[q_no] = {
            "visited": False,
            "answer": None,
            "review": False,
        }

    return st.session_state.question_state[q_no]


def save_answer(q_no, answer):

    state = get_question_state(q_no)

    state["visited"] = True

    if answer:
        state["answer"] = answer
    else:
        state["answer"] = None


def toggle_review(q_no):

    state = get_question_state(q_no)

    state["visited"] = True
    state["review"] = not state["review"]


def clear_answer(q_no):

    state = get_question_state(q_no)

    state["visited"] = True
    state["answer"] = None


def option_selector(q_no, options):

    state = get_question_state(q_no)

    current = state["answer"]

    selected = None

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

    if st.session_state.test_state == "running":
        st_autorefresh(
            interval=1000,
            key="exam_timer",
        )
    # Timer
    if selected_subject == "Full Mock Test":
        total_time = 7200
    else:
        total_time = 15

    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(total_time - elapsed))
    if remaining <= 0:
        st.warning("⏰ Time is over. Submitting your test...")

        submit_exam(
            questions,
            selected_subject,
            student_name,
            student_email,
        )

        return

    mins = remaining // 60
    secs = remaining % 60

    st.markdown(f"## ⏳ Time Left: {mins}:{secs:02d}")

    q = questions[st.session_state.current_q]
    state = get_question_state(st.session_state.current_q)

    state["visited"] = True

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

    # Current question state
    state = get_question_state(st.session_state.current_q)

    saved_answer = state["answer"]

    index = None

    if saved_answer in q["options"]:
        index = q["options"].index(saved_answer)

    radio_key = f"q_{st.session_state.current_q}"

    # answer = st.radio(
    #    "",
    #    q["options"],
    #    index=index,
    #    key=radio_key,
    # )

    # Save only after selection
    # if answer is not None:
    #    save_answer(
    #       st.session_state.current_q,
    #        answer,
    #    )
    answer = option_selector(
        st.session_state.current_q,
        q["options"],
    )

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("⬅ Previous", use_container_width=True):
            if st.session_state.current_q > 0:
                st.session_state.current_q -= 1
                st.rerun()

    with col2:
        if st.button(
            "🗑 Clear Response",
            use_container_width=True,
        ):
            clear_answer(
                st.session_state.current_q,
            )

            st.rerun()

    with col3:
        if st.button(
            "🟨 Save & Mark Review",
            use_container_width=True,
        ):
            if answer is None:
                st.warning("⚠ Please select an option.")

            else:
                save_answer(
                    st.session_state.current_q,
                    answer,
                )

                toggle_review(
                    st.session_state.current_q,
                )

                if st.session_state.current_q < len(questions) - 1:
                    st.session_state.current_q += 1

                st.rerun()

    with col4:
        if st.button(
            "💾 Save & Next",
            use_container_width=True,
        ):
            if answer is None:
                st.warning("⚠ Please select an option.")

            else:
                save_answer(
                    st.session_state.current_q,
                    answer,
                )

                if st.session_state.current_q < len(questions) - 1:
                    st.session_state.current_q += 1

                st.rerun()
    with col5:
        if st.button(
            "🟪 Mark Review & Next",
            use_container_width=True,
        ):
            if answer is not None:
                save_answer(
                    st.session_state.current_q,
                    answer,
                )

            toggle_review(
                st.session_state.current_q,
            )

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

            state = get_question_state(q_no)

            # Current Question
            if q_no == st.session_state.current_q:
                icon = "🔵"

            # Answered + Review
            elif state["review"] and state["answer"] is not None:
                icon = "🟪🟩"

            # Review only
            elif state["review"]:
                icon = "🟪"

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
    st.divider()
    col_submit = st.columns([4, 1])[1]

    with col_submit:
        if st.button(
            "🔴 Submit Test",
            use_container_width=True,
        ):
            st.session_state.test_state = "confirm_submit"

            st.rerun()


def submit_exam(
    questions,
    selected_subject,
    student_name,
    student_email,
):
    if st.session_state.submitted:
        return

    st.session_state.submitted = True

    total = len(questions)

    answered = 0
    review = 0
    answered_review = 0
    visited = 0

    for q_no in range(total):
        state = get_question_state(q_no)

        if state["visited"]:
            visited += 1

        if state["answer"] is not None:
            answered += 1

        if state["review"]:
            review += 1

        if state["review"] and state["answer"] is not None:
            answered_review += 1

    not_answered = visited - answered

    attempt_id = create_attempt(
        student_email,
        student_name,
        selected_subject,
        len(questions),
        answered,
        not_answered,
        review,
        answered_review,
    )

    st.session_state.attempt_id = attempt_id

    for q_no, q in enumerate(questions):
        state = get_question_state(q_no)

        selected_answer = state["answer"]
        correct_answer = q["answer"]

        save_response(
            attempt_id=attempt_id,
            question_uid=q["question_uid"],
            question_no=q_no + 1,
            subject=q["subject"],
            selected_answer=selected_answer,
            correct_answer=correct_answer,
            is_correct=int(selected_answer == correct_answer),
            review=state["review"],
            visited=state["visited"],
        )

    result = calculate_result(questions)

    duration_seconds = int(time.time() - st.session_state.start_time)

    finish_attempt(
        attempt_id=attempt_id,
        answered=result["answered"],
        not_answered=result["not_answered"],
        correct=result["correct"],
        wrong=result["wrong"],
        score=result["score"],
        percentage=result["percentage"],
        duration_seconds=duration_seconds,
    )

    st.session_state.result = {
        "student_name": student_name,
        "student_email": student_email,
        "subject": selected_subject,
        "total_questions": len(questions),
        "duration_seconds": duration_seconds,
        **result,
    }
    st.session_state.test_state = "result"

    st.rerun()


def show_submit_confirmation(
    questions,
    selected_subject,
    student_name,
    student_email,
):

    total = len(questions)

    answered = 0
    review = 0
    answered_review = 0
    visited = 0

    for q_no in range(total):
        state = get_question_state(q_no)

        if state["visited"]:
            visited += 1

        if state["answer"] is not None:
            answered += 1

        if state["review"]:
            review += 1

        if state["review"] and state["answer"] is not None:
            answered_review += 1

    not_answered = visited - answered

    not_visited = total - visited

    st.title("Submit Test")

    st.warning("Once submitted you cannot modify your answers.")

    st.write(f"Total Questions : {total}")
    st.write(f"Answered : {answered}")
    st.write(f"Not Answered : {not_answered}")
    st.write(f"Marked for Review : {review}")
    st.write(f"Answered & Review : {answered_review}")
    st.write(f"Not Visited : {not_visited}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "⬅ Back to Test",
            use_container_width=True,
        ):
            st.session_state.test_state = "running"

            st.rerun()

    with col2:
        if st.button(
            "✅ Submit Final",
            use_container_width=True,
        ):
            submit_exam(
                questions,
                selected_subject,
                student_name,
                student_email,
            )


def calculate_result(questions):

    correct = 0
    wrong = 0
    not_answered = 0

    for q_no, q in enumerate(questions):
        state = get_question_state(q_no)

        answer = state["answer"]

        if answer is None:
            not_answered += 1

        elif answer == q["answer"]:
            correct += 1

        else:
            wrong += 1

    total = len(questions)

    score = correct

    percentage = round((score / total) * 100, 2)

    return {
        "answered": correct + wrong,
        "correct": correct,
        "wrong": wrong,
        "not_answered": not_answered,
        "score": score,
        "percentage": percentage,
    }


def show_review():

    rows = st.session_state.review_data

    q = rows[st.session_state.review_q]

    st.title("📖 Review Answers")

    st.write(f"### Question {q[0]}")

    st.info(q[2])
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

    # Image (if available)
    if q[11]:
        if os.path.exists(q[11]):
            st.image(q[11], width=450)

    options = [
        q[3],
        q[4],
        q[5],
        q[6],
    ]

    student_answer = q[7]
    correct_answer = q[8]

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

    if q[10]:
        st.info(q[10])
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
            "🏠 Home",
            use_container_width=True,
        ):
            st.session_state.test_state = "home"

            # Reset review
            st.session_state.review_q = 0
            st.session_state.review_data = None

            # Reset exam
            st.session_state.question_state = {}
            st.session_state.current_q = 0
            st.session_state.result = None
            st.session_state.submitted = False
            st.session_state.start_time = None

            st.rerun()

    with c3:
        if st.button("Next ➡"):
            if st.session_state.review_q < len(rows) - 1:
                st.session_state.review_q += 1
                st.rerun()
