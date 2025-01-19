"""
DropBox endpoints
"""
import os
from urllib.request import Request
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse

from backend.app.models.dropbox_models import DropboxOAuthClass
from backend.app.utils.token_generation import validate_csrf_token

router = APIRouter()

key = os.getenv("DROPBOX_APP_KEY")
secret = os.getenv("DROPBOX_APP_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

dropbox_oauth_class = DropboxOAuthClass(
    key = key,
    secret = secret,
    redirect_uri = redirect_uri
)

# dropbox_manager = DropboxOAuthManager
@router.get("/authorization")
async def dropbox_authorization(request: Request, csrf_valid: bool = Depends(validate_csrf_token)):
    """
    Initiates DropBox OAuth Flow
    """
    auth_url = dropbox_oauth_class.get_authorization_url(session=request.session)
    return RedirectResponse(auth_url)

@router.get("/callback")
async def dropbox_callback(request: Request):
    """
    Finalizes DropBox OAuth Flow
    """
    try:
        access_token, user_id, _ =  dropbox_oauth_class.finish_auth(
            session=request.session, query_params=request.query_params
        )
        return {"access_token": access_token, "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")