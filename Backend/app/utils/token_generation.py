"""
Access and Refresh Token Generation
"""

import os
from datetime import datetime, timedelta
import jwt

ACCESS_KEY = os.getenv("ACCESS_KEY")
REFRESH_KEY = os.getenv("REFRESH_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24


def create_access_token(data: dict):
    """Generates a new access token."""
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, ACCESS_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Generates a new refresh token."""
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, ALGORITHM)
    return encoded_jwt


def get_payload(refresh_token):
    """Decodes JWT refresh token to payload."""
    return jwt.decode(refresh_token, REFRESH_KEY, algorithms=[ALGORITHM])
