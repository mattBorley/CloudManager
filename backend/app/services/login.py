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
    print(f"🔍 Attempting to verify login for email: {email}")

    connection = get_db_connection()
    if connection:
        print("✅ Database connection established")
    else:
        print("❌ Failed to establish database connection")
        return False

    cursor = connection.cursor()

    try:
        # Check if there are any users in the table
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"👥 Users found in table: {user_count}")

        if user_count == 0:
            print("⚠️ Users table is empty. Login attempt aborted.")
            return False

        # Proceed to validate user
        print(f"🔎 Searching for user with email: {email}")
        cursor.execute("SELECT hashed_password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user is None:
            print(f"❌ No user found with email: {email}")
            return False

        stored_hash = user[0]
        print("🔑 User found. Verifying password...")

        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            print("✅ Password match. Login verified.")
            return True
        else:
            print("❌ Password mismatch.")
            return False

    except mysql.connector.Error as e:
        print(f"❌ Database error during login verification: {e}")
        return False

    finally:
        cursor.close()
        connection.close()
        print("🔒 Database connection closed.")

