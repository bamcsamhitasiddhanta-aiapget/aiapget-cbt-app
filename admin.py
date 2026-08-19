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
from database import (
    add_question_tag,
    execute,
    get_connection,
    get_question_tags,
    remove_question_tag,
)
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        [
            "📥 Import Excel",
            "📜 Import PYQ",
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
                            tag.strip().title()
                            for tag in tags.split(",")
                            if tag.strip()
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
    # TAB 2 - IMPORT PREVIOUS YEAR QUESTIONS
    # =====================================================

    with tab2:
        st.subheader("📜 Import Previous Year Questions")

        st.info(
            "PYQ questions are stored separately from regular questions "
            "and will not appear in Subject Tests, Samhita Tests, or Full Mock Tests."
        )

        uploaded_pyq = st.file_uploader(
            "Choose PYQ Excel File",
            type=["xlsx"],
            key="pyq_excel_upload",
        )

        if uploaded_pyq is not None:
            try:
                pyq_df = pd.read_excel(uploaded_pyq)

                st.success(f"Loaded {len(pyq_df)} PYQ questions")

                st.dataframe(
                    pyq_df,
                    use_container_width=True,
                )

                # -----------------------------------------
                # Required columns
                # -----------------------------------------

                required_columns = [
                    "question",
                    "option1",
                    "option2",
                    "option3",
                    "option4",
                    "answer",
                    "subject",
                    "paper_year",
                    "paper_name",
                    "paper_id",
                    "paper_question_no",
                ]

                missing_columns = [
                    column
                    for column in required_columns
                    if column not in pyq_df.columns
                ]

                if missing_columns:
                    st.error("Missing required columns: " + ", ".join(missing_columns))

                else:
                    # -----------------------------------------
                    # Basic validation
                    # -----------------------------------------

                    validation_errors = []

                    for index, row in pyq_df.iterrows():
                        excel_row = index + 2

                        if pd.isna(row["question"]) or not str(row["question"]).strip():
                            validation_errors.append(
                                f"Row {excel_row}: Question is empty."
                            )

                        if pd.isna(row["paper_id"]) or not str(row["paper_id"]).strip():
                            validation_errors.append(
                                f"Row {excel_row}: paper_id is empty."
                            )

                        if pd.isna(row["paper_question_no"]):
                            validation_errors.append(
                                f"Row {excel_row}: paper_question_no is empty."
                            )

                    if validation_errors:
                        st.error("Please correct the following errors:")

                        for error in validation_errors[:20]:
                            st.write(f"• {error}")

                        if len(validation_errors) > 20:
                            st.write(f"...and {len(validation_errors) - 20} more.")

                    else:
                        # -----------------------------------------
                        # Import button
                        # -----------------------------------------

                        if st.button(
                            "📜 Import PYQs to Database",
                            use_container_width=True,
                            key="import_pyq_button",
                        ):
                            conn = None

                            try:
                                conn = get_connection()
                                cursor = conn.cursor()

                                imported = 0
                                skipped = 0

                                # ---------------------------------
                                # Process each PYQ
                                # ---------------------------------

                                for _, row in pyq_df.iterrows():
                                    question = str(row["question"]).strip()

                                    paper_id = str(row["paper_id"]).strip()

                                    paper_name = str(row["paper_name"]).strip()

                                    paper_year = int(row["paper_year"])

                                    paper_question_no = int(row["paper_question_no"])

                                    subject = str(row["subject"]).strip()

                                    option1 = str(row["option1"]).strip()

                                    option2 = str(row["option2"]).strip()

                                    option3 = str(row["option3"]).strip()

                                    option4 = str(row["option4"]).strip()

                                    answer = str(row["answer"]).strip()

                                    # Optional fields
                                    explanation = ""

                                    if "explanation" in pyq_df.columns and not pd.isna(
                                        row["explanation"]
                                    ):
                                        explanation = str(row["explanation"]).strip()

                                    image = ""

                                    if "image" in pyq_df.columns and not pd.isna(
                                        row["image"]
                                    ):
                                        image = str(row["image"]).strip()

                                    # ---------------------------------
                                    # Check duplicate PYQ
                                    #
                                    # Same question may legitimately
                                    # occur in different years.
                                    # ---------------------------------

                                    execute(
                                        cursor,
                                        """
                                        SELECT COUNT(*) AS count
                                        FROM questions
                                        WHERE question_source = ?
                                        AND paper_id = ?
                                        AND paper_question_no = ?
                                        """,
                                        (
                                            "previous_year",
                                            paper_id,
                                            paper_question_no,
                                        ),
                                    )

                                    exists = cursor.fetchone()["count"]

                                    if exists:
                                        skipped += 1
                                        continue

                                    # ---------------------------------
                                    # Generate global Question UID
                                    # ---------------------------------

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

                                    # ---------------------------------
                                    # Insert PYQ
                                    # ---------------------------------

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
                                            image,
                                            question_source,
                                            paper_id,
                                            paper_year,
                                            paper_name,
                                            paper_question_no
                                        )
                                        VALUES
                                        (
                                            ?, ?, ?, ?, ?, ?, ?, ?,
                                            ?, ?, ?, ?, ?, ?, ?
                                        )
                                        """,
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
                                            image,
                                            "previous_year",
                                            paper_id,
                                            paper_year,
                                            paper_name,
                                            paper_question_no,
                                        ),
                                    )

                                    # ---------------------------------
                                    # Import tags
                                    # ---------------------------------

                                    tags = ""

                                    if (
                                        "additional_tags" in pyq_df.columns
                                        and not pd.isna(row["additional_tags"])
                                    ):
                                        tags = str(row["additional_tags"]).strip()

                                    if tags:
                                        tag_list = [
                                            tag.strip().title()
                                            for tag in tags.split(",")
                                            if tag.strip()
                                        ]

                                        for tag in tag_list:
                                            execute(
                                                cursor,
                                                """
                                                INSERT INTO question_tags
                                                (
                                                    question_uid,
                                                    tag_name
                                                )
                                                VALUES (?, ?)
                                                ON CONFLICT
                                                (
                                                    question_uid,
                                                    tag_name
                                                )
                                                DO NOTHING
                                                """,
                                                (
                                                    question_uid,
                                                    tag,
                                                ),
                                            )

                                    imported += 1

                                # ---------------------------------
                                # Commit entire import
                                # ---------------------------------

                                conn.commit()

                                st.success(
                                    f"✅ Imported {imported} PYQs | "
                                    f"⚠️ Skipped {skipped} duplicates"
                                )

                            except Exception as e:
                                if conn is not None:
                                    conn.rollback()

                                st.error(f"❌ PYQ import failed: {e}")

                            finally:
                                if conn is not None:
                                    conn.close()

            except Exception as e:
                st.error(f"❌ Could not read PYQ Excel file: {e}")

    # =====================================================
    # TAB 3 - MANAGE QUESTIONS
    # =====================================================

    with tab3:
        st.subheader("✏️ Manage Questions")

        # =================================================
        # QUESTION TYPE
        # =================================================

        question_type = st.radio(
            "Question Type",
            [
                "Regular Questions",
                "Previous Year Questions",
                "All Questions",
            ],
            horizontal=True,
            key="manage_question_type",
        )

        conn = get_connection()
        cursor = conn.cursor()

        # =================================================
        # BUILD FILTERS
        # =================================================

        if question_type == "Previous Year Questions":
            # ---------------------------------------------
            # Get PYQ papers
            # ---------------------------------------------

            execute(
                cursor,
                """
                SELECT DISTINCT
                    paper_id,
                    paper_name,
                    paper_year
                FROM questions
                WHERE question_source = ?
                AND paper_id IS NOT NULL
                ORDER BY paper_year DESC, paper_name
                """,
                ("previous_year",),
            )

            paper_rows = cursor.fetchall()

            if not paper_rows:
                st.info("📭 No Previous Year Questions found.")

                conn.close()

            else:
                paper_options = {
                    f"{row['paper_name']} ({row['paper_year']})": row["paper_id"]
                    for row in paper_rows
                }

                selected_paper_label = st.selectbox(
                    "📜 Select Previous Year Paper",
                    list(paper_options.keys()),
                    key="manage_pyq_paper",
                )

                selected_paper_id = paper_options[selected_paper_label]

                # ---------------------------------------------
                # Get subjects for selected PYQ paper
                # ---------------------------------------------

                execute(
                    cursor,
                    """
                    SELECT DISTINCT subject
                    FROM questions
                    WHERE question_source = ?
                    AND paper_id = ?
                    ORDER BY subject
                    """,
                    (
                        "previous_year",
                        selected_paper_id,
                    ),
                )

                subjects = [row["subject"] for row in cursor.fetchall()]

                subject_options = ["All Subjects"] + subjects

                selected_subject = st.selectbox(
                    "📚 Subject",
                    subject_options,
                    key="manage_pyq_subject",
                )

                # ---------------------------------------------
                # Get questions
                # ---------------------------------------------

                if selected_subject == "All Subjects":
                    execute(
                        cursor,
                        """
                        SELECT
                            id,
                            question_uid,
                            question,
                            paper_question_no,
                            subject
                        FROM questions
                        WHERE question_source = ?
                        AND paper_id = ?
                        ORDER BY paper_question_no
                        """,
                        (
                            "previous_year",
                            selected_paper_id,
                        ),
                    )

                else:
                    execute(
                        cursor,
                        """
                        SELECT
                            id,
                            question_uid,
                            question,
                            paper_question_no,
                            subject
                        FROM questions
                        WHERE question_source = ?
                        AND paper_id = ?
                        AND subject = ?
                        ORDER BY paper_question_no
                        """,
                        (
                            "previous_year",
                            selected_paper_id,
                            selected_subject,
                        ),
                    )

                question_rows = cursor.fetchall()

                if not question_rows:
                    st.warning("No questions found.")

                else:
                    question_dict = {
                        (
                            f"Q{row['paper_question_no']} | "
                            f"{row['subject']} | "
                            f"{row['question'][:80]}"
                        ): row["id"]
                        for row in question_rows
                    }

                    selected_question = st.selectbox(
                        "Choose Question",
                        list(question_dict.keys()),
                        key="manage_pyq_question",
                    )

                    question_id = question_dict[selected_question]

                    # =========================================
                    # LOAD FULL QUESTION
                    # =========================================

                    execute(
                        cursor,
                        """
                        SELECT
                            question_uid,
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer,
                            explanation,
                            image,
                            subject,
                            question_source,
                            paper_id,
                            paper_year,
                            paper_name,
                            paper_question_no
                        FROM questions
                        WHERE id = ?
                        """,
                        (question_id,),
                    )

                    row = cursor.fetchone()

                    # =========================================
                    # PYQ INFORMATION
                    # =========================================

                    st.info(
                        f"""
                        📜 **Previous Year Question**

                        **Paper:** {row["paper_name"]}

                        **Year:** {row["paper_year"]}

                        **Original Question No.:** {row["paper_question_no"]}

                        **Subject:** {row["subject"]}

                        **UID:** {row["question_uid"]}
                        """
                    )

                    st.divider()

                    # =========================================
                    # IMAGE
                    # =========================================

                    if row["image"]:
                        if os.path.exists(row["image"]):
                            st.image(
                                row["image"],
                                width=350,
                                caption="Question Image",
                            )

                    # =========================================
                    # QUESTION
                    # =========================================

                    question = st.text_area(
                        "Question",
                        value=row["question"],
                        height=120,
                        key=f"edit_question_{question_id}",
                    )

                    # =========================================
                    # OPTIONS
                    # =========================================

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
                        answer_index = options.index(row["answer"])
                    else:
                        answer_index = 0

                    answer = st.selectbox(
                        "Correct Answer",
                        options,
                        index=answer_index,
                        key=f"edit_answer_{question_id}",
                    )

                    # =========================================
                    # EXPLANATION
                    # =========================================

                    explanation = st.text_area(
                        "Explanation",
                        value=row["explanation"] or "",
                        height=100,
                        key=f"edit_explanation_{question_id}",
                    )

                    # =========================================
                    # TAG MANAGER
                    # =========================================

                    st.divider()

                    st.subheader("🏷️ Tags")

                    question_uid = row["question_uid"]

                    tags = get_question_tags(question_uid)

                    if tags:
                        st.write("Current Tags:")

                        for tag in tags:
                            c1, c2 = st.columns([8, 1])

                            with c1:
                                st.write(f"✅ {tag}")

                            with c2:
                                if st.button(
                                    "❌",
                                    key=f"remove_{question_uid}_{tag}",
                                ):
                                    remove_question_tag(
                                        question_uid,
                                        tag,
                                    )

                                    st.rerun()

                    else:
                        st.info("No tags assigned.")

                    new_tag = st.text_input(
                        "Add New Tag",
                        key=f"new_tag_{question_uid}",
                    )

                    if st.button(
                        "➕ Add Tag",
                        key=f"add_tag_{question_uid}",
                    ):
                        if new_tag.strip():
                            add_question_tag(
                                question_uid,
                                new_tag,
                            )

                            st.success("Tag Added!")

                            st.rerun()

                    # =========================================
                    # SAVE / DELETE
                    # =========================================

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                            "💾 Save Changes",
                            key=f"save_pyq_{question_id}",
                        ):
                            execute(
                                cursor,
                                """
                                UPDATE questions
                                SET
                                    question = ?,
                                    option1 = ?,
                                    option2 = ?,
                                    option3 = ?,
                                    option4 = ?,
                                    answer = ?,
                                    explanation = ?
                                WHERE id = ?
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

                            st.success("✅ PYQ updated successfully!")

                            st.rerun()

                    with col2:
                        if st.button(
                            "🗑️ Delete PYQ",
                            key=f"delete_pyq_{question_id}",
                        ):
                            execute(
                                cursor,
                                """
                                DELETE FROM questions
                                WHERE id = ?
                                AND question_source = ?
                                """,
                                (
                                    question_id,
                                    "previous_year",
                                ),
                            )

                            conn.commit()

                            st.success("✅ PYQ deleted successfully!")

                            st.rerun()

                conn.close()

        # =================================================
        # REGULAR / ALL QUESTIONS
        # =================================================

        else:
            if question_type == "Regular Questions":
                source_condition = """
                    question_source = ?
                """
                source_params = ("regular",)

            else:
                source_condition = "1=1"
                source_params = ()

            # ---------------------------------------------
            # Load subjects
            # ---------------------------------------------

            execute(
                cursor,
                f"""
                SELECT DISTINCT subject
                FROM questions
                WHERE {source_condition}
                ORDER BY subject
                """,
                source_params,
            )

            subjects = [row["subject"] for row in cursor.fetchall()]

            if not subjects:
                st.warning("No questions found.")

                conn.close()

            else:
                selected_subject = st.selectbox(
                    "Select Subject",
                    subjects,
                    key="manage_subject",
                )

                search_text = st.text_input(
                    "🔍 Search Question",
                    key="manage_search",
                )

                if question_type == "Regular Questions":
                    execute(
                        cursor,
                        """
                        SELECT id, question
                        FROM questions
                        WHERE question_source = ?
                        AND subject = ?
                        AND question LIKE ?
                        ORDER BY id
                        """,
                        (
                            "regular",
                            selected_subject,
                            f"%{search_text}%",
                        ),
                    )

                else:
                    execute(
                        cursor,
                        """
                        SELECT id, question
                        FROM questions
                        WHERE subject = ?
                        AND question LIKE ?
                        ORDER BY id
                        """,
                        (
                            selected_subject,
                            f"%{search_text}%",
                        ),
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
                        "Choose Question",
                        list(question_dict.keys()),
                        key="manage_question",
                    )

                    question_id = question_dict[selected]

                    # =========================================
                    # LOAD QUESTION
                    # =========================================

                    execute(
                        cursor,
                        """
                        SELECT
                            question_uid,
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer,
                            explanation,
                            image,
                            subject,
                            question_source,
                            paper_id,
                            paper_year,
                            paper_name,
                            paper_question_no
                        FROM questions
                        WHERE id = ?
                        """,
                        (question_id,),
                    )

                    row = cursor.fetchone()

                    # =========================================
                    # SHOW PYQ INFO IF "ALL QUESTIONS"
                    # =========================================

                    if row["question_source"] == "previous_year":
                        st.info(
                            f"""
                            📜 **Previous Year Question**

                            **Paper:** {row["paper_name"]}

                            **Year:** {row["paper_year"]}

                            **Original Question No.:**
                            {row["paper_question_no"]}

                            **Paper ID:** {row["paper_id"]}
                            """
                        )

                    # =========================================
                    # IMAGE
                    # =========================================

                    if row["image"]:
                        if os.path.exists(row["image"]):
                            st.image(
                                row["image"],
                                width=350,
                                caption="Question Image",
                            )

                    # =========================================
                    # QUESTION
                    # =========================================

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
                        answer_index = options.index(row["answer"])
                    else:
                        answer_index = 0

                    answer = st.selectbox(
                        "Correct Answer",
                        options,
                        index=answer_index,
                        key=f"edit_answer_{question_id}",
                    )

                    explanation = st.text_area(
                        "Explanation",
                        value=row["explanation"] or "",
                        height=100,
                        key=f"edit_explanation_{question_id}",
                    )

                    # =========================================
                    # TAG MANAGER
                    # =========================================

                    st.divider()

                    st.subheader("🏷️ Tags")

                    question_uid = row["question_uid"]

                    tags = get_question_tags(question_uid)

                    if tags:
                        st.write("Current Tags:")

                        for tag in tags:
                            c1, c2 = st.columns([8, 1])

                            with c1:
                                st.write(f"✅ {tag}")

                            with c2:
                                if st.button(
                                    "❌",
                                    key=f"remove_{question_uid}_{tag}",
                                ):
                                    remove_question_tag(
                                        question_uid,
                                        tag,
                                    )

                                    st.rerun()

                    else:
                        st.info("No tags assigned.")

                    new_tag = st.text_input(
                        "Add New Tag",
                        key=f"new_tag_{question_uid}",
                    )

                    if st.button(
                        "➕ Add Tag",
                        key=f"add_tag_{question_id}",
                    ):
                        if new_tag.strip():
                            add_question_tag(
                                question_uid,
                                new_tag,
                            )

                            st.success("Tag Added!")

                            st.rerun()

                    # =========================================
                    # SAVE / DELETE
                    # =========================================

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                            "💾 Save Changes",
                            key=f"save_question_{question_id}",
                        ):
                            execute(
                                cursor,
                                """
                                UPDATE questions
                                SET
                                    question = ?,
                                    option1 = ?,
                                    option2 = ?,
                                    option3 = ?,
                                    option4 = ?,
                                    answer = ?,
                                    explanation = ?
                                WHERE id = ?
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

                            st.rerun()

                    with col2:
                        if st.button(
                            "🗑️ Delete Question",
                            key=f"delete_question_{question_id}",
                        ):
                            execute(
                                cursor,
                                "DELETE FROM questions WHERE id=?",
                                (question_id,),
                            )

                            conn.commit()

                            st.success("✅ Question deleted successfully!")

                            st.rerun()

                conn.close()

    # =====================================================
    # TAB 4 - ADD QUESTION
    # =====================================================
    with tab4:
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
    # TAB 5 - EXPORT QUESTIONS
    # =====================================================
    with tab5:
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
    # TAB 6 - STUDENT PERFORMANCE
    # =====================================================

    with tab6:
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
    with tab7:
        show_admin_students()

    with tab8:
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
