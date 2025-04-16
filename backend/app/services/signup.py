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
    if connection:
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    cursor = connection.cursor()

    try:
        # Before checking if user exists
        print(f"🔍 Checking if user with email '{email}' already exists...")

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            print(f"⚠️ Email '{email}' is already registered.")
            raise HTTPException(status_code=400, detail="Email already registered")

        # Before inserting the new user
        print(f"📝 Inserting new user with email '{email}' into the database...")

        cursor.execute(
            "INSERT INTO users (email, name, hashed_password) VALUES (%s, %s, %s)",
            (email, name, hashed_password),
        )
        connection.commit()

        # After insertion, verifying
        print(f"✅ Inserted user with email '{email}'. Verifying insertion...")

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        inserted_user = cursor.fetchone()

        if inserted_user:
            print(f"🎉 User '{email}' successfully registered and verified.")
            return True
        else:
            print(f"❌ User '{email}' not found in database after insertion.")
            raise HTTPException(status_code=500, detail="User insertion failed")

    except mysql.connector.Error as e:
        print(f"❌ Database error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Database error: {e}")

    finally:
        cursor.close()
        connection.close()
        print("🔒 Database connection closed.")
