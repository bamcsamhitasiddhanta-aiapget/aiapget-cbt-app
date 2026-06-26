import streamlit as st
import pandas as pd
import sqlite3

def show_admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    st.write("Welcome, Admin!")

    # -------------------------------
    # Tabs
    # -------------------------------
    tab1, tab2, tab3 = st.tabs([
        "📥 Import Excel",
        "✏️ Manage Questions",
        "➕ Add Question"
    ])

    # =====================================================
    # TAB 1 - IMPORT EXCEL
    # =====================================================
    with tab1:

        st.subheader("📥 Import Questions from Excel")

        uploaded_file = st.file_uploader(
            "Choose Excel File",
            type=["xlsx"],
            key="excel_upload"
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
                        (str(row["question"]).strip(),)
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
                            str(row["explanation"])
                        )
                    )

                    imported += 1

                conn.commit()
                conn.close()

                st.success(
                    f"✅ Imported {imported} questions | "
                    f"⚠️ Skipped {skipped} duplicates"
                )

    # =====================================================
    # TAB 2 - MANAGE QUESTIONS
    # =====================================================
    with tab2:

        st.subheader("✏️ Manage Questions")

        conn = sqlite3.connect("aiapget.db")
        cursor = conn.cursor()

        # Get all subjects
        cursor.execute("""
            SELECT DISTINCT subject
            FROM questions
            ORDER BY subject
        """)
        subjects = [row[0] for row in cursor.fetchall()]

        selected_subject = st.selectbox(
            "Select Subject",
            subjects,
            key="manage_subject"
        )

        # Search box
        search_text = st.text_input(
            "🔍 Search Question",
            key="manage_search"
        )

        # Load matching questions
        cursor.execute("""
            SELECT id, question
            FROM questions
            WHERE subject = ?
            AND question LIKE ?
            ORDER BY id
        """, (
            selected_subject,
            f"%{search_text}%"
        ))

        question_rows = cursor.fetchall()

        if not question_rows:
            st.warning("No questions found.")
            conn.close()
        else:

            question_dict = {
                f"{qid}: {qtext[:80]}": qid
                for qid, qtext in question_rows
            }

            selected = st.selectbox(
                "Choose Question",
                list(question_dict.keys())
            )

            question_id = question_dict[selected]
            cursor.execute("""
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
        """, (question_id,))

        row = cursor.fetchone()

        question = st.text_area(
            "Question",
            row[0],
            height=120
        )

        option1 = st.text_input("Option 1", row[1])
        option2 = st.text_input("Option 2", row[2])
        option3 = st.text_input("Option 3", row[3])
        option4 = st.text_input("Option 4", row[4])

        answer = st.selectbox(
            "Correct Answer",
            [option1, option2, option3, option4],
            index=[option1, option2, option3, option4].index(row[5])
            if row[5] in [option1, option2, option3, option4]
            else 0
        )

        explanation = st.text_area(
            "Explanation",
            row[6],
            height=100
        )
        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Save Changes"):

                cursor.execute("""
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
                """, (
                    question,
                    option1,
                    option2,
                    option3,
                    option4,
                    answer,
                    explanation,
                    question_id
                ))

                conn.commit()
                st.success("✅ Question updated successfully!")

        with col2:
            if st.button("🗑️ Delete Question"):

                cursor.execute(
                    "DELETE FROM questions WHERE id=?",
                    (question_id,)
                )

                conn.commit()
                st.success("✅ Question deleted successfully!")
                st.rerun()

        conn.close()            

    # =====================================================
    # TAB 3 - ADD QUESTION
    # =====================================================
    with tab3:

        st.subheader("➕ Add New Question")

        conn = sqlite3.connect("aiapget.db")
        cursor = conn.cursor()

        # Get existing subjects
        cursor.execute("""
           SELECT DISTINCT subject
           FROM questions
           ORDER BY subject
        """)
        subject_list = [row[0] for row in cursor.fetchall()]

        subject = st.selectbox(
            "Subject",
            subject_list,
            key="add_subject"
        )

        question = st.text_area(
            "Question",
            height=120,
            key="add_question"
        )

        option1 = st.text_input("Option 1", key="add_option1")
        option2 = st.text_input("Option 2", key="add_option2")
        option3 = st.text_input("Option 3", key="add_option3")
        option4 = st.text_input("Option 4", key="add_option4")

        # Correct answer dropdown
        options = [option1, option2, option3, option4]
        valid_options = [opt for opt in options if opt.strip()]

        if valid_options:
            answer = st.selectbox(
                "Correct Answer",
                valid_options,
                key="add_answer"
           )
        else:
            answer = ""

        explanation = st.text_area(
            "Explanation",
            height=100,
            key="add_explanation"
        )

        if st.button("✅ Save Question"):

            if (
                question.strip() == ""
                or len(valid_options) < 4
                or explanation.strip() == ""
            ):
                st.error("Please fill all fields.")
            else:

                # Duplicate check
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM questions
                    WHERE LOWER(question)=LOWER(?)
                    """,
                    (question.strip(),)
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
                            subject,
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer,
                            explanation
                        )
                    )

                    conn.commit()

                    st.success("✅ Question added successfully!")

        conn.close()