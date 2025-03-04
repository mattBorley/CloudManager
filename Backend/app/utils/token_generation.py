"""
Token Generation
"""

import os
import secrets
from datetime import datetime, timedelta
import jwt
from fastapi import Request, HTTPException

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

def get_payload_from_access(access_token):
    return jwt.decode(access_token, ACCESS_KEY, algorithms=[ALGORITHM])

def get_payload_from_refresh(refresh_token):
    """Decodes JWT refresh token to payload."""
    return jwt.decode(refresh_token, REFRESH_KEY, algorithms=[ALGORITHM])

def generate_csrf_token() -> str:
    """
    Generates a new CSRF token.
    """
    return secrets.token_urlsafe(32)

def generate_session_key() -> str:
    """
    Generates a new secret key.
    """
    return secrets.token_hex(32)


def validate_csrf_token(request: Request):
    """
    Validates the existing CSRF token
    """
    session_token = request.session.get('csrf_token')
    cookie_token = request.cookies.get('csrf_token')

    if not session_token or not cookie_token or session_token != cookie_token:
        raise HTTPException(status_code=403, detail="Invalid CSRF Token")

    return True