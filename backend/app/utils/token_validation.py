"""
Token Validation
"""
from datetime import timezone, datetime

import jwt
from fastapi import Request, HTTPException
from fastapi.params import Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from .token_generation import ALGORITHM, ACCESS_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def validate_csrf_token(request: Request):
    """
    Validates the CSRF token from the request against the stored session token.
    """
    request_csrf_token = request.query_params.get("state") or request.cookies.get("csrf_token")

    if not request_csrf_token:
        raise HTTPException(status_code=400, detail="Missing CSRF token")

    session_csrf_token = request.session.get("csrf_token")

    if not session_csrf_token:
        raise HTTPException(status_code=400, detail="CSRF token missing from session")

    if request_csrf_token != session_csrf_token:
        raise HTTPException(status_code=403, detail="CSRF token mismatch")

    return True

def validate_access_token(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, ACCESS_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")


        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):

            raise HTTPException(status_code=401, detail="Token expired")

        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")