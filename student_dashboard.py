import streamlit as st


def dashboard_card(icon, title, description, button_text, page_key):

    st.markdown(
        f"""
        <div style="
            border:1px solid #ddd;
            border-radius:12px;
            padding:20px;
            margin-bottom:15px;
            background-color:#fafafa;
        ">
            <h3>{icon} {title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(button_text, key=page_key, use_container_width=True):
        st.session_state.student_page = page_key
        st.rerun()


def show_student_dashboard(student_name):

    st.title("🎓 AIAPGET CBT Practice Test")

    st.markdown(
        f"""
### Welcome, **{student_name}**

Practice consistently. Success in AIAPGET comes one test at a time.
"""
    )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            label="Tests Attempted",
            value="0",
        )

    with c2:
        st.metric(
            label="Average Score",
            value="0%",
        )

    with c3:
        st.metric(
            label="Highest Score",
            value="0%",
        )

    with c4:
        st.metric(
            label="Last Test",
            value="-",
        )

    st.divider()

    dashboard_card(
        "📘",
        "Subject Tests",
        "Practice individual subjects with a timed CBT examination.",
        "Start Subject Tests",
        "subject_tests",
    )

    dashboard_card(
        "📖",
        "Samhita Tests",
        "Practice Charaka, Sushruta, Ashtanga Hridaya and other Samhitas.",
        "Start Samhita Tests",
        "samhita_tests",
    )

    dashboard_card(
        "🎯",
        "Mock Tests",
        "Attempt a complete AIAPGET-style mock examination.",
        "Start Mock Test",
        "mock_tests",
    )

    dashboard_card(
        "📊",
        "My Results",
        "View your previous test attempts and performance.",
        "View Results",
        "results",
    )

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.student_page = None
        st.rerun()
