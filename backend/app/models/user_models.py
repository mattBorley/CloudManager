"""
Models for SQLAlchemy and for User endpoints
"""
import logging

from fastapi import HTTPException
from mysql.connector import Error
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from .database import get_db_connection

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for database migrations
    """
    __tablename__ = "users"  # Table name in the database

    # Define columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True, default=func.current_timestamp())

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, created_at={self.created_at})>"


# Define the request model to validate the data sent from the client
class SignUpRequest(BaseModel):
    """
    Model for sign up request
    """
    email: str
    name: str
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    """
    Model for login request
    """
    email: str
    password: str


def get_user_id(email):
    logging.info("Email: " + email)
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(f"SELECT id FROM users WHERE email='{email}'")
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        local_user_id = user["id"]
        logging.info(f"Local user id: {local_user_id}")

        return local_user_id
    except Error as e:
        logging.error(f"Couldn't get user id: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()