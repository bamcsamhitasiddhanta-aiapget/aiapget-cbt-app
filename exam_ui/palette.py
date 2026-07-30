import streamlit as st


def render_palette(questions, get_question_state):
    """
    Render the question palette and submit button.

    Returns:
        True if Submit Test is clicked.
        False otherwise.
    """

    st.subheader("🗂 Question Palette")

    NUM_COLS = 5

    for start in range(0, len(questions), NUM_COLS):
        cols = st.columns(NUM_COLS)

        for i in range(NUM_COLS):
            q_no = start + i

            if q_no >= len(questions):
                continue

            state = get_question_state(q_no)

            # Current Question
            if q_no == st.session_state.current_q:
                icon = "🔵"

            # Answered + Review
            elif state["review"] and state["answer"] is not None:
                icon = "🟪🟩"

            # Review only
            elif state["review"]:
                icon = "🟪"

            # Answered
            elif state["answer"] is not None:
                icon = "🟩"

            # Visited but Not Answered
            elif state.get("visited", False):
                icon = "🟧"

            # Not Visited
            else:
                icon = "⬜"

            if cols[i].button(
                f"{icon} {q_no + 1}",
                key=f"palette_{q_no}",
                use_container_width=True,
            ):
                st.session_state.current_q = q_no
                st.rerun()

    st.divider()

    col_submit = st.columns([4, 1])[1]

    with col_submit:
        if st.button(
            "🔴 Submit Test",
            use_container_width=True,
        ):
            return True

    return False
