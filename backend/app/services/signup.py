"""
Sign Up file
"""

from fastapi import HTTPException
import mysql.connector
from ..models.database import get_db_connection


async def store_user_in_database(email, name, hashed_password):
    """
    Checks there is no user with email, and if not, adds user to the database.
    """
    connection = get_db_connection()
    if connection:
        print("Database connection successful")
    else:
        print("Database connection failed")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        cursor.execute(
            "INSERT INTO users (email, name, hashed_password) VALUES (%s, %s, %s)",
            (email, name, hashed_password),
        )
        connection.commit()
        return True
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()
