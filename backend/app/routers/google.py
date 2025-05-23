import logging
import os

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse

from ..utils.header_validation import check_header

try:
    from app.models.google_model import GoogleOAuth
except ImportError:
    from ..models.google_model import GoogleClass, google_store_credentials

router = APIRouter()

key = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
redirect_uri = os.getenv("GOOGLE_REDIRECTURL")
SCOPES = [os.getenv("SCOPES")]

# Initialize the Google OAuth handler
google_auth = GoogleClass(
    key=key,
    secret=secret,
    redirect_uri=redirect_uri,
)


@router.post("/callback")
async def google_oauth_callback(request: Request):
    try:

        local_access_token = check_header(request.headers.get("Authorization"))
        data = await request.json()
        code = data.get("code")
        cloud_name = data.get("cloud_name")

        if not code:
            raise HTTPException(status_code=400, detail="Missing auth code")
        if not cloud_name:
            raise HTTPException(status_code=400, detail="Missing query parameter 'cloud_name'")

        token_response = google_auth.exchange_code_for_token(code)
        if not token_response:
            raise HTTPException(status_code=400, detail="Invalid code")

        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Missing access token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Missing refresh token")

        await google_store_credentials(local_access_token, refresh_token, cloud_name)

        return JSONResponse(status_code=200, content={"Success": True})

    except Exception as e:
        print(f"Failed to authenticate with Google: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to authenticate with Google: {str(e)}")
