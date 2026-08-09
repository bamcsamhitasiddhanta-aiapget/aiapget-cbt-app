import streamlit as st


def render_question_summary(stats):
    answered = stats["answered"]
    review = stats["review"]
    not_answered = stats["not_answered"]
    not_visited = stats["not_visited"]
    st.markdown(
        """
        <div class="summary-title">
            📊 Question Summary
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="summary-grid">

<div class="summary-item answered-card">
    <div class="summary-status">
        <span class="status-dot answered-dot"></span>
        Answered
    </div>
    <div class="summary-number">{answered}</div>
</div>

<div class="summary-item not-answered-card">
    <div class="summary-status">
        <span class="status-dot not-answered-dot"></span>
        Not Answered
    </div>
    <div class="summary-number">{not_answered}</div>
</div>

<div class="summary-item review-card">
    <div class="summary-status">
        <span class="status-dot review-dot"></span>
        Review
    </div>
    <div class="summary-number">{review}</div>
</div>

<div class="summary-item not-visited-card">
    <div class="summary-status">
        <span class="status-dot not-visited-dot"></span>
        Not Visited
    </div>
    <div class="summary-number">{not_visited}</div>
</div>

</div>
        """,
        unsafe_allow_html=True,
    )
