def render_options(
    current_q,
    options,
    get_question_state,
    option_selector,
):
    """
    Render answer options and return the selected answer.
    """

    state = get_question_state(current_q)

    saved_answer = state["answer"]

    if saved_answer in options:
        index = options.index(saved_answer)
    else:
        index = None

    radio_key = f"q_{current_q}"

    # Reserved for future if we switch back to st.radio
    _ = radio_key
    _ = index

    answer = option_selector(
        current_q,
        options,
    )

    return answer
