import streamlit as st

from exam_db import get_attempt_review


def show_attempt_review(
    attempt_id,
):
    rows = get_attempt_review(attempt_id)

    st.title("📖 Attempt Review")
    st.write(f"Attempt ID : {attempt_id}")

    st.divider()
    if st.button(
        "🏠 Back to Dashboard",
        use_container_width=True,
    ):
        st.session_state.test_state = "home"

        if "review_attempt_id" in st.session_state:
            del st.session_state.review_attempt_id

        st.rerun()

    for q in rows:
        st.caption(f"📚 {q[1]}")

        if q[9]:
            st.success("✅ Correct")
        else:
            st.error("❌ Wrong")
        st.subheader(f"Question {q[0]}")

        st.write(q[2])

        options = [
            q[3],
            q[4],
            q[5],
            q[6],
        ]

        for option in options:
            if option == q[8]:
                st.success(f"✅ {option}")

            elif option == q[7]:
                st.error(f"❌ {option}")

            else:
                st.write(f"⚪ {option}")

                st.write("Explanation :", q[10])

                st.divider()
