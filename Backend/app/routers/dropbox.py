"""
DropBox endpoints
"""
import logging
import os
from fastapi import Request, APIRouter, HTTPException
from starlette.responses import RedirectResponse, JSONResponse

try:
    from app.models.dropbox_models import DropboxOAuthClass
except ImportError:
    from ..models.dropbox_models import DropboxOAuthClass

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
redirect_uri = os.getenv("REDIRECT_URI")

dropbox_oauth = DropboxOAuthClass(
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
        auth_url = dropbox_oauth.get_authorization_url(session=request.session, csrf_token=csrf_token)

        return RedirectResponse(auth_url)
    except Exception as e:
        logging.error(f"Dropbox OAuth Error: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": str(e)})

@router.get("/callback")
async def dropbox_callback(request: Request):
    """
    Handle Dropbox OAuth Callback with CSRF validation
    """
    try:
        validate_csrf_token(request)

        code = request.query_params.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Missing auth code")

        query_params = dict(request.query_params)
        access_token, refresh_token, user_id = await dropbox_oauth.finish_auth(
            session=request.session, query_params=query_params
        )

        return JSONResponse(status_code=200, content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id
        })
    except Exception as e:
        logging.error(f"OAuth error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

