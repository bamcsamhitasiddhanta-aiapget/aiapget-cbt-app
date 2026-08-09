def calculate_exam_stats(questions, get_question_state):
    """
    Calculate exam-wide question statistics once.

    Returns a dictionary containing all status counts.
    """

    total = len(questions)

    answered = 0
    review = 0
    visited = 0
    answered_review = 0

    for q_no in range(total):
        state = get_question_state(q_no)

        is_visited = state.get("visited", False)
        has_answer = state.get("answer") is not None
        is_review = state.get("review", False)

        if is_visited:
            visited += 1

        if has_answer:
            answered += 1

        if is_review:
            review += 1

        if is_review and has_answer:
            answered_review += 1

    not_answered = visited - answered
    not_visited = total - visited

    percentage = int((answered / total) * 100) if total > 0 else 0

    return {
        "total": total,
        "answered": answered,
        "not_answered": not_answered,
        "review": review,
        "answered_review": answered_review,
        "visited": visited,
        "not_visited": not_visited,
        "percentage": percentage,
    }
