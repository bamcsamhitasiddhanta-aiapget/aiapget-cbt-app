import streamlit as st

from database import (
    get_all_questions,
    get_mock_questions,
)

FULL_MOCK_QUESTIONS = 120
MINI_MOCK_QUESTIONS = 60


def show_mock_tests():

    st.title("🎯 Mock Tests")

    if st.button(
        "⬅ Back to Dashboard",
        use_container_width=True,
    ):
        st.session_state.student_page = "dashboard"
        st.rerun()

    st.divider()

    total_questions = len(get_all_questions())

    st.info(f"📚 Total Question Bank : {total_questions}")

    # --------------------------------------------------
    # Full Mock
    # --------------------------------------------------

    st.subheader("🏆 Full AIAPGET Mock Test")

    st.write("**120 Questions**")
    st.write("**2 Hours**")

    if total_questions < FULL_MOCK_QUESTIONS:
        st.warning(
            f"Full Mock Test requires "
            f"{FULL_MOCK_QUESTIONS} questions.\n\n"
            f"Currently available : {total_questions}"
        )

        st.button(
            "🔒 Start Full Mock",
            disabled=True,
            use_container_width=True,
        )

    else:
        if st.button(
            "▶ Start Full Mock",
            use_container_width=True,
        ):
            st.session_state.test_type = "full_mock"
            st.session_state.mock_questions = get_mock_questions(FULL_MOCK_QUESTIONS)

            st.session_state.student_page = "subject_tests"
            st.session_state.test_state = "home"
            st.session_state.mock_name = "Full AIAPGET Mock"

            st.rerun()

    st.divider()

    # --------------------------------------------------
    # Mini Mock
    # --------------------------------------------------

    st.subheader("⚡ Mini Mock Test")

    st.write("**60 Questions**")
    st.write("**1 Hour**")

    if total_questions < MINI_MOCK_QUESTIONS:
        st.warning(
            f"Mini Mock Test requires "
            f"{MINI_MOCK_QUESTIONS} questions.\n\n"
            f"Currently available : {total_questions}"
        )

        st.button(
            "🔒 Start Mini Mock",
            disabled=True,
            use_container_width=True,
        )

    else:
        if st.button(
            "▶ Start Mini Mock",
            use_container_width=True,
        ):
            st.session_state.test_type = "mini_mock"
            st.session_state.mock_questions = get_mock_questions(MINI_MOCK_QUESTIONS)

            st.session_state.student_page = "subject_tests"
            st.session_state.test_state = "home"
            st.session_state.mock_name = "Mini AIAPGET Mock"

            st.rerun()
