import os

import pandas as pd
import streamlit as st

from admin_database import (
    get_maintenance_mode,
    get_registration_enabled,
    set_maintenance_mode,
    set_registration_enabled,
)
from admin_students import show_admin_students
from database import execute, get_connection
from db_utils import backup_database


def show_admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    st.write("Welcome, Admin!")
    st.divider()

    if st.button(
        "🚪 Admin Logout",
        use_container_width=True,
    ):
        st.session_state.clear()
        st.rerun()
    st.divider()

    if st.button(
        "💾 Backup Database",
        use_container_width=True,
    ):
        backup_file = backup_database()

        st.success(f"Database backed up successfully!\n\n{backup_file}")

    # -------------------------------
    # Tabs
    # -------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "📥 Import Excel",
            "✏️ Manage Questions",
            "➕ Add Question",
            "📤 Export Questions",
            "👥 Student Performance",
            "🎓 Student Management",
            "⚙️ System Settings",
        ]
    )

    # =====================================================
    # TAB 1 - IMPORT EXCEL
    # =====================================================
    with tab1:
        st.subheader("📥 Import Questions from Excel")

        uploaded_file = st.file_uploader(
            "Choose Excel File", type=["xlsx"], key="excel_upload"
        )

        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)

            st.success(f"Loaded {len(df)} questions")
            st.dataframe(df, use_container_width=True)

            if st.button("📥 Import to Database"):
                conn = get_connection()
                cursor = conn.cursor()

                imported = 0
                skipped = 0

                for _, row in df.iterrows():
                    execute(
                        cursor,
                        """
                        SELECT COUNT(*) AS count
                        FROM questions
                        WHERE LOWER(question)=LOWER(?)
                        """,
                        (str(row["question"]).strip(),),
                    )

                    exists = cursor.fetchone()["count"]

                    if exists:
                        skipped += 1
                        continue

                    # Generate Question UID
                    execute(
                        cursor,
                        """
                    SELECT question_uid
                    FROM questions
                    WHERE question_uid IS NOT NULL
                    ORDER BY question_uid DESC
                    LIMIT 1
                    """,
                    )

                    last = cursor.fetchone()

                    if last:
                        next_no = int(last["question_uid"][1:]) + 1
                    else:
                        next_no = 1

                    question_uid = f"Q{next_no:06d}"

                    execute(
                        cursor,
                        """
                        INSERT INTO questions
                        (
                            question_uid,
                            subject,
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer,
                            explanation
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            question_uid,
                            str(row["subject"]).strip(),
                            str(row["question"]).strip(),
                            str(row["option1"]).strip(),
                            str(row["option2"]).strip(),
                            str(row["option3"]).strip(),
                            str(row["option4"]).strip(),
                            str(row["answer"]).strip(),
                            str(row["explanation"]).strip(),
                        ),
                    )

                    # -----------------------------
                    # Import Additional Tags
                    # -----------------------------
                    tags = str(row.get("additional_tags", "")).strip()

                    if tags and tags.lower() != "nan":
                        tag_list = [
                            tag.strip() for tag in tags.split(",") if tag.strip()
                        ]

                        for tag in tag_list:
                            execute(
                                cursor,
                                """
                                INSERT INTO question_tags
                                (question_uid, tag_name)
                                VALUES (?, ?)
                                ON CONFLICT (question_uid, tag_name) DO NOTHING
                                """,
                                (question_uid, tag),
                            )

                    imported += 1

                conn.commit()
                conn.close()

                st.success(
                    f"✅ Imported {imported} questions | ⚠️ Skipped {skipped} duplicates"
                )

    # =====================================================
    # TAB 2 - MANAGE QUESTIONS
    # =====================================================
    with tab2:
        st.subheader("✏️ Manage Questions")

        conn = get_connection()
        cursor = conn.cursor()
        # -------------------------------
        # Load Subjects
        # -------------------------------
        execute(
            cursor,
            """
            SELECT DISTINCT subject
            FROM questions
            ORDER BY subject
        """,
        )

        subjects = [row["subject"] for row in cursor.fetchall()]

        if not subjects:
            st.warning("No subjects found in database.")
            conn.close()

        else:
            selected_subject = st.selectbox(
                "Select Subject", subjects, key="manage_subject"
            )

            search_text = st.text_input("🔍 Search Question", key="manage_search")

            execute(
                cursor,
                """
                SELECT id, question
                FROM questions
                WHERE subject = ?
                AND question LIKE ?
                ORDER BY id
                """,
                (selected_subject, f"%{search_text}%"),
            )

            question_rows = cursor.fetchall()

            if not question_rows:
                st.warning("No questions found.")

            else:
                question_dict = {
                    f"{row['id']}: {row['question'][:80]}": row["id"]
                    for row in question_rows
                }

                selected = st.selectbox(
                    "Choose Question", list(question_dict.keys()), key="manage_question"
                )

                question_id = question_dict[selected]

                execute(
                    cursor,
                    """
                    SELECT
                        question,
                        option1,
                        option2,
                        option3,
                        option4,
                        answer,
                        explanation,
                        image
                    FROM questions
                    WHERE id = ?
                    """,
                    (question_id,),
                )

                row = cursor.fetchone()

                if row["image"]:
                    if os.path.exists(row["image"]):
                        st.image(
                            row["image"],
                            width=350,
                            caption="Question Image",
                        )

                question = st.text_area(
                    "Question",
                    value=row["question"],
                    height=120,
                    key=f"edit_question_{question_id}",
                )

                option1 = st.text_input(
                    "Option 1",
                    value=row["option1"],
                    key=f"edit_option1_{question_id}",
                )

                option2 = st.text_input(
                    "Option 2",
                    value=row["option2"],
                    key=f"edit_option2_{question_id}",
                )

                option3 = st.text_input(
                    "Option 3",
                    value=row["option3"],
                    key=f"edit_option3_{question_id}",
                )

                option4 = st.text_input(
                    "Option 4",
                    value=row["option4"],
                    key=f"edit_option4_{question_id}",
                )

                options = [
                    option1,
                    option2,
                    option3,
                    option4,
                ]

                if row["answer"] in options:
                    index = options.index(row["answer"])
                else:
                    index = 0

                answer = st.selectbox(
                    "Correct Answer",
                    options,
                    index=index,
                    key=f"edit_answer_{question_id}",
                )

                explanation = st.text_area(
                    "Explanation",
                    value=row["explanation"],
                    height=100,
                    key=f"edit_explanation_{question_id}",
                )
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("💾 Save Changes", key="save_question"):
                        execute(
                            cursor,
                            """
                            UPDATE questions
                            SET
                                question=?,
                                option1=?,
                                option2=?,
                                option3=?,
                                option4=?,
                                answer=?,
                                explanation=?
                            WHERE id=?
                            """,
                            (
                                question,
                                option1,
                                option2,
                                option3,
                                option4,
                                answer,
                                explanation,
                                question_id,
                            ),
                        )

                        conn.commit()

                        st.success("✅ Question updated successfully!")

                with col2:
                    if st.button("🗑️ Delete Question", key="delete_question"):
                        execute(
                            cursor, "DELETE FROM questions WHERE id=?", (question_id,)
                        )

                        conn.commit()

                        st.success("✅ Question deleted successfully!")

                        st.rerun()

            conn.close()
    # =====================================================
    # TAB 3 - ADD QUESTION
    # =====================================================
    with tab3:
        if "add_form_version" not in st.session_state:
            st.session_state.add_form_version = 0
        st.subheader("➕ Add New Question")

        conn = get_connection()
        cursor = conn.cursor()

        # -------------------------------
        # Existing Subjects
        # -------------------------------
        execute(
            cursor,
            """
            SELECT DISTINCT subject
            FROM questions
            ORDER BY subject
        """,
        )
        subjects = [row["subject"] for row in cursor.fetchall()]

        subject_type = st.radio(
            "Subject", ["Existing Subject", "New Subject"], horizontal=True
        )

        if subject_type == "Existing Subject":
            subject = st.selectbox("Select Subject", subjects, key="subject_select")
        else:
            subject = st.text_input("Enter New Subject Name", key="new_subject")

        st.divider()

        question = st.text_area(
            "Question", height=120, key=f"question_{st.session_state.add_form_version}"
        )
        st.divider()

        st.subheader("📷 Question Image")

        uploaded_image = st.file_uploader(
            "Upload Question Image",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"question_image_{st.session_state.add_form_version}",
        )

        if uploaded_image is not None:
            st.image(
                uploaded_image,
                width=300,
                caption="Preview",
            )
        st.markdown("### Options")

        col1, col2 = st.columns(2)

        with col1:
            option1 = st.text_input(
                "Option 1", key=f"option1_{st.session_state.add_form_version}"
            )
            option2 = st.text_input(
                "Option 2", key=f"option2_{st.session_state.add_form_version}"
            )

        with col2:
            option3 = st.text_input(
                "Option 3", key=f"option3_{st.session_state.add_form_version}"
            )
            option4 = st.text_input(
                "Option 4", key=f"option4_{st.session_state.add_form_version}"
            )

        st.divider()

        answer_choice = st.radio(
            "Correct Answer",
            ["Option 1", "Option 2", "Option 3", "Option 4"],
            horizontal=True,
        )

        answer_map = {
            "Option 1": option1,
            "Option 2": option2,
            "Option 3": option3,
            "Option 4": option4,
        }

        answer = answer_map[answer_choice]

        explanation = st.text_area(
            "Explanation",
            height=120,
            key=f"explanation_{st.session_state.add_form_version}",
        )

        st.divider()

        if st.button("✅ Save Question", use_container_width=True):
            if (
                subject.strip() == ""
                or question.strip() == ""
                or option1.strip() == ""
                or option2.strip() == ""
                or option3.strip() == ""
                or option4.strip() == ""
                or explanation.strip() == ""
            ):
                st.error("Please fill all fields.")

            else:
                execute(
                    cursor,
                    """
                    SELECT COUNT(*) AS count
                    FROM questions
                    WHERE LOWER(question)=LOWER(?)
                    """,
                    (question.strip(),),
                )

                exists = cursor.fetchone()["count"]

                if exists:
                    st.warning("⚠️ Question already exists.")

                else:
                    # Generate Question UID
                    execute(
                        cursor,
                        """
                        SELECT question_uid
                        FROM questions
                        WHERE question_uid IS NOT NULL
                        ORDER BY question_uid DESC
                        LIMIT 1
                    """,
                    )

                    last = cursor.fetchone()

                    if last:
                        next_no = int(last["question_uid"][1:]) + 1
                    else:
                        next_no = 1

                    question_uid = f"Q{next_no:06d}"
                    image_path = ""

                    if uploaded_image is not None:
                        os.makedirs("images/questions", exist_ok=True)

                        extension = uploaded_image.name.split(".")[-1]

                        filename = f"{question_uid}.{extension}"

                        image_path = os.path.join("images", "questions", filename)

                        with open(image_path, "wb") as f:
                            f.write(uploaded_image.getbuffer())
                    execute(
                        cursor,
                        """
                        INSERT INTO questions
                        (   
                            question_uid,
                            subject,
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer,
                            explanation,
                            image
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            question_uid,
                            subject.strip(),
                            question.strip(),
                            option1.strip(),
                            option2.strip(),
                            option3.strip(),
                            option4.strip(),
                            answer.strip(),
                            explanation.strip(),
                            image_path,
                        ),
                    )

                    conn.commit()

                    st.success("✅ Question added successfully!")

                    st.balloons()

                    st.session_state.add_form_version += 1
                    st.rerun()

        conn.close()
    # =====================================================
    # TAB 4 - EXPORT QUESTIONS
    # =====================================================
    with tab4:
        st.subheader("📤 Export Questions")
        conn = get_connection()

        cursor = conn.cursor()

        execute(
            cursor,
            """
        SELECT DISTINCT subject
        FROM questions
        ORDER BY subject
        """,
        )

        subjects = [row["subject"] for row in cursor.fetchall()]
        export_type = st.radio(
            "Export Type",
            ["All Subjects", "Selected Subject"],
            horizontal=True,
        )
        if export_type == "Selected Subject":
            selected_subject = st.selectbox("Subject", subjects, key="export_subject")

            query = """
                 SELECT
                     subject,
                     question,
                     option1,
                     option2,
                     option3,
                     option4,
                     answer,
                     explanation
                 FROM questions
                 WHERE subject=?
                 ORDER BY id
             """

            execute(
                cursor,
                query,
                (selected_subject,),
            )

            rows = cursor.fetchall()

            df = pd.DataFrame([dict(row) for row in rows])

        else:
            query = """
                SELECT
                    subject,
                    question,
                    option1,
                    option2,
                    option3,
                    option4,
                    answer,
                    explanation
                FROM questions
                ORDER BY subject,id
            """

            execute(
                cursor,
                query,
            )

            rows = cursor.fetchall()

            df = pd.DataFrame([dict(row) for row in rows])
        st.success(f"Total Questions : {len(df)}")

        st.dataframe(
            df.head(20),
            use_container_width=True,
        )
        filename = "AIAPGET_Questions.xlsx"

        if export_type == "Selected Subject":
            filename = f"{selected_subject}.xlsx"

        df.to_excel(
            filename,
            index=False,
        )

        with open(filename, "rb") as file:
            st.download_button(
                "📥 Download Excel",
                file,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        conn.close()

    # =====================================================
    # TAB 5 - STUDENT PERFORMANCE
    # =====================================================

    with tab5:
        st.subheader("👥 Student Performance")

        from exam_db import (
            get_all_students,
            get_student_summary,
        )

        students = get_all_students()

        search = st.text_input(
            "🔍 Search Student", placeholder="Enter name or email..."
        )

        if search:
            students = [
                s
                for s in students
                if search.lower() in s["name"].lower()
                or search.lower() in s["email"].lower()
            ]

        st.subheader("Registered Students")

        if not students:
            st.info("No students registered.")
        else:
            for student in students:
                summary = get_student_summary(student["email"])

                st.write(
                    f"""
            👤 {student["name"]}

            📧 {student["email"]}

            Tests : {summary["total_tests"]}

            Average : {summary["average_percentage"]} %

            Highest : {summary["highest_percentage"]} %

            Last Test : {summary["last_test"]}
            """
                )

            st.divider()
    with tab6:
        show_admin_students()

    with tab7:
        st.subheader("⚙️ System Settings")

        maintenance = get_maintenance_mode()

        if maintenance:
            st.error("🔴 Maintenance Mode is ENABLED")
        else:
            st.success("🟢 Maintenance Mode is DISABLED")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Enable Maintenance"):
                set_maintenance_mode(True)
                st.success("Maintenance Mode Enabled")
                st.rerun()

        with col2:
            if st.button("Disable Maintenance"):
                set_maintenance_mode(False)
                st.success("Maintenance Mode Disabled")
                st.rerun()

        st.subheader("📝 Student Registration")

        registration = get_registration_enabled()

        if registration:
            st.success("🟢 Registration Enabled")
        else:
            st.error("🔴 Registration Disabled")

        col1, col2 = st.columns(2)

    with col1:
        if st.button("Enable Registration"):
            set_registration_enabled(True)
            st.rerun()

    with col2:
        if st.button("Disable Registration"):
            set_registration_enabled(False)
            st.rerun()
