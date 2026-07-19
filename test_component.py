import streamlit as st

from components.timer_component import timer_component

st.write(timer_component)
st.write(type(timer_component))

result = timer_component()

st.write(result)
