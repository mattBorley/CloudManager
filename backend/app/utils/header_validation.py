"""
Header Validation
"""
import logging

from fastapi import HTTPException


def check_header(authorization: str) -> str:
    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header is missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    access_token = authorization.split("Bearer ")[1]

    logging.info(f"Local access token: {access_token}")
    return access_token