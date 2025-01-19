"""
Token Validation
"""

from fastapi import Request, HTTPException

def validate_csrf_token(request: Request):
    """
    Validates the existing CSRF token
    """
    session_token = request.session.get("csrf_token")
    cookie_token = request.cookies.get("csrf_token")

    if not session_token or not cookie_token or session_token != cookie_token:
        raise HTTPException(status_code=403, detail="Invalid CSRF Token")