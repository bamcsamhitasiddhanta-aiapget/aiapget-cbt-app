import streamlit as st


def get_question_state(q_no):
    """Return state for a question."""

    if q_no not in st.session_state.question_state:
        st.session_state.question_state[q_no] = {
            "visited": False,
            "answer": None,
            "review": False,
        }

    return st.session_state.question_state[q_no]


def save_answer(q_no, answer):

    state = get_question_state(q_no)

    state["visited"] = True

    if answer:
        state["answer"] = answer
    else:
        state["answer"] = None


def toggle_review(q_no):

    state = get_question_state(q_no)

    state["visited"] = True
    state["review"] = not state["review"]


def clear_answer(q_no):

    state = get_question_state(q_no)

    state["visited"] = True
    state["answer"] = None
