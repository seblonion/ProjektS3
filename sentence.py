import eel

from db import DB_CONNECTION


@eel.expose
def insert_sentence(text, answer, exercise_id):
    cursor = DB_CONNECTION.cursor()
    cursor.execute("INSERT INTO Sentences (content, answer, exercise_id) VALUES (?,?,?)", (text, answer, exercise_id,))
    DB_CONNECTION.commit()
    return cursor.lastrowid


@eel.expose
def get_all_sentences():
    cursor = DB_CONNECTION.execute("SELECT uid, content, answer, exercise_id FROM Sentences")
    return cursor.fetchall()


# get_all_sentences_of_exercise
@eel.expose
def get_all_sentences_of_exercise(exercise_id):
    cursor = DB_CONNECTION.execute("SELECT uid, content, answer, exercise_id FROM Sentences WHERE exercise_id = ?",
                                   (exercise_id,))
    return cursor.fetchall()
