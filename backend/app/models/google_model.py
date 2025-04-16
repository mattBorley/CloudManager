import os

import requests
from fastapi import HTTPException
from googleapiclient.model import BaseModel
from sqlalchemy.testing.plugin.plugin_base import logging

from .google_database import insert_into_google_table, get_google_accounts, remove_from_google_table
from .user_models import get_user_id
from ..models.oauth import OAuthBase
from ..utils.token_generation import get_payload_from_access


class GoogleClass(OAuthBase):
    """
    Google OAuth implementation extending OAuthBase.
    """
    TOKEN_URL = "https://oauth2.googleapis.com/token"

    def __init__(self, key: str, secret: str, redirect_uri: str):
        super().__init__(key, secret, redirect_uri)

    def exchange_code_for_token(self, code: str) -> dict:
        """
        Exchange authorization code for access and refresh tokens.
        """
        data = {
            "code": code,
            "client_id": self.app_key,
            "client_secret": self.app_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }

        print(f"➡️ Requesting token from Google OAuth endpoint: {self.TOKEN_URL}")
        print(f"Payload: {data}")

        try:
            response = requests.post(self.TOKEN_URL, data=data)
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error during token exchange: {e}")
            raise HTTPException(status_code=500, detail="Network error during token exchange.")

        print(f"✅ Response received. Status Code: {response.status_code}")
        print(f"🔁 Raw Response Body: {response.text}")

        if response.status_code != 200:
            print(f"❌ Token exchange failed. Status: {response.status_code}, Body: {response.text}")
            raise HTTPException(status_code=400, detail="Failed to exchange code for tokens.")

        try:
            token_data = response.json()
        except ValueError:
            print("❌ Invalid JSON response from token endpoint.")
            raise HTTPException(status_code=500, detail="Invalid JSON from Google token exchange.")

        required_keys = ["access_token", "refresh_token", "id_token"]
        missing = [k for k in required_keys if k not in token_data]
        if missing:
            print(f"❌ Missing fields in token response: {missing}")
            raise HTTPException(status_code=400, detail=f"Missing fields in token response: {', '.join(missing)}")

        print("✅ Token exchange successful.")
        return {
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "id_token": token_data["id_token"],
            "expires_in": token_data.get("expires_in"),
            "scope": token_data.get("scope"),
            "token_type": token_data.get("token_type")
        }

    async def refresh_access_token(self, refresh_token: str):
        """
        Use the refresh token to get a new access token.
        """
        data = {
            "client_id": self.app_key,
            "client_secret": self.app_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(self.TOKEN_URL, data=data)

        if response.status_code != 200:
            logging.error(f"Failed to refresh access token: {response.text}")
            raise HTTPException(status_code=400, detail="Failed to refresh access token.")

        response_data = response.json()
        access_token = response_data.get('access_token')
        if access_token:
            return access_token
        else:
            raise HTTPException(status_code=400, detail="Access token not found in response.")

    async def get_google_data(self, local_user_id):
        google_clouds = []

        accounts = get_google_accounts(local_user_id)

        for account in accounts:
            account_name = account.get("name")
            refresh_token = account.get("refresh_token")

            try:
                access_token = await GoogleClass.refresh_access_token(self, refresh_token)
            except Exception as e:
                print(f"Error refreshing access token for account: {account_name}. Error: {e}")
                continue  # Skip to the next account if there is an issue with this one

            try:
                data = await get_google_data_for_lists(access_token)
            except Exception as e:
                print(f"Error fetching Google Drive data for account: {account_name}. Error: {e}")
                data = {}

            google_data = {
                "cloud_name": f"{account_name} (Google Drive)",
                "cloud_data": data
            }

            google_clouds.append(google_data)

        return google_clouds


async def google_store_credentials(local_access_token: str, refresh_token: str, cloud_name: str):
    payload = get_payload_from_access(local_access_token)
    user_email = payload.get("sub")

    local_user_id = get_user_id(user_email)

    if not local_user_id:
        raise HTTPException(status_code=400, detail="Missing local_user_id")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")
    if not cloud_name:
        raise HTTPException(status_code=400, detail="Missing cloud_name")
    insert_into_google_table(local_user_id, refresh_token, cloud_name)

async def remove_google_account(cloud_name, local_access_token):
    """
    Removes account from the database and logs key actions.
    """
    payload = get_payload_from_access(local_access_token)
    user_email = payload.get("sub")

    local_user_id = get_user_id(user_email)
    remove_from_google_table(local_user_id, cloud_name[:-15])


import requests
from fastapi import HTTPException


async def get_google_data_for_lists(access_token: str) -> dict:
    """
    Uses the access token to gather Google Drive account data and file metadata,
    returning a structured response for frontend consumption, including folder structure.
    """
    GOOGLE_DRIVE_ABOUT_URL = "https://www.googleapis.com/drive/v3/about?fields=storageQuota"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        # Fetch storage usage data
        storage_response = requests.get(GOOGLE_DRIVE_ABOUT_URL, headers=headers)
        if storage_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch Google Drive storage data: {storage_response.text}")

        storage_data = storage_response.json().get("storageQuota", {})
        used_storage = int(storage_data.get("usage", 0))
        total_storage = int(storage_data.get("limit", 0))  # Some accounts may not have a limit
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
                    "name": largest_file.get("name", "N/A") if largest_file else "N/A",
                    "size": largest_file_size if largest_file else 0,
                },
                "oldest_file": {
                    "name": oldest_file.get("name", "N/A") if oldest_file else "N/A",
                    "modified": oldest_file_time if oldest_file else "N/A",
                }
            },
            "duplicates": {
                "duplicate_count": duplicate_count,
                "storage_used_by_duplicates": storage_used_by_duplicates
            },
            "sync_info": {
                "last_synced": oldest_file_time if oldest_file else "N/A"
            },
            "file_types": file_types,
            "folder_structure": folder_structure
        }

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Google Drive data: {str(e)}")


async def get_folder_structure(headers: dict, parent_id: str = 'root') -> list:
    """
    Recursively fetches the folder structure from Google Drive starting at the given parent ID.
    """
    folders = []
    GOOGLE_DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"

    params = {
        "q": f"'{parent_id}' in parents and trashed = false",
        "fields": "files(id, name, mimeType, parents)",
        "pageSize": 1000
    }

    response = requests.get(GOOGLE_DRIVE_FILES_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to fetch folder data from Google Drive: {response.text}")

    items = response.json().get("files", [])

    for item in items:
        if item["mimeType"] == "application/vnd.google-apps.folder":
            # If item is a folder, recursively fetch its structure
            folder = {
                "name": item["name"],
                "type": "folder",
                "path": item["id"],
                "children": await get_folder_structure(headers, item["id"])
            }
            folders.append(folder)
        else:
            # If item is a file, add it directly
            file = {
                "name": item["name"],
                "type": "file",
                "path": item["id"],
                "size": item.get("size", 0),
                "client_modified": item.get("modifiedTime", ''),
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
                folder, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types
            )
        elif folder['type'] == 'folder':
            file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types = await traverse_folders(
                folder.get('children', [])
            )

    return file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types


def process_file_metadata(entry, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types):
    """
    Process file metadata and update file-related statistics.
    """
    file_name = entry.get('name', '')
    file_size = entry.get('size', 0)
    modified_time = entry.get('client_modified', '')

    file_count += 1

    if file_size > largest_file_size:
        largest_file = entry
        largest_file_size = file_size

    if not oldest_file_time or modified_time < oldest_file_time:
        oldest_file = entry
        oldest_file_time = modified_time

    if file_name in duplicates:
        duplicates[file_name].append(entry)
    else:
        duplicates[file_name] = [entry]

    file_extension = file_name.split('.')[-1].lower() if '.' in file_name else ''
    if file_extension:
        file_types[file_extension] = file_types.get(file_extension, 0) + 1

    return file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types
