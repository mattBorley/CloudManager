"""
Models for SQLAlchemy and for User endpoints
"""

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

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
