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

    st.subheader("📊 Question Summary")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("🟩 Answered", answered)
        st.metric("🟪 Review", review)

    with c2:
        st.metric("🟧 Not Answered", not_answered)
        st.metric("⬜ Not Visited", not_visited)
