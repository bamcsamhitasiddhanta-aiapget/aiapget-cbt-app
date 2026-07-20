import time

import streamlit as st
from timer_component import timer_component


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

    result = timer_component(
        end_time=int(st.session_state.end_time),
        key="exam_timer",
    )
    return remaining, result.get("expired", False)
