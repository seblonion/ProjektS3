import os
import sqlite3

DB_PATH = "database.db"  # Path to the SQLite database file
DB_CONNECTION = sqlite3.connect(DB_PATH)  # Global connection object


def initialize_database():
    """
    Initialize the database by reading and executing SQL statements
    from an external file (create_table.sql).
    """
    if not os.path.exists("create_table.sql"):
        raise FileNotFoundError("The file 'create_table.sql' is missing.")

    with open("create_table.sql", "r") as sql_file:
        sql_script = sql_file.read()

    print(sql_script)

    cursor = DB_CONNECTION.cursor()
    cursor.executescript(sql_script)
    DB_CONNECTION.commit()


def execute_query(query, params=None):
    """
    Execute a query on the database and return the results.
    """
    cursor = DB_CONNECTION.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    DB_CONNECTION.commit()
    return cursor.fetchall()
