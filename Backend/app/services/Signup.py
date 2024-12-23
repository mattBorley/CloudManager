from fastapi import HTTPException
import mysql.connector

# try:
#     # First, attempt to use the absolute import
from ..models.Database import get_db_connection
# except ImportError:
#     # If that fails (e.g., during reloading), use the relative import
#     from Backend.app.models.Database import get_db_connection



async def storeUserInDatabase (email, name, hash):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        cursor.execute("INSERT INTO users (email, name, hashed_password) VALUES (%s, %s, %s)",
                       (email, name, hash))
        connection.commit()
        return True
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

