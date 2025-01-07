"""
Settings file
"""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Locates .env file
    """
    database_url: str

    class Config:
        env_file = "../../../.env"


settings = Settings()
