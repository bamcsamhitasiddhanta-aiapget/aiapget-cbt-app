import streamlit as st


def render_progress(
    questions,
    get_question_state,
):
    """
    Render exam progress.
    """

    total = len(questions)

    answered = 0

    for q_no in range(total):
        state = get_question_state(q_no)

        if state["answer"] is not None:
            answered += 1

    progress = answered / total if total else 0

    st.subheader("📈 Exam Progress")

    st.progress(progress)

    st.write(f"**{answered} / {total} Questions Answered**")

    st.caption(f"{progress * 100:.0f}% Completed")
