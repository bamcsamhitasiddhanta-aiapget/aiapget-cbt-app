import streamlit as st


def show_dashboard(student_name):

    st.title("🏠 Student Dashboard")

    st.success(f"Welcome, {student_name}")

    st.divider()

    st.write("Dashboard under construction...")
