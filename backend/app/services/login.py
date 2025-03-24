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
    Verifies if the users credentials are correct and if so, establishes tokens.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Check if there are any users in the table
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        # If no users are found, return False immediately
        if user_count == 0:
            logging.info("Users table is empty, login is not allowed.")
            return False

        # Proceed to validate user
        cursor.execute("SELECT hashed_password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user is None:
            logging.info(f"User with email {email} not found in the database.")
            return False

        # Check if the password matches the stored hash
        stored_hash = user[0]
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return True
        return False

    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()
