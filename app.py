import sqlite3
import os
import sqlite3
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def login(username: str, password: str) -> Optional[User]:
    db_path = os.getenv("DATABASE_PATH", "users.db")
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, password_hash FROM users WHERE name = ?",
                (username,),
            )
            row = cur.fetchone()
            if row and verify_password(password, row["password_hash"]):
                return User(id=row["id"], name=row["name"])
    except sqlite3.Error as e:
        logger.exception("Database error during login")
    return None