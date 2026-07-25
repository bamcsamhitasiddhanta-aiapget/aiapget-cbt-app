import streamlit as st

import student_test
from database import (
    get_questions_by_subject,
    get_subjects,
)


def show_subject_tests():

    # Get unique subjects
    subjects = get_subjects()

    selected_subject = st.selectbox(
        "Select Subject",
        subjects,
        index=None,
        placeholder="Select Subject",
        key="subject_select",
        disabled=st.session_state.get("test_state", "home") != "home",
    )

    # Reset test state when subject changes
    if "last_subject" not in st.session_state:
        st.session_state.last_subject = selected_subject

    if st.session_state.last_subject != selected_subject:
        st.session_state.last_subject = selected_subject

        st.session_state.start_time = None
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.session_state.review = {}
        st.session_state.current_q = 0
        st.session_state.result_saved = False

        # Reset mock questions if needed
        st.session_state.mock_questions = None
        st.rerun()

    # ---------------------------------------
    # Mock Test
    # ---------------------------------------

    if st.session_state.get("test_type") in ["full_mock", "mini_mock"]:
        questions = st.session_state.mock_questions

        selected_subject = "Mock Test"

    # ---------------------------------------
    # Subject Test
    # ---------------------------------------

    elif selected_subject is None:
        questions = []

    else:
        questions = get_questions_by_subject(selected_subject)
        st.session_state.mock_questions = None

    # Allow attempt review even without selecting a subject
    if (
        selected_subject is not None
        or st.session_state.get("test_state") == "attempt_review"
    ):
        student_test.show_test(
            questions=questions,
            selected_subject=selected_subject,
            student_name=st.session_state.student_name,
            student_email=st.session_state.student_email,
        )
