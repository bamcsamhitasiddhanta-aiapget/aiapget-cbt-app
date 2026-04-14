import streamlit as st
import json
import time
import pandas as pd
st.markdown("""
<style>
section[data-testid="stSidebar"] button {
    width: 100%;
    padding: 4px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)
# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

# Get unique subjects
subjects = list(set(q["subject"] for q in questions))
subjects.append("Full Mock Test")

# Single selectbox ONLY
import random

selected_subject = st.selectbox("Select Subject", subjects, key="subject_select")

# Filter logic
if selected_subject == "Full Mock Test":
    if "mock_questions" not in st.session_state or st.session_state.mock_questions is None:
        temp = questions.copy()
        random.shuffle(temp)
        st.session_state.mock_questions = temp[:100]

    questions = st.session_state.mock_questions

else:
    questions = [q for q in questions if q["subject"] == selected_subject]
    st.session_state.mock_questions = None

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
col1 = st.container()

st.sidebar.markdown("## ⏳ Timer")
st.sidebar.write(f"{mins}:{secs:02d}")

st.sidebar.markdown("## Questions")

# Detect screen size indirectly (simple approach)
num_cols = 2   # works best for mobile + desktop sidebar

for i in range(0, len(questions), num_cols):
    cols = st.sidebar.columns(num_cols)

    for j in range(num_cols):
        if i + j < len(questions):
            q_index = i + j

            if cols[j].button(str(q_index+1), key=f"nav{q_index}"):
                st.session_state.current_q = q_index
                st.rerun()

# Default question index
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

# Show current question
q = questions[st.session_state.current_q]

with col1:
    # Question number
    st.markdown(f"### Q{st.session_state.current_q + 1}")

    # Question text
    question_text = q["question"].replace("\n", " ").strip()
    st.markdown(question_text)

    # Options
    options = [opt.replace("\n", " ").strip() for opt in q["options"]]

    # Radio
    current_key = f"q_{st.session_state.current_q}"

    choice = st.radio(
        "",
        options,
        key=current_key,
        label_visibility="collapsed"
    )

    # Save answer
    st.session_state.answers[st.session_state.current_q] = choice

    # Navigation buttons
    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("⬅ Previous"):
            if st.session_state.current_q > 0:
                st.session_state.current_q -= 1
                st.rerun()

    with col_next:
        if st.button("Next ➡"):
            if st.session_state.current_q < len(questions) - 1:
                st.session_state.current_q += 1
                st.rerun()
                # Submit
if st.button("Submit Test") or st.session_state.submitted:
    st.session_state.submitted = True

name = st.text_input("Enter your name")

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

    # Save score
    if name:
        score_data = {"Name": name, "Score": score}
        
        try:
            df = pd.read_csv("scores.csv")
        except:
            df = pd.DataFrame(columns=["Name", "Score"])
        
        df = pd.concat([df, pd.DataFrame([score_data])], ignore_index=True)
        df.to_csv("scores.csv", index=False)

st.markdown("---")

if st.button("📊 Show Leaderboard"):
    try:
        df = pd.read_csv("scores.csv")
        df = df.sort_values(by="Score", ascending=False)
        st.subheader("🏆 Leaderboard")
        st.dataframe(df)
    except:
        st.warning("No scores available yet")