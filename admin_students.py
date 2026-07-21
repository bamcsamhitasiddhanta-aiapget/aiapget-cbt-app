import streamlit as st

from admin_students import show_admin_students


def show_admin_students():
    st.title("👨‍🎓 Student Management")

    st.markdown("### Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", "0")

    with col2:
        st.metric("Active Today", "0")

    with col3:
        st.metric("Blocked", "0")

    with col4:
        st.metric("Tests Taken", "0")

    st.divider()

    st.subheader("Student List")

    search = st.text_input("🔍 Search Student")

    st.info("Student table will appear here.")
