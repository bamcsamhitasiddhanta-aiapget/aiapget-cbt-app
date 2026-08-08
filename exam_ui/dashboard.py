import streamlit as st

from exam_ui.palette import render_palette
from exam_ui.progress import render_progress
from exam_ui.question_summary import render_question_summary


def render_dashboard(
    questions,
    get_question_state,
):

    st.markdown(
        """
        <div class="dashboard-title">
            📝 Exam Dashboard
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================
    # QUESTION PALETTE
    # =========================================

    render_palette(
        questions,
        get_question_state,
    )

    st.divider()

    # =========================================
    # PROGRESS
    # =========================================

    render_progress(
        questions,
        get_question_state,
    )

    # =========================================
    # SUMMARY
    # =========================================

    render_question_summary(
        questions,
        get_question_state,
    )

    st.divider()

    # =========================================
    # SUBMIT
    # =========================================

    if st.button(
        "🔴 Submit Test",
        use_container_width=True,
    ):
        return True

    return False
