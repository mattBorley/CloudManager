"""
Token refresh file
"""

from datetime import datetime
import jwt
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request


from ..models.token_models import RefreshToken
from ..utils.token_generation import create_access_token, get_payload, generate_csrf_token

router = APIRouter()

@router.post("/refresh")
async def refresh(request: RefreshToken):
    """
    Refresh endpoint
    Refresh Access Token using Refresh Token
    """
    refresh_token = request.refresh_token
    try:
        payload = get_payload(refresh_token)

        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            raise HTTPException(status_code=401, detail="Refresh Token expired")

        new_access_token = create_access_token(data={"sub": payload["sub"]})
        return {"accessToken": new_access_token}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.get("/get_csrf_token")
def get_csrf_token(request: Request):
    """
    Generates new csrf token for each session.
    """
    csrf_token = generate_csrf_token()
    request.session["csrf_token"] = csrf_token

    response = JSONResponse({"csrf_token": csrf_token})
    response.set_cookie("csrf_token", csrf_token, httponly=True, secure=True, samesite="Strict")
    return response