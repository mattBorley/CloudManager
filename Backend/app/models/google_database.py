"""
Google model for database storage
"""
import logging

from fastapi import HTTPException
from mysql.connector import Error
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from .database import get_db_connection  # Ensure you have this function

Base = declarative_base()

class GoogleAccount(Base):
    __tablename__ = 'google_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    local_user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    def __repr__(self):
        return f"<GoogleAccount(id={self.id}, name={self.name}, refresh_token={self.refresh_token})>"


def insert_into_google_table(local_user_id, refresh_token, name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            INSERT INTO google_accounts (name, refresh_token, local_user_id)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, refresh_token, local_user_id))
        connection.commit()
    except Error as e:
        logging.error(f"Error inserting Google OAuth credentials: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def get_google_accounts(local_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT refresh_token, name FROM google_accounts WHERE local_user_id=%s
            """,
            (local_user_id,)
        )
        accounts = cursor.fetchall()
        return accounts
    except Error as e:
        logging.error(f"Couldn't retrieve Google OAuth accounts: {e}")
        raise HTTPException(status_code=500, detail="Database connection error.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

