"""
Alembic configuration for database migrations
"""

import os
from dotenv import load_dotenv

from alembic import context
from fastapi import HTTPException
from sqlalchemy import create_engine
from mysql.connector import Error
from logging.config import fileConfig

try:
    from app.models.user_models import User
except ImportError:
    from ..app.models.user_models import User

try:
    from app.models.database import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
except ImportError:
    from ..app.models.database import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

load_dotenv()

if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError(
        "Database connection details are missing from environment variables"
    )

DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"



config = context.config
fileConfig(config.config_file_name)


def get_db_connection():
    """Gets database connection."""
    try:
        engine = create_engine(DB_URL)
        return engine.connect()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")


target_metadata = User.metadata


def run_migrations_online():
    """Run migrations in online mode."""
    connection = get_db_connection()
    try:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


run_migrations_online()
