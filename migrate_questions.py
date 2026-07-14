import json
import os

from database import get_connection

conn = get_connection()
cursor = conn.cursor()

for filename in os.listdir("questions"):
    if filename.endswith(".json"):
        filepath = os.path.join("questions", filename)

        with open(filepath, "r", encoding="utf-8") as f:
            questions = json.load(f)

        for q in questions:
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
                    q["subject"],
                    q["question"],
                    q["options"][0],
                    q["options"][1],
                    q["options"][2],
                    q["options"][3],
                    q["answer"],
                    q["explanation"],
                ),
            )

conn.commit()
conn.close()

print("✅ All JSON questions migrated to SQLite successfully!")
