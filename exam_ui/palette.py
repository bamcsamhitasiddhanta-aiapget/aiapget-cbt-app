import streamlit as st


def render_palette(questions, get_question_state):
    """
    Render the question palette and submit button.

    Returns:
        True if Submit Test is clicked.
        False otherwise.
    """

    st.markdown(
        """
        <div class="palette-title">
            🗂 Question Palette
        </div>
        """,
        unsafe_allow_html=True,
    )

    NUM_COLS = 5

    # -------------------------------------------------
    # Build status information
    # -------------------------------------------------

    for q_no in range(len(questions)):
        state = get_question_state(q_no)

        # Current question
        if q_no == st.session_state.current_q:
            status = "current"

        # Answered + Review
        elif state["review"] and state["answer"] is not None:
            status = "answered-review"

        # Review only
        elif state["review"]:
            status = "review"

        # Answered
        elif state["answer"] is not None:
            status = "answered"

        # Visited but not answered
        elif state.get("visited", False):
            status = "not-answered"

        # Not visited
        else:
            status = "not-visited"

        # -------------------------------------------------
        # CSS selector based on button aria-label
        # -------------------------------------------------

        number = q_no + 1

        if status == "current":
            background = "#2563EB"
            border = "#1D4ED8"
            text = "#FFFFFF"
            shadow = "0 0 0 3px rgba(37,99,235,.18)"

        elif status == "answered-review":
            background = "#8B5CF6"
            border = "#7C3AED"
            text = "#FFFFFF"
            shadow = "inset 0 -5px 0 #10B981"

        elif status == "review":
            background = "#8B5CF6"
            border = "#7C3AED"
            text = "#FFFFFF"
            shadow = "0 3px 8px rgba(139,92,246,.18)"

        elif status == "answered":
            background = "#10B981"
            border = "#059669"
            text = "#FFFFFF"
            shadow = "0 3px 8px rgba(16,185,129,.18)"

        elif status == "not-answered":
            background = "#F97316"
            border = "#EA580C"
            text = "#FFFFFF"
            shadow = "0 3px 8px rgba(249,115,22,.18)"

        else:
            background = "#F3F4F6"
            border = "#D1D5DB"
            text = "#374151"
            shadow = "none"

        st.markdown(
            f"""
            <style>
            button[aria-label="{number}"] {{
                background: {background} !important;
                border-color: {border} !important;
                color: {text} !important;
                box-shadow: {shadow} !important;
            }}

            button[aria-label="{number}"]:hover {{
                filter: brightness(0.96);
                transform: translateY(-1px);
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    # -------------------------------------------------
    # Palette grid
    # -------------------------------------------------

    for start in range(0, len(questions), NUM_COLS):
        cols = st.columns(NUM_COLS, gap="small")

        for i in range(NUM_COLS):
            q_no = start + i

            if q_no >= len(questions):
                continue

            number = q_no + 1

            if cols[i].button(
                f"{number}",
                key=f"palette_{q_no}",
                use_container_width=True,
            ):
                st.session_state.current_q = q_no
                st.rerun()

    # -------------------------------------------------
    # Legend
    # -------------------------------------------------

    st.markdown(
        """<div class="palette-legend">
    <div>
    <span class="legend-dot legend-green"></span>
    Answered
    </div>

    <div>
    <span class="legend-dot legend-orange"></span>
    Not Answered
    </div>

    <div>
    <span class="legend-dot legend-purple"></span>
    Review
    </div>

    <div>
    <span class="legend-dot legend-grey"></span>
    Not Visited
    </div>
    </div>""",
        unsafe_allow_html=True,
    )

    st.divider()

    # -------------------------------------------------
    # Submit
    # -------------------------------------------------

    if st.button(
        "🔴 Submit Test",
        use_container_width=True,
    ):
        return True

    return False
