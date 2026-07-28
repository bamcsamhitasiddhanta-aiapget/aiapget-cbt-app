import streamlit as st


def render_navigation(
    answer,
    current_q,
    total_questions,
    save_answer,
    clear_answer,
    toggle_review,
):

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("⬅ Previous", use_container_width=True):
            if st.session_state.current_q > 0:
                st.session_state.current_q -= 1
                st.rerun()

    with col2:
        if st.button(
            "🗑 Clear Response",
            use_container_width=True,
        ):
            clear_answer(
                st.session_state.current_q,
            )

            st.rerun()

    with col3:
        if st.button(
            "🟨 Save & Mark Review",
            use_container_width=True,
        ):
            if answer is None:
                st.warning("⚠ Please select an option.")

            else:
                save_answer(
                    st.session_state.current_q,
                    answer,
                )

                toggle_review(
                    st.session_state.current_q,
                )

                if st.session_state.current_q < total_questions - 1:
                    st.session_state.current_q += 1

                st.rerun()

    with col4:
        if st.button(
            "💾 Save & Next",
            use_container_width=True,
        ):
            if answer is None:
                st.warning("⚠ Please select an option.")

            else:
                save_answer(
                    st.session_state.current_q,
                    answer,
                )

                if st.session_state.current_q < total_questions - 1:
                    st.session_state.current_q += 1

                st.rerun()
    with col5:
        if st.button(
            "🟪 Mark Review & Next",
            use_container_width=True,
        ):
            if answer is not None:
                save_answer(
                    st.session_state.current_q,
                    answer,
                )

            toggle_review(
                st.session_state.current_q,
            )

            if st.session_state.current_q < total_questions - 1:
                st.session_state.current_q += 1

            st.rerun()
    st.divider()
