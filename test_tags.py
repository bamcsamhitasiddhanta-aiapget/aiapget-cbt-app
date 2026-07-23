from database import add_question_tag, get_question_tags

add_question_tag("Q000001", "Revision Test")

print(get_question_tags("Q000001"))
from database import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT current_database();")
print("Connected database:", cur.fetchone()[0])
