from http.client import HTTPException

from fastapi import APIRouter, Request

try:
    from app.models.dropbox_models import DropboxClass
except ImportError:
    from ..models.dropbox_models import DropBoxClass

try:
    from app.models.user_models import get_user_id
except ImportError:
    from ..models.user_models import get_user_id

try:
    from app.routers.dropbox import key, secret, redirect_uri
except ImportError:
    from ..routers.dropbox import key, secret, redirect_uri

try:
    from app.utils.header_validation import check_header
except ImportError:
    from ..utils.header_validation import check_header

try:
    from app.utils.token_generation import get_payload_from_access
except ImportError:
    from ..utils.token_generation import get_payload_from_access

router = APIRouter()


@router.get('/get_data')
async def get_data(request: Request):
    authorization_header = request.headers.get("Authorization")
    local_access_token = check_header(authorization_header)

    try:
        payload = get_payload_from_access(local_access_token)
    except Exception as e:
        raise

    user_email = payload.get("sub")

    try:
        local_user_id = get_user_id(user_email)
    except Exception as e:
        raise e

    clouds = []

    #Dropbox
    dropbox_data_class = DropboxClass(
        key=key,
        secret=secret,
        redirect_uri=redirect_uri
    )

    try:
        dropbox_data = await dropbox_data_class.get_dropbox_data(local_user_id)
    except Exception as e:
        dropbox_data = None

    clouds = clouds + dropbox_data

    #Google
    # google_data = get_google_data(local_user_id)

    # clouds.append(google_data)

    return clouds
