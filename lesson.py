import eel

from db import DB_CONNECTION


@eel.expose
def insert_lesson(content, topic_id):
    cursor = DB_CONNECTION.cursor()
    cursor.execute("INSERT INTO Lessons (content, topic_id) VALUES (?,?)", (content, topic_id,))
    DB_CONNECTION.commit()
    return cursor.lastrowid


@eel.expose
def get_all_lessons_from_topic(topic_id):
    cursor = DB_CONNECTION.execute("SELECT uid, content, topic_id FROM Lessons WHERE topic_id = ?", (topic_id,))
    return cursor.fetchall()


@eel.expose
def get_all_lessons():
    cursor = DB_CONNECTION.execute("SELECT uid, content, topic_id FROM Lessons")


# get_lesson_content
@eel.expose
def get_lesson_content(uid):
    cursor = DB_CONNECTION.execute("SELECT content FROM Lessons WHERE uid = ?", (uid,))
    return cursor.fetchone()[0]


# get_lesson_content_from_topic_id
@eel.expose
def get_lesson_content_from_topic_id(topic_id):
    cursor = DB_CONNECTION.execute("SELECT content FROM Lessons WHERE topic_id = ?", (topic_id,))
    return cursor.fetchall()
