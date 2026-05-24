import sqlite3
from flask import request

def search_users():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    username = request.args.get("username")

    query = f"""
        SELECT id, username, email
        FROM users
        WHERE username = '{username}'
    """

    print("Executing:", query)

    cur.execute(query)
    results = cur.fetchall()

    conn.close()
    return results