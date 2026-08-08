import streamlit as st


def render_question_summary(questions, get_question_state):
    total = len(questions)

    answered = 0
    review = 0
    visited = 0

    for q_no in range(total):
        state = get_question_state(q_no)

        if state["visited"]:
            visited += 1

        if state["answer"] is not None:
            answered += 1

        if state["review"]:
            review += 1

    not_answered = visited - answered
    not_visited = total - visited

    st.markdown(
        """
        <div class="summary-title">
            📊 Question Summary
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="summary-grid">

<div class="summary-item answered-card">
    <div class="summary-status">
        <span class="status-dot answered-dot"></span>
        Answered
    </div>
    <div class="summary-number">{answered}</div>
</div>

<div class="summary-item not-answered-card">
    <div class="summary-status">
        <span class="status-dot not-answered-dot"></span>
        Not Answered
    </div>
    <div class="summary-number">{not_answered}</div>
</div>

<div class="summary-item review-card">
    <div class="summary-status">
        <span class="status-dot review-dot"></span>
        Review
    </div>
    <div class="summary-number">{review}</div>
</div>

<div class="summary-item not-visited-card">
    <div class="summary-status">
        <span class="status-dot not-visited-dot"></span>
        Not Visited
    </div>
    <div class="summary-number">{not_visited}</div>
</div>

</div>
        """,
        unsafe_allow_html=True,
    )
