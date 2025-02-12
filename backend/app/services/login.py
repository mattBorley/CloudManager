"""
Log In File
"""

import bcrypt
import mysql.connector
from fastapi import HTTPException

from ..models.database import get_db_connection


def verify_login(email, password):
    """
    Verifies if the users credentials are correct and if so, establishes tokens.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT hashed_password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            stored_hash = user[0]
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                return {"message": "Login successful", "success": True}
            return {"message": "Invalid password - login failed", "success": False}
        return {"message": "User not found - login failed", "success": False}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()
