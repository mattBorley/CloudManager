import re
from os import access

from fastapi import APIRouter, Request

try:
    from app.models.dropbox_models import remove_dropbox_account
except ImportError:
    from ..models.dropbox_models import remove_dropbox_account

try:
    from app.models.google_model import remove_google_account
except ImportError:
    from ..models.google_model import remove_google_account

try:
    from app.models.box_models import remove_box_account
except ImportError:
    from ..models.box_models import remove_box_account

router = APIRouter()


@router.post('/remove')
async def remove_cloud(request: Request):

    try:
        body = await request.json()
    except Exception as e:
        print("Failed to parse JSON body:", e)
        return {"message": "Invalid JSON", "success": False}

    cloud_name = body.get("cloudName")
    access_token = body.get("access_token")

    if not cloud_name or not access_token:
        return {"message": "Missing cloudName or accessToken", "success": False}

    match = re.search(r'\((.*?)\)', cloud_name)
    cloud_type = match.group(1) if match else None

    if cloud_type == "Dropbox":
        await remove_dropbox_account(cloud_name, access_token)
    elif cloud_type == "Google Drive":
        print("Removing Google Drive account...")
        await remove_google_account(cloud_name, access_token)
    elif cloud_type == "Box":
        print("Removing Box account...")
        await remove_box_account(cloud_name, access_token)
    else:
        return {"message": "Cloud type not supported", "success": False}

    return {"message": f"Cloud '{cloud_name}' removed successfully", "success": True}
