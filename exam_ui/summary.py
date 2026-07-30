import streamlit as st


def show_submit_confirmation(questions, get_question_state):
    """
    Render the submit confirmation page.

    Returns:
        "back"   -> User clicked Back to Test
        "submit" -> User clicked Submit Final
        None     -> No action
    """

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
    not_visited = total - visited

    st.title("Submit Test")

    st.warning("Once submitted you cannot modify your answers.")

    st.write(f"Total Questions : {total}")
    st.write(f"Answered : {answered}")
    st.write(f"Not Answered : {not_answered}")
    st.write(f"Marked for Review : {review}")
    st.write(f"Answered & Review : {answered_review}")
    st.write(f"Not Visited : {not_visited}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "⬅ Back to Test",
            use_container_width=True,
        ):
            return "back"

    with col2:
        if st.button(
            "✅ Submit Final",
            use_container_width=True,
        ):
            return "submit"

    return None
