import eel

from db import DB_CONNECTION


@eel.expose
def insert_language(name):
    cursor = DB_CONNECTION.cursor()
    cursor.execute("INSERT INTO Languages (name) VALUES (?)", (name,))
    DB_CONNECTION.commit()
    return cursor.lastrowid


@eel.expose
def get_language_id(name):
    cursor = DB_CONNECTION.execute("SELECT uid FROM Languages WHERE name = ?", (name,))
    return cursor.fetchone()[0]


@eel.expose
def get_language_name(uid):
    cursor = DB_CONNECTION.execute("SELECT name FROM Languages WHERE uid = ?", (uid,))
    return cursor.fetchone()[0]


@eel.expose
def get_all_languages():
    cursor = DB_CONNECTION.execute("SELECT uid, name FROM Languages")
    return cursor.fetchall()


@eel.expose
def delete_language(uid):
    cursor = DB_CONNECTION.cursor()
    cursor.execute("DELETE FROM Languages WHERE uid = ?", (uid,))
    DB_CONNECTION.commit()
