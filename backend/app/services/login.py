"""
Log In File
"""
import logging

import bcrypt
import mysql.connector
from fastapi import HTTPException

from ..models.database import get_db_connection


def verify_login(email, password):
    """
    Verifies if the user's credentials are correct and if so, returns True.
    """
    connection = get_db_connection()
    if not connection:
        return False
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            print("Users table is empty. Login attempt aborted.")
            return False

        cursor.execute("SELECT hashed_password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user is None:
            print(f"No user found with email: {email}")
            return False

        stored_hash = user[0]

        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return True
        else:
            return False

    except mysql.connector.Error as e:
        print(f"Database error during login verification: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

