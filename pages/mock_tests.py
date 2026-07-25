import streamlit as st


def show_mock_tests():

    st.title("🎯 Mock Tests")

    if st.button(
        "⬅ Back to Dashboard",
        use_container_width=True,
    ):
        st.session_state.student_page = "dashboard"
        st.rerun()

    st.divider()

    st.info("🚧 Mock Tests page under development")
