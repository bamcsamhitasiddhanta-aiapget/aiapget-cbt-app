import time

import streamlit as st
import streamlit.components.v1 as components


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
    ">
    ⏳ Time Left: <span id="countdown">{remaining}</span>
    </div>

    <script>

    let remaining = {remaining};

    function updateTimer() {{

        let mins = Math.floor(remaining / 60);
        let secs = remaining % 60;

        document.getElementById("countdown").innerHTML =
            mins.toString().padStart(2,"0") + ":" +
            secs.toString().padStart(2,"0");

        remaining--;

    }}

    updateTimer();

    setInterval(updateTimer,1000);

    </script>
    """
    components.html(timer_html, height=110)
    return remaining
