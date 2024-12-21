from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

if not DB_URL:
    raise ValueError("DB_URL environment variable not set")

def get_db_connection():
    try:
        engine =create_engine(DB_URL)
        return engine.connect()
    except Error as e:
        raise Exception(f"Database connection error: {e}")

# Load Alembic configuration
config = context.config
fileConfig(config.config_file_name)

def run_migrations_online():
    """Run migrations in online mode."""
    connection = get_db_connection()
    try:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

run_migrations_online()
