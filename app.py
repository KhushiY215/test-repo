import sqlite3


def login(username, password):

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE name=? AND password=?"

    cursor.execute(query, (username, password))

    return cursor.fetchall()