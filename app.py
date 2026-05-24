# app.py
import os
import logging
import sqlite3
from dataclasses import dataclass
from typing import Optional

import bcrypt   # pip install bcrypt

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class User:
    id: int
    username: str


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_connection() -> sqlite3.Connection:
    """Create a new DB connection using the path from the environment."""
    db_path = os.getenv("DATABASE_PATH", "users.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _hash_password(plain: str) -> bytes:
    """Hash a plain‑text password for storage."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())


def _verify_password(plain: str, hashed: bytes) -> bool:
    """Constant‑time password verification."""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed)
    except ValueError:
        # malformed hash – treat as failure
        return False


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def login(username: str, password: str) -> Optional[User]:
    """
    Authenticate a user.

    Parameters
    ----------
    username: str
        The user’s login name.
    password: str
        The plain‑text password supplied by the caller.

    Returns
    -------
    Optional[User]
        ``User`` instance on success, ``None`` on failure.
    """
    try:
        with _get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,),
            )
            row = cur.fetchone()
            if row and _verify_password(password, row["password_hash"]):
                return User(id=row["id"], username=row["username"])
    except sqlite3.Error as exc:
        logger.exception("Database error during login")
    return None


# ----------------------------------------------------------------------
# Optional demo initialisation (run only when executed directly)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Simple one‑off demo DB creation
    DB = "demo.db"
    os.environ["DATABASE_PATH"] = DB

    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash BLOB NOT NULL
            )
            """
        )
        # Insert demo user (only if not present)
        demo_user = conn.execute(
            "SELECT 1 FROM users WHERE username = ?", ("admin",)
        ).fetchone()
        if not demo_user:
            pwd_hash = _hash_password("secret123")
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                ("admin", pwd_hash),
            )
            conn.commit()
            logger.info("Demo user created")
        else:
            logger.info("Demo user already exists")

    # Manual test runs
    print("=== Successful login ===")
    print(login("admin", "secret123"))

    print("\n=== Failed login (SQL injection attempt) ===")
    print(login("admin' --", "anything"))