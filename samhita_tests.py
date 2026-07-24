import streamlit as st

import student_test
from database import (
    get_classical_texts,
    get_questions_by_text_and_section,
    get_sections,
)

 
def show_samhita_tests():

    texts = get_classical_texts()

    selected_text = st.selectbox(
        "Select Classical Text",
        texts,
        index=None,
        placeholder="Select Classical Text",
        key="text_select",
    )

    if selected_text is None:
        return

    sections = get_sections(selected_text)

    selected_section = st.selectbox(
        "Select Section",
        sections,
        index=None,
        placeholder="Select Section",
        key="section_select",
    )

    if selected_section is None:
        return

    questions = get_questions_by_text_and_section(
        selected_text,
        selected_section,
    )

    if not questions:
        st.warning("No questions available.")
        return

    student_test.show_test(
        questions=questions,
        selected_subject=f"{selected_text} - {selected_section}",
        student_name=st.session_state.student_name,
        student_email=st.session_state.student_email,
    )
