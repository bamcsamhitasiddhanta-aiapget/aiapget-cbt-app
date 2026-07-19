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

    from streamlit.components.v1 import html

    mins = remaining // 60
    secs = remaining % 60

    timer_html = f"""
    <div id="timer"
    style="
    font-size:40px;
    font-weight:bold;
    text-align:center;
    padding:15px;
    border-radius:10px;
    background:#f8f9fa;
    border:2px solid #4CAF50;
    color:#2E7D32;
    margin-bottom:20px;
    ">
    ⏳ Time Left: {mins:02d}:{secs:02d}
    </div>
    """

    html(timer_html, height=90)

    return remaining
