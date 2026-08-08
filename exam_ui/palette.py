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
        cols = st.columns(NUM_COLS, gap="small")

        for i in range(NUM_COLS):
            q_no = start + i

            if q_no >= len(questions):
                continue

            state = get_question_state(q_no)

            # -----------------------------------------
            # Determine status
            # -----------------------------------------

            if q_no == st.session_state.current_q:
                marker = "🔵"

            elif state["review"] and state["answer"] is not None:
                marker = "🟣🟢"

            elif state["review"]:
                marker = "🟣"

            elif state["answer"] is not None:
                marker = "🟢"

            elif state.get("visited", False):
                marker = "🟠"

            else:
                marker = "⬜"

            # -----------------------------------------
            # Palette button
            # -----------------------------------------

            if cols[i].button(
                f"{marker} {q_no + 1:02d}",
                key=f"palette_{q_no}",
                use_container_width=True,
            ):
                st.session_state.current_q = q_no
                st.rerun()

    # -----------------------------------------
    # Legend
    # -----------------------------------------

    st.markdown("**Status**")

    legend_col1, legend_col2 = st.columns(2)

    with legend_col1:
        st.caption("🟢 Answered")
        st.caption("🟣 Review")

    with legend_col2:
        st.caption("🟠 Not Answered")
        st.caption("⬜ Not Visited")

    st.divider()

    # -----------------------------------------
    # Submit
    # -----------------------------------------

    if st.button(
        "🔴 Submit Test",
        use_container_width=True,
    ):
        return True

    return False
