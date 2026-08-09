import streamlit as st


def render_progress(stats):
    """Render the exam progress card."""

    total = stats["total"]
    answered = stats["answered"]
    percentage = stats["percentage"]

    st.markdown(
        f"""<div class="progress-card">
<div class="progress-header">
<span>📈 Exam Progress</span>
<span class="progress-percentage">{percentage}%</span>
</div>

<div class="progress-track">
<div class="progress-fill" style="width:{percentage}%;"></div>
</div>

<div class="progress-footer">
<span>{answered} / {total} Questions</span>
<span>{percentage}% Completed</span>
</div>
</div>""",
        unsafe_allow_html=True,
    )
