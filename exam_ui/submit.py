import time

import streamlit as st

from exam_db import create_attempt, finish_attempt, save_response
from exam_ui.exam_state import get_question_state
from student_test import calculate_result
from time_utils import current_time_iso


def submit_exam(
    questions,
    selected_subject,
    student_name,
    student_email,
):
    if not st.session_state.submitted:
        st.session_state.submitted = True
    else:
        return

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
    submitted_at = current_time_iso()
    finish_attempt(
        attempt_id=attempt_id,
        answered=result["answered"],
        not_answered=result["not_answered"],
        correct=result["correct"],
        wrong=result["wrong"],
        score=result["score"],
        percentage=result["percentage"],
        duration_seconds=duration_seconds,
        submitted_at=submitted_at,
    )

    st.session_state.result = {
        "student_name": student_name,
        "student_email": student_email,
        "subject": selected_subject,
        "total_questions": len(questions),
        "duration_seconds": duration_seconds,
        "submitted_at": submitted_at,
        **result,
    }
    st.session_state.test_state = "result"

    st.rerun()
