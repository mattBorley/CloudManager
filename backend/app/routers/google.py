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


@router.get("/callback")
async def google_oauth_callback(request: Request):
    try:
        print("Google OAuth callback received.")

        # Check for the Authorization header
        local_access_token = check_header(request.headers.get("Authorization"))
        print(f"Authorization header found: {local_access_token is not None}")

        # Get the 'code' query parameter
        code = request.query_params.get("code")
        if not code:
            print("Missing authorization code.")
            raise HTTPException(status_code=400, detail="Missing auth code")
        print(f"Received code: {code}")

        # Get the 'cloud_name' query parameter
        cloud_name = request.query_params.get("cloud_name")
        if not cloud_name:
            print("Missing cloud_name parameter.")
            raise HTTPException(status_code=400, detail="Missing query parameter 'cloud_name'")
        print(f"Received cloud_name: {cloud_name}")

        # Exchange the code for a token
        print("Exchanging code for token...")
        token_response = google_auth.exchange_code_for_token(code)
        print(f"Token exchange response: {token_response}")

        if not token_response:
            print("Token exchange failed.")
            raise HTTPException(status_code=400, detail="Invalid code")

        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")

        if not access_token:
            print("Missing access token in response.")
            raise HTTPException(status_code=400, detail="Missing access token")
        print(f"Access token received: {access_token}")

        if not refresh_token:
            print("Missing refresh token in response.")
            raise HTTPException(status_code=400, detail="Missing refresh token")
        print(f"Refresh token received: {refresh_token}")

        # Store the credentials (could be a database or some external storage)
        await google_store_credentials(local_access_token, refresh_token, cloud_name)
        print("Credentials stored successfully.")

        # Log success and return response
        print("Google authentication successful.")
        return JSONResponse(status_code=200, content={"Success": True})

    except Exception as e:
        print(f"Failed to authenticate with Google: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to authenticate with Google: {str(e)}")
