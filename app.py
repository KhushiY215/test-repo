# vulnerable_login_demo.py
import sqlite3

# Setup demo database
conn = sqlite3.connect("demo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")

cursor.execute("DELETE FROM users")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret123')")
conn.commit()


def login(username, password):
    #  Vulnerable query (SQL Injection)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    print("Executing:", query)

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        print("Login successful")
    else:
        print("Invalid credentials")


# Normal login
login("admin", "secret123")

# SQL Injection payload
login("admin' --", "anything")