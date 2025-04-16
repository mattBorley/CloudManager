from http.client import HTTPException

from fastapi import APIRouter, Request

from ..models.box_models import BoxClass
from ..models.google_model import GoogleClass

try:
    from app.models.dropbox_models import DropboxClass
except ImportError:
    from ..models.dropbox_models import DropBoxClass

try:
    from app.models.user_models import get_user_id
except ImportError:
    from ..models.user_models import get_user_id

try:
    from app.routers.dropbox import (
        key as dropbox_key,
        secret as dropbox_secret,
        redirect_uri as dropbox_redirect_uri
    )
except ImportError:
    from ..routers.dropbox import (
        key as dropbox_key,
        secret as dropbox_secret,
        redirect_uri as dropbox_redirect_uri
    )

try:
    from app.routers.google import (
        key as google_key,
        secret as google_secret,
        redirect_uri as google_redirect_uri
    )
except ImportError:
    from ..routers.google import (
        key as google_key,
        secret as google_secret,
        redirect_uri as google_redirect_uri
    )

try:
    from app.routers.box import (
        client_id as box_client_id,
        client_secret as box_client_secret,
        redirect_uri as box_redirect_uri
    )
except ImportError:
    from ..routers.box import (
        client_id as box_client_id,
        client_secret as box_client_secret,
        redirect_uri as box_redirect_uri
    )

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
        print(f"Error while getting payload from access token: {e}")
        raise

    user_email = payload.get("sub")

    try:
        local_user_id = get_user_id(user_email)
    except Exception as e:
        print(f"Error while getting user ID: {e}")
        raise e

    clouds = []

    # Dropbox
    dropbox_data_class = DropboxClass(
        key=dropbox_key,
        secret=dropbox_secret,
        redirect_uri=dropbox_redirect_uri
    )
    try:
        dropbox_data = await dropbox_data_class.get_dropbox_data(local_user_id)
    except Exception as e:
        print(f"Error fetching Dropbox data: {e}")
        dropbox_data = None

    if dropbox_data:
        clouds = clouds + dropbox_data

    # Google
    google_data_class = GoogleClass(
        key=google_key,
        secret=google_secret,
        redirect_uri=google_redirect_uri
    )
    try:
        google_data = await google_data_class.get_google_data(local_user_id)
    except Exception as e:
        print(f"Error fetching Google data: {e}")
        google_data = None

    if google_data:
        clouds = clouds + google_data

    # Box
    box_data_class = BoxClass(
        client_id=box_client_id,
        client_secret=box_client_secret,
        redirect_uri=box_redirect_uri
    )
    try:
        box_data = await box_data_class.get_box_data(local_user_id)
    except Exception as e:
        print(f"Error fetching Box data: {e}")
        box_data = None

    if box_data:
        clouds = clouds + box_data

    return clouds