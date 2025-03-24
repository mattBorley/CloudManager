# from fastapi import HTTPException
# from sqlalchemy.dialects import mysql
#
# from backend.app.models.database import get_db_connection, logger
#
#
# def insert_dropbox_account(user_id: int, dropbox_name: str, refresh_token: str):
#     """
#     Insert a new Dropbox account linked to the user.
#     """
#     connection = get_db_connection()
#     cursor = connection.cursor()
#
#     try:
#         # Insert the Dropbox account details into the database
#         query = """
#         INSERT INTO dropbox_accounts (user_id, name, refresh_token)
#         VALUES (%s, %s, %s)
#         """
#         cursor.execute(query, (user_id, dropbox_name, refresh_token))
#         connection.commit()
#
#         # Return the last inserted ID to know which account was created
#         return cursor.lastrowid
#
#     except mysql.connector.Error as e:
#         logger.error(f"Error inserting Dropbox account: {e}")
#         raise HTTPException(status_code=400, detail=f"Error inserting Dropbox account: {e}")
#     finally:
#         cursor.close()
#         connection.close()