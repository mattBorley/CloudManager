"""
Token refresh file
"""

from datetime import datetime
import jwt
from fastapi import APIRouter, HTTPException


from ..models.token_models import RefreshToken
from ..utils.token_generation import create_access_token, get_payload

router = APIRouter()


@router.post("/refresh")
async def resfresh(request: RefreshToken):
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
