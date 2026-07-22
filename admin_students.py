import streamlit as st

from admin_database import (
    block_student,
    get_all_students,
    unblock_student,
)


def show_admin_students():

    st.title("👨‍🎓 Student Management")

    students = get_all_students()

    st.subheader(f"Registered Students : {len(students)}")

    st.divider()

    header = st.columns([0.5, 1.5, 2.2, 1, 1])

    header[0].markdown("**ID**")
    header[1].markdown("**Name**")
    header[2].markdown("**Email**")
    header[3].markdown("**Status**")
    header[4].markdown("**Action**")

    st.divider()

    for student in students:
        cols = st.columns([0.5, 1.5, 2.2, 1, 1])

        cols[0].write(student["id"])
        cols[1].write(student["name"])
        cols[2].write(student["email"])

        if student["is_blocked"]:
            cols[3].error("Blocked")

            if cols[4].button("Unblock", key=f"unblock_{student['id']}"):
                unblock_student(student["id"])
                st.rerun()

        else:
            cols[3].success("Active")

            if cols[4].button("Block", key=f"block_{student['id']}"):
                block_student(student["id"])
                st.rerun()
