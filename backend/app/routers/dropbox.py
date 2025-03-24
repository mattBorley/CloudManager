"""
DropBox endpoints
"""
import logging
import os

from fastapi import Request, APIRouter, HTTPException
from starlette.responses import JSONResponse


try:
    from app.utils.header_validation import check_header
except ImportError:
    from ..utils.header_validation import check_header

try:
    from app.models.dropbox_models import DropboxClass, dropbox_store_credentials, get_dropbox_data_for_list
except ImportError:
    from ..models.dropbox_models import DropboxClass, dropbox_store_credentials, get_dropbox_data_for_list

try:
    from app.utils.token_generation import generate_csrf_token
except ImportError:
    from ..utils.token_generation import generate_csrf_token

try:
    from app.utils.token_validation import validate_csrf_token
except ImportError:
    from ..utils.token_validation import validate_csrf_token


router = APIRouter()

key = os.getenv("DROPBOX_APP_KEY")
secret = os.getenv("DROPBOX_APP_SECRET")
redirect_uri = os.getenv("DROPBOX_REDIRECTURL")

dropbox_class = DropboxClass(
    key=key,
    secret=secret,
    redirect_uri=redirect_uri
)

@router.get("/authorization")
async def dropbox_authorization(request: Request):
    """
    Initiate Dropbox OAuth Flow with CSRF protection
    """
    try:
        logging.info("Stared dropbox Oauth")
        csrf_token = generate_csrf_token()
        request.session["csrf_token"] = csrf_token
        auth_url = dropbox_class.get_authorization_url(session=request.session, csrf_token=csrf_token)

        return {
            "message": "Auth URL obtained",
            "success": True,
            "auth_url": auth_url,
        }
    except Exception as e:
        logging.error(f"Dropbox OAuth Error: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": str(e)})

@router.get("/callback")
async def dropbox_callback(
    request: Request,
):
    """
    Handle Dropbox OAuth Callback with CSRF validation
    """
    try:
        local_access_token = check_header(request.headers.get("Authorization"))

        body = await request.json()
        code = body.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Missing auth code")

        state = request.query_params.get("state")
        if not state:
            raise HTTPException(status_code=400, detail="Missing query parameter 'state'")

        cloud_name = request.query_params.get("cloud_name")
        if not cloud_name:
            raise HTTPException(status_code=400, detail="Missing query parameter 'cloud_name'")

        query_params = dict(request.query_params)

        access_token, refresh_token, user_id = await dropbox_class.finish_auth(
            session=request.session, query_params=query_params
        )

        if not access_token:
            raise HTTPException(status_code=400, detail="Missing access token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Missing refresh token")
        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user id")

        await dropbox_store_credentials(local_access_token, refresh_token, user_id, cloud_name)

        return JSONResponse(status_code=200, content={
            "Success": True,
        })
    except Exception as e:
        logging.error(f"Failed to authenticate with Dropbox: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to authenticate with Dropbox: {str(e)}")