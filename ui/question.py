import os

import streamlit as st


def render_question(questions, current_q):
    """
    Render the current question and image.
    """

    q = questions[current_q]

    st.markdown(f"## Q{current_q + 1}")

    st.write(q["question"])

    if q.get("image"):
        if os.path.exists(q["image"]):
            st.image(q["image"], width=450)
