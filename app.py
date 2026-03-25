import streamlit as st
import json
import time

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

st.set_page_config(page_title="AIAPGET CBT", layout="wide")

st.title("🧠 AIAPGET CBT Practice Test")

# Session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Start screen
if st.session_state.start_time is None:
    st.write("### Instructions:")
    st.write("- Total Questions:", len(questions))
    st.write("- Time: 10 minutes (demo)")
    st.write("- Do not refresh during test")

    if st.button("Start Test"):
        st.session_state.start_time = time.time()
    st.stop()

# Timer
TOTAL_TIME = 600
elapsed = time.time() - st.session_state.start_time
remaining = int(TOTAL_TIME - elapsed)

if remaining <= 0:
    st.session_state.submitted = True
    st.warning("⏰ Time Up! Auto Submitted")

mins = remaining // 60
secs = remaining % 60

# Layout
col1, col2 = st.columns([3, 1])

with col2:
    st.write(f"### ⏳ {mins}:{secs:02d}")
    st.write("### Questions")
    for i in range(len(questions)):
        if st.button(f"Q{i+1}", key=f"nav{i}"):
            st.session_state.current_q = i

# Default question index
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

# Show current question
q = questions[st.session_state.current_q]

with col1:
    st.write(f"### Q{st.session_state.current_q + 1}")
    st.write(q["question"])

    choice = st.radio(
        "Select answer:",
        q["options"],
        key=f"q{st.session_state.current_q}"
    )

    st.session_state.answers[st.session_state.current_q] = choice

    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("⬅ Previous"):
            if st.session_state.current_q > 0:
                st.session_state.current_q -= 1

    with col_next:
        if st.button("Next ➡"):
            if st.session_state.current_q < len(questions) - 1:
                st.session_state.current_q += 1

# Submit
if st.button("Submit Test") or st.session_state.submitted:
    st.session_state.submitted = True

if st.session_state.submitted:
    st.subheader("📊 Results")
    score = 0

    for i, q in enumerate(questions):
        user_ans = st.session_state.answers.get(i)
        correct = q["answer"]

        if user_ans == correct:
            score += 1
            st.success(f"Q{i+1}: Correct")
        else:
            st.error(f"Q{i+1}: Wrong")

        st.write(f"Your Answer: {user_ans}")
        st.write(f"Correct Answer: {correct}")
        st.info(f"Explanation: {q['explanation']}")
        st.write("---")

    st.write(f"## 🎯 Score: {score} / {len(questions)}")