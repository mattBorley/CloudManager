import os

from fastapi import APIRouter, HTTPException

try:
    from app.models.google_model import GoogleOAuth
except ImportError:
    from ..models.google_model import GoogleOAuth


router = APIRouter()

key = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
redirect_uri = os.getenv("GOOGLE_REDIRECTURL")
SCOPES = [os.getenv("SCOPES")]


google_auth = GoogleOAuth(
    key=key,
    secret=secret,
    redirect_uri=redirect_uri,
)


@router.get("/callback")
async def google_oauth_callback(code: str):
    try:
        token_response = google_auth.exchange_code_for_token(code)

        if not token_response:
            raise HTTPException(status_code=400, detail="Failed to retrieve tokens from Google")

        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")

        return {"access_token": access_token, "refresh_token": refresh_token}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to authenticate with Google: {str(e)}")