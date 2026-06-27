import sqlite3

import pandas as pd
import streamlit as st


def show_admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    st.write("Welcome, Admin!")

    # -------------------------------
    # Tabs
    # -------------------------------
    tab1, tab2, tab3 = st.tabs(
        ["📥 Import Excel", "✏️ Manage Questions", "➕ Add Question"]
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
                conn = sqlite3.connect("aiapget.db")
                cursor = conn.cursor()

                imported = 0
                skipped = 0

                for _, row in df.iterrows():
                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM questions
                        WHERE LOWER(question)=LOWER(?)
                        """,
                        (str(row["question"]).strip(),),
                    )

                    exists = cursor.fetchone()[0]

                    if exists:
                        skipped += 1
                        continue

                    cursor.execute(
                        """
                        INSERT INTO questions
                        (
                            subject,
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer,
                            explanation
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            str(row["subject"]),
                            str(row["question"]),
                            str(row["option1"]),
                            str(row["option2"]),
                            str(row["option3"]),
                            str(row["option4"]),
                            str(row["answer"]),
                            str(row["explanation"]),
                        ),
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

        conn = sqlite3.connect("aiapget.db")
        cursor = conn.cursor()
        # -------------------------------
        # Load Subjects
        # -------------------------------
        cursor.execute("""
            SELECT DISTINCT subject
            FROM questions
            ORDER BY subject
        """)

        subjects = [row[0] for row in cursor.fetchall()]

        if not subjects:
            st.warning("No subjects found in database.")
            conn.close()

        else:
            selected_subject = st.selectbox(
                "Select Subject", subjects, key="manage_subject"
            )

            search_text = st.text_input("🔍 Search Question", key="manage_search")

            cursor.execute(
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
                    f"{qid}: {qtext[:80]}": qid for qid, qtext in question_rows
                }

                selected = st.selectbox(
                    "Choose Question", list(question_dict.keys()), key="manage_question"
                )

                question_id = question_dict[selected]

                cursor.execute(
                    """
                    SELECT
                        question,
                        option1,
                        option2,
                        option3,
                        option4,
                        answer,
                        explanation
                    FROM questions
                    WHERE id = ?
                    """,
                    (question_id,),
                )

                row = cursor.fetchone()

                question = st.text_area(
                    "Question",
                    value=row[0],
                    height=120,
                    key=f"edit_question_{question_id}",
                )

                option1 = st.text_input(
                    "Option 1", value=row[1], key=f"edit_option1_{question_id}"
                )

                option2 = st.text_input(
                    "Option 2", value=row[2], key=f"edit_option2_{question_id}"
                )

                option3 = st.text_input(
                    "Option 3", value=row[3], key=f"edit_option3_{question_id}"
                )

                option4 = st.text_input(
                    "Option 4", value=row[4], key=f"edit_option4_{question_id}"
                )

                options = [
                    option1,
                    option2,
                    option3,
                    option4,
                ]

                if row[5] in options:
                    index = options.index(row[5])
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
                    value=row[6],
                    height=100,
                    key=f"edit_explanation_{question_id}",
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("💾 Save Changes", key="save_question"):
                        cursor.execute(
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
                        cursor.execute(
                            "DELETE FROM questions WHERE id=?", (question_id,)
                        )

                        conn.commit()

                        st.success("✅ Question deleted successfully!")

                        st.rerun()

            conn.close()
    # =====================================================
    # TAB 3 - ADD QUESTION
    # =====================================================
    with tab3:
        st.success("Tab 3 Loaded")
        st.subheader("➕ Add New Question")

        conn = sqlite3.connect("aiapget.db")
        cursor = conn.cursor()

        # -------------------------------
        # Existing Subjects
        # -------------------------------
        cursor.execute("""
            SELECT DISTINCT subject
            FROM questions
            ORDER BY subject
        """)
        subjects = [row[0] for row in cursor.fetchall()]

        subject_type = st.radio(
            "Subject", ["Existing Subject", "New Subject"], horizontal=True
        )

        if subject_type == "Existing Subject":
            subject = st.selectbox("Select Subject", subjects, key="subject_select")
        else:
            subject = st.text_input("Enter New Subject Name", key="new_subject")

        st.divider()

        question = st.text_area("Question", height=120, key="question")

        st.markdown("### Options")

        col1, col2 = st.columns(2)

        with col1:
            option1 = st.text_input("Option 1", key="option1")
            option2 = st.text_input("Option 2", key="option2")

        with col2:
            option3 = st.text_input("Option 3", key="option3")
            option4 = st.text_input("Option 4", key="option4")

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

        explanation = st.text_area("Explanation", height=120, key="explanation")

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
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM questions
                    WHERE LOWER(question)=LOWER(?)
                    """,
                    (question.strip(),),
                )

                exists = cursor.fetchone()[0]

                if exists:
                    st.warning("⚠️ Question already exists.")

                else:
                    cursor.execute(
                        """
                        INSERT INTO questions
                        (
                            subject,
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer,
                            explanation
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            subject.strip(),
                            question.strip(),
                            option1.strip(),
                            option2.strip(),
                            option3.strip(),
                            option4.strip(),
                            answer.strip(),
                            explanation.strip(),
                        ),
                    )

                    conn.commit()

                    st.success("✅ Question added successfully!")

                    st.balloons()

        conn.close()
