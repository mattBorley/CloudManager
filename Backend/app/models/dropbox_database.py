"""
Dropbox model for database additions
"""
import logging

from fastapi import HTTPException
from mysql.connector import Error
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from .database import get_db_connection

Base = declarative_base()

class DropboxAccount(Base):
    __tablename__ = 'dropbox_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dropbox_user_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)

    local_user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    def __repr__(self):
        return f"<DropboxAccount(id={self.id}, dropbox_user_id={self.dropbox_user_id}, name={self.name}, refresh_token={self.refresh_token})>"


def insert_into_dropbox_table(local_user_id, dropbox_user_id, refresh_token, name):
    try:
        connection = get_db_connection()  # Ensure this returns a MySQL connection instance

        cursor = connection.cursor(dictionary=True)

        query = """
            INSERT INTO dropbox_accounts (dropbox_user_id, name, refresh_token, local_user_id)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (dropbox_user_id, name, refresh_token, local_user_id))
        connection.commit()
    except Error as e:
        # Catch any errors and log them with more details
        logging.error(f"Error occurred: {e}")
    finally:
        # Ensure that the cursor and connection are closed, even if an error occurs
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# def get_refresh_token(local_access_token):
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)
#
#         payload = get_payload_from_access(local_access_token)
#         user_email = payload['email']
#         local_user_id = get_user_id(user_email)

def get_dropbox_accounts(local_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT dropbox_user_id, refresh_token, name FROM dropbox_accounts WHERE local_user_id=%s
            """,
            (local_user_id,)
        )
        accounts = cursor.fetchall()
        return accounts
    except Error as e:
        logging.error(f"Couldn't get dropbox: {e}")
        raise HTTPException(status_code=500, detail=f"Database (dropbox) connection error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()




