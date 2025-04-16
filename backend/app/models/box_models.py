"""
Box OAuth Implementation
"""
import logging
import os

import httpx
import requests
from fastapi import HTTPException

from .user_models import get_user_id

try:
    from app.models.box_database import insert_into_box_table, get_box_accounts, update_refresh_token, remove_from_box_table
    from app.utils.token_generation import get_payload_from_access
    from app.models.oauth import OAuthBase
except ImportError:
    from ..models.box_database import insert_into_box_table, get_box_accounts, update_refresh_token, remove_from_box_table
    from ..utils.token_generation import get_payload_from_access
    from ..models.oauth import OAuthBase


BOX_API_URL = 'https://api.box.com/2.0'
TOKEN_URL = 'https://api.box.com/oauth2/token'

class BoxClass(OAuthBase):
    """
    Class for handling Box OAuth authentication
    """
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        super().__init__(client_id, client_secret, redirect_uri)

    def get_authorization_url(self) -> str:
        auth_url = f"https://account.box.com/api/oauth2/authorize?client_id={self.app_key}&redirect_uri={self.redirect_uri}&response_type=code&scope=root_readonly"
        print(f"Generated authorization URL: {auth_url}")
        return auth_url

    async def exchange_code_for_token(self, code: str):
        print(f"Exchanging code for token: {code}")
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.app_key,
            'client_secret': self.app_secret,
            'redirect_uri': self.redirect_uri,
        }
        print(f"Code: {code}\nClient ID: {self.app_key}\nClient Secret: {self.app_secret}\nRedirect URI: {self.redirect_uri}")

        async with httpx.AsyncClient() as client:
            response = await client.post(TOKEN_URL, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            response_data = response.json()
            print(f"Token exchange response: {response_data}")

            if response.status_code == 200:
                print("Token exchange successful.")
                return response_data
            else:
                error_msg = response_data.get('error_description', 'Unknown error')
                print(f"Error exchanging code for token: {error_msg}")
                raise Exception(f"Error exchanging code for token: {error_msg}")

    async def refresh_access_token(self, refresh_token: str):
        """
        Use the refresh token to obtain a new access token and refresh token.
        """
        print(f"Refreshing access token using refresh_token: {refresh_token}")
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.app_key,
            'client_secret': self.app_secret,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(TOKEN_URL, data=payload)
            response_data = response.json()
            print(f"Refresh token response: {response_data}")

            if response.status_code == 200:
                print("Token refresh successful.")
                update_refresh_token(refresh_token, response_data.get("refresh_token"))
                return response_data.get("access_token")
            else:
                error_msg = response_data.get('error_description', 'Unknown error')
                print(f"Error refreshing token: {error_msg}")
                raise HTTPException(status_code=400, detail=f"Error refreshing token: {error_msg}")

    async def get_box_data(self, local_user_id):
        box_clouds = []
        accounts = get_box_accounts(local_user_id)
        for account in accounts:
            access_token = await BoxClass.refresh_access_token(self, account.get('refresh_token'))
            data = await get_box_data_for_list(access_token)
            box_data = {
                "cloud_name": account.get("name") + " (Box)",
                "cloud_data": data
            }
            print(box_data)
            box_clouds.append(box_data)
        return box_clouds

async def box_store_credentials(local_access_token: str, refresh_token: str, cloud_name: str):
    """
    Adds Box account to the database and logs key actions.
    """
    try:
        print("Storing credentials...")
        print(f"Local access token: {local_access_token}")
        payload = get_payload_from_access(local_access_token)
        print(f"Extracted payload: {payload}")

        user_email = payload.get("sub")
        print(f"Extracted user email: {user_email}")

        local_user_id = get_user_id(user_email)
        print(f"Local user ID: {local_user_id}")

        if not local_user_id:
            print("Missing local_user_id.")
            raise HTTPException(status_code=400, detail="Missing local_user_id")
        if not refresh_token:
            print("Missing refresh_token.")
            raise HTTPException(status_code=400, detail="Missing refresh_token")
        if not cloud_name:
            print("Missing cloud_name.")
            raise HTTPException(status_code=400, detail="Missing cloud_name")

        insert_into_box_table(local_user_id, refresh_token, cloud_name)
        print("Credentials successfully stored in database.")

    except Exception as e:
        error_msg = f"Error storing credentials in cloud {cloud_name}: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        raise HTTPException(status_code=500, detail=str(e))

async def remove_box_account(cloud_name, local_access_token):
    """
    Removes account from the database and logs key actions.
    """
    payload = get_payload_from_access(local_access_token)
    user_email = payload.get("sub")

    local_user_id = get_user_id(user_email)
    remove_from_box_table(local_user_id, cloud_name[:-6])


async def get_box_data_for_list(access_token: str) -> dict:
    """
    Uses the access token to gather Box account data and file metadata,
    returning a structured response for frontend consumption, including folder structure.
    """
    # API Endpoints
    space_usage_url = "https://api.box.com/2.0/users/me"
    list_folder_url = "https://api.box.com/2.0/folders/0/items"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        # Fetch space usage data
        space_usage_response = requests.get(space_usage_url, headers=headers)
        if space_usage_response.status_code != 200:
            raise HTTPException(status_code=400,
                                detail=f"Failed to fetch storage data from Box: {space_usage_response.text}")

        space_usage_data = space_usage_response.json()
        used_storage = space_usage_data.get('space_used', 0)
        total_storage = space_usage_data.get('space_amount', 0)
        remaining_storage = total_storage - used_storage if total_storage else "Unlimited"

        # Fetch folder structure
        folder_structure = await get_folder_structure(headers)

        # Process file metadata from folder structure
        file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types = await traverse_folders(
            folder_structure
        )

        # Calculate duplicate information
        duplicate_count = sum(len(files) for files in duplicates.values() if len(files) > 1)
        storage_used_by_duplicates = sum(
            int(file.get("size", 0)) for files in duplicates.values() if len(files) > 1 for file in files
        )

        data = {
            "storage": {
                "used_storage": used_storage,
                "total_storage": total_storage if total_storage else "Unlimited",
                "remaining_storage": remaining_storage
            },
            "file_metadata": {
                "file_count": file_count,
                "largest_file": {
                    "name": largest_file.get('name', 'N/A') if largest_file else 'N/A',
                    "size": largest_file_size if largest_file else 0,
                },
                "oldest_file": {
                    "name": oldest_file.get('name', 'N/A') if oldest_file else 'N/A',
                    "created_at": oldest_file_time if oldest_file else 'N/A',
                }
            },
            "duplicates": {
                "duplicate_count": duplicate_count,
                "storage_used_by_duplicates": storage_used_by_duplicates
            },
            "sync_info": {
                "last_synced": oldest_file_time if oldest_file else 'N/A'
            },
            "file_types": file_types,  # Add file types count here
            "folder_structure": folder_structure
        }

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Box data: {str(e)}")


async def get_folder_structure(headers: dict, parent_id: str = '0') -> list:
    """
    Recursively fetches the folder structure from Box starting at the given parent ID.
    """
    folders = []
    list_folder_url = f"https://api.box.com/2.0/folders/{parent_id}/items"

    params = {
        "fields": "id,name,type,created_at,size",
        "limit": 1000  # Adjust as needed
    }

    response = requests.get(list_folder_url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to fetch folder data from Box: {response.text}")

    items = response.json().get("entries", [])

    for item in items:
        if item["type"] == "folder":
            # If item is a folder, recursively fetch its structure
            folder = {
                "name": item["name"],
                "type": "folder",
                "path": item["id"],
                "children": await get_folder_structure(headers, item["id"])
            }
            folders.append(folder)
        elif item["type"] == "file":
            # If item is a file, add it directly
            file = {
                "name": item["name"],
                "type": "file",
                "path": item["id"],
                "size": item.get("size", 0),
                "created_at": item.get("created_at", ''),
            }
            folders.append(file)

    return folders


async def traverse_folders(folders: list) -> tuple:
    """
    Traverse through the folder structure recursively and process file metadata.
    """
    file_count = 0
    largest_file = None
    largest_file_size = 0
    oldest_file = None
    oldest_file_time = None
    duplicates = {}
    file_types = {}

    for folder in folders:
        if folder['type'] == 'file':
            file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types = process_file_metadata(
                folder, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates,
                file_types
            )
        elif folder['type'] == 'folder':
            file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types = await traverse_folders(
                folder.get('children', [])
            )

    return file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types


def process_file_metadata(entry, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates,
                          file_types):
    """
    Process file metadata and update file-related statistics.
    """
    file_name = entry.get('name', '')
    file_size = entry.get('size', 0)
    created_at = entry.get('created_at', '')

    file_count += 1

    # Count file types based on extension
    file_extension = os.path.splitext(file_name)[1].lower()
    if file_extension:
        file_types[file_extension] = file_types.get(file_extension, 0) + 1

    if file_size > largest_file_size:
        largest_file = entry
        largest_file_size = file_size

    if not oldest_file_time or created_at < oldest_file_time:
        oldest_file = entry
        oldest_file_time = created_at

    if file_name in duplicates:
        duplicates[file_name].append(entry)
    else:
        duplicates[file_name] = [entry]

    return file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types