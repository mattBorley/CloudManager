"""
Box Database Models
"""
import logging
from fastapi import HTTPException
from mysql.connector import Error
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from .database import get_db_connection

Base = declarative_base()

class BoxAccount(Base):
    __tablename__ = 'box_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    local_user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

def insert_into_box_table(local_user_id, refresh_token, name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            INSERT INTO box_accounts (name, refresh_token, local_user_id)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, refresh_token, local_user_id))
        connection.commit()
    except Exception as e:
        logging.error(f"Error inserting into Box table: {e}")
    finally:
        cursor.close()
        connection.close()

def get_box_accounts(local_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT refresh_token, name FROM box_accounts WHERE local_user_id=%s
            """,
            (local_user_id,)
        )
        accounts = cursor.fetchall()
        return accounts
    except Error as e:
        logging.error(f"Couldn't get box: {e}")
        raise HTTPException(status_code=500, detail=f"Database (Box) connection error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def update_refresh_token(old_refresh_token, new_refresh_token):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        print(
            f"Preparing to update refresh_token in box_accounts table: old_refresh_token = {old_refresh_token}, new_refresh_token = {new_refresh_token}")
        cursor.execute(
            """
            UPDATE box_accounts SET refresh_token = %s WHERE refresh_token = %s;
            """,
            (new_refresh_token, old_refresh_token)
        )
        connection.commit()


    except Error as e:
        print(f"Error occurred while updating refresh_token: {e}")
        logging.error(f"Couldn't update refresh token in box_accounts: {e}")
        raise HTTPException(status_code=500, detail=f"Database (Box) connection error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def remove_from_box_table(local_user_id, name):
    print("ID: ", local_user_id)
    print("Name: ", name)
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            DELETE FROM box_accounts
            WHERE local_user_id = %s AND name = %s
        """

        cursor.execute(query, (local_user_id, name))
        connection.commit()

        if cursor.rowcount > 0:
            logging.info(f"Successfully removed {cursor.rowcount} record(s) from box_accounts")
        else:
            logging.warning(f"No records found to remove for local_user_id: {local_user_id} and name: {name}")

    except Error as e:
        logging.error(f"Error occurred: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
