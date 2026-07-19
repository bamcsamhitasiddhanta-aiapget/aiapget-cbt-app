import time

import streamlit as st
import streamlit.components.v1 as components


def render_timer(selected_subject):
    """
    Render exam timer and return remaining seconds.
    """

    # Exam duration

    # Initialize start time
    if st.session_state.end_time is None:
        st.error("Exam timer not initialized.")
        st.stop()

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

    const timer = document.getElementById("timer");
    const countdown = document.getElementById("countdown");

    function updateTimer() {{

        let mins = Math.floor(remaining / 60);
        let secs = remaining % 60;

        countdown.innerHTML =
            mins.toString().padStart(2,"0") + ":" +
            secs.toString().padStart(2,"0");

        // Change colors
        if (remaining <= 300) {{
           timer.style.borderColor = "#d32f2f";
           timer.style.color = "#d32f2f";
        }}
        else if (remaining <= 1800) {{
            timer.style.borderColor = "#f57c00";
            timer.style.color = "#f57c00";
        }}
        else {{
            timer.style.borderColor = "#2e7d32";
            timer.style.color = "#2e7d32";
        }}

        if (remaining <= 0) {{

            clearInterval(timerInterval);

            countdown.innerHTML = "00:00";

            return;
        }}

        remaining--;

    }}

    updateTimer();

    const timerInterval = setInterval(updateTimer,1000);

    </script>
    """
    components.html(timer_html, height=110)
    return remaining
