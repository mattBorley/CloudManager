"""
Dropbox model for database additions
"""
from webbrowser import Error

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from .database import get_db_connection

Base = declarative_base()

class DropboxAccount(Base):
    __tablename__ = 'dropbox_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dropbox_user_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)

    # Foreign key constraint to the users table
    local_user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    def __repr__(self):
        return f"<DropboxAccount(id={self.id}, dropbox_user_id={self.dropbox_user_id}, name={self.name}, refresh_token={self.refresh_token})>"

def insert_into_dropbox_table(local_user_id, dropbox_user_id, refresh_token, name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO dropbox_accounts (dropbox_user_id, name, refresh_token, local_user_id)
            VALUES (%s, %s, %s, %s)
            """,
            (dropbox_user_id, name, refresh_token, local_user_id)
        )
        connection.commit()
    except Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

