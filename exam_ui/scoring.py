from exam_ui.exam_state import get_question_state


def calculate_result(questions):

    correct = 0
    wrong = 0
    not_answered = 0

    for q_no, q in enumerate(questions):
        state = get_question_state(q_no)

        answer = state["answer"]

        if answer is None:
            not_answered += 1

        elif answer == q["answer"]:
            correct += 1

        else:
            wrong += 1

    total = len(questions)

    score = correct

    if total == 0:
        percentage = 0
    else:
        percentage = round((score / total) * 100, 2)

    return {
        "answered": correct + wrong,
        "correct": correct,
        "wrong": wrong,
        "not_answered": not_answered,
        "score": score,
        "percentage": percentage,
    }
