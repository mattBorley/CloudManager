"""
Sign Up file
"""

from fastapi import HTTPException
import mysql.connector
from ..models.database import get_db_connection


async def store_user_in_database(email, name, hashed_password):
    """
    Checks if there is no user with the given email, and if not, adds the user to the database.
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

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

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        inserted_user = cursor.fetchone()

        if inserted_user:
            return True
        else:
            raise HTTPException(status_code=500, detail="User insertion failed")

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")

    finally:
        cursor.close()
        connection.close()
