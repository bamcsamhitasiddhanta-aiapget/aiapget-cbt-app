from exam_db import get_attempt_review

rows = get_attempt_review(68)

for row in rows:
    print(row)
