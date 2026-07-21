import pandas as pd
import streamlit as st

from admin_database import get_all_students


def show_admin_students():

    st.title("👨‍🎓 Student Management")

    students = get_all_students()

    df = pd.DataFrame(students)

    st.dataframe(df, use_container_width=True, hide_index=True)
