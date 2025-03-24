"""
Box endpoints
"""
import logging
import os

from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse

try:
    from app.models.box_models import BoxClass, box_store_credentials
except ImportError:
    from ..models.box_models import BoxClass, box_store_credentials

try:
    from app.utils.header_validation import check_header
except ImportError:
    from ..utils.header_validation import check_header

router = APIRouter()

client_id = os.getenv("BOX_CLIENT_ID")
client_secret = os.getenv("BOX_CLIENT_SECRET")
redirect_uri = os.getenv("BOX_REDIRECT_URI")

box_class = BoxClass(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri
)

@router.get("/authorization")
async def authorization():
    """
    Endpoint to redirect the user to the Box OAuth authorization URL.
    This URL will ask the user for permission to access their Box account.
    """
    auth_url = box_class.get_authorization_url()
    return {"auth_url": auth_url}

@router.get("/callback")
async def callback(request: Request):
    """
    Callback endpoint that handles the redirect from Box after user authorization.
    Exchanges the authorization code for an access token and refresh token.
    """
    try:
        print("Received callback request.")

        local_access_token = check_header(request.headers.get("Authorization"))
        print(f"Extracted local access token: {local_access_token}")

        code = request.query_params.get("code")


        if not code:
            print("Authorization code missing.")
            raise HTTPException(status_code=400, detail="Authorization code missing.")

        print(f"Extracted authorization code: {code}")

        cloud_name = request.query_params.get("cloud_name")
        print(f"Extracted cloud_name: {cloud_name}")

        if not cloud_name:
            print("Missing query parameter 'cloud_name'.")
            raise HTTPException(status_code=400, detail="Missing query parameter 'cloud_name'")

        tokens = await box_class.exchange_code_for_token(code)
        print(f"Received tokens: {tokens}")

        await box_store_credentials(local_access_token, tokens.get("refresh_token"), cloud_name)
        print("Stored credentials successfully.")

        return JSONResponse(status_code=200, content={"Success": True})

    except Exception as e:
        print(f"Failed to authenticate with Box: {str(e)}")
        logging.error(f"Failed to authenticate with Box: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to authenticate with Box: {str(e)}")
