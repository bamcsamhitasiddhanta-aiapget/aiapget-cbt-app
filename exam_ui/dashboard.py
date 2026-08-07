import streamlit as st

from exam_ui.palette import render_palette
from exam_ui.progress import render_progress
from exam_ui.question_summary import render_question_summary


def render_dashboard(
    questions,
    get_question_state,
):
    """
    Render the complete exam dashboard.
    """

    st.markdown(
        """
        <div class="exam-dashboard">
            <div class="dashboard-title">
                📝 Exam Dashboard
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress card
    render_progress(
        questions,
        get_question_state,
    )

    st.divider()

    # Question Summary
    render_question_summary(
        questions,
        get_question_state,
    )

    st.divider()

    # Question Palette
    submit = render_palette(
        questions,
        get_question_state,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    return submit
