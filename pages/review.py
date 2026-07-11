import streamlit as st


def show_review(review_data):

    st.title("📖 Review")

    st.write(f"Questions : {len(review_data)}")
