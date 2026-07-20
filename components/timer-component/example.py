import time

import streamlit as st
from timer_component import timer_component

st.title("Timer Component Test")

# Create an end time 2 minutes from now
if "end_time" not in st.session_state:
    st.session_state.end_time = int(time.time()) + 120

result = timer_component(
    end_time=st.session_state.end_time,
    key="exam_timer",
)

remaining = max(0, st.session_state.end_time - int(time.time()))
st.write(f"Remaining (Python): {remaining} seconds")

st.write("Component returned:")
st.json(result)

if result.get("expired"):
    st.success("✅ Timer Expired!")
