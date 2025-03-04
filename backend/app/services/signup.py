"""
Sign Up file
"""

from fastapi import HTTPException
import mysql.connector
from ..models.database import get_db_connection
import logging


async def store_user_in_database(email, name, hashed_password):
    """
    Checks if there is no user with the given email, and if not, adds the user to the database.
    """
    connection = get_db_connection()
    if connection:
        logging.info("Database connection successful")
    else:
        logging.error("Database connection failed")
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    cursor = connection.cursor()

    try:
        # Log before the query execution
        logging.info(f"Checking if user with email {email} already exists.")

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            logging.warning(f"Email {email} is already registered.")
            raise HTTPException(status_code=400, detail="Email already registered")

        # Log before inserting the user
        logging.info(f"Inserting user with email {email} into the database.")

        cursor.execute(
            "INSERT INTO users (email, name, hashed_password) VALUES (%s, %s, %s)",
            (email, name, hashed_password),
        )
        connection.commit()

        logging.info(f"User with email {email} successfully registered.")
        return True
    except mysql.connector.Error as e:
        # Log the error message
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    finally:
        # Ensure cursor and connection are closed properly
        cursor.close()
        connection.close()
        logging.info("Database connection closed.")

