import time

import streamlit as st


def render_timer(selected_subject):
    """
    Render exam timer and return remaining seconds.
    """

    # Exam duration
    total_time = 1200

    if selected_subject == "Full Mock Test":
        total_time = 7200

    # Initialize start time
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    remaining = max(0, int(st.session_state.end_time - time.time()))

    mins = remaining // 60
    secs = remaining % 60

    st.markdown(f"## ⏳ Time Left: {mins}:{secs:02d}")

    return remaining
