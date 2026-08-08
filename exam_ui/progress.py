import streamlit as st


def render_progress(
    questions,
    get_question_state,
):
    """Render the exam progress card."""

    total = len(questions)

    answered = 0

    for q_no in range(total):
        state = get_question_state(q_no)

        if state["answer"] is not None:
            answered += 1

    progress = answered / total if total else 0
    percentage = int(progress * 100)

    st.markdown(
        f"""<div class="progress-card">
<div class="progress-header">
<span>📈 Exam Progress</span>
<span class="progress-percentage">{percentage}%</span>
</div>

<div class="progress-track">
<div class="progress-fill" style="width:{percentage}%;"></div>
</div>

<div class="progress-footer">
<span>{answered} / {total} Questions</span>
<span>{percentage}% Completed</span>
</div>
</div>""",
        unsafe_allow_html=True,
    )
