import eel

from db import DB_CONNECTION


@eel.expose
def insert_topic(name, language_id):
    cursor = DB_CONNECTION.cursor()
    cursor.execute("INSERT INTO Topics (nom, language_id) VALUES (?,?)", (name, language_id,))
    DB_CONNECTION.commit()
    return cursor.lastrowid


@eel.expose
def get_topic_id(name, language_id):
    cursor = DB_CONNECTION.execute("SELECT uid FROM Topics WHERE nom = ? AND language_id = ?", (name, language_id,))
    return cursor.fetchone()[0]


@eel.expose
def get_topic_name(uid, language_id):
    cursor = DB_CONNECTION.execute("SELECT nom FROM Topics WHERE uid = ? AND language_id = ?", (uid, language_id,))
    return cursor.fetchone()[0]


@eel.expose
def get_all_topics(language_id):
    cursor = DB_CONNECTION.execute("SELECT uid, nom FROM Topics WHERE language_id = ?", (language_id,))
    return cursor.fetchall()
