import eel

from db import DB_CONNECTION


@eel.expose
def insert_exercise(name, topic_id, level):
    cursor = DB_CONNECTION.cursor()
    cursor.execute("INSERT INTO Exercises (nom, topic_id, level) VALUES (?,?,?)", (name, topic_id, level,))
    DB_CONNECTION.commit()
    return cursor.lastrowid


@eel.expose
def get_all_exercises():
    cursor = DB_CONNECTION.execute("SELECT uid, nom, topic_id, level FROM Exercises")
    return cursor.fetchall()


# get_all_exercises_of_topic
@eel.expose
def get_all_exercises_of_topic(topic_id):
    cursor = DB_CONNECTION.execute(
        "SELECT uid, nom, topic_id, level, is_solved FROM Exercises WHERE topic_id = ? ORDER BY level",
        (topic_id,))
    return cursor.fetchall()


@eel.expose
def get_exercise_id(name, topic_id):
    cursor = DB_CONNECTION.execute("SELECT uid FROM Exercises WHERE nom = ? AND topic_id = ?", (name, topic_id,))
    return cursor.fetchone()[0]


@eel.expose
def get_exercise_name(uid, topic_id):
    cursor = DB_CONNECTION.execute("SELECT nom FROM Exercises WHERE uid = ? AND topic_id = ?", (uid, topic_id,))
    return cursor.fetchone()[0]


@eel.expose
def set_is_solved(uid):
    cursor = DB_CONNECTION.cursor()
    cursor.execute("UPDATE Exercises SET is_solved = 1 WHERE uid = ?", (uid,))
    DB_CONNECTION.commit()
