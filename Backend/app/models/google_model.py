import os

import requests
from fastapi import HTTPException
from googleapiclient.model import BaseModel
from sqlalchemy.testing.plugin.plugin_base import logging

from .google_database import insert_into_google_table, get_google_accounts
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


    def exchange_code_for_token(self, code: str):
        """
        Exchange the authorization code for an access token and refresh token.
        """
        data = {
            "code": code,
            "client_id": self.app_key,
            "client_secret": self.app_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }

        print(f"Making POST request to {self.TOKEN_URL} with data: {data}")

        try:
            response = requests.post(self.TOKEN_URL, data=data)
            print(f"Google OAuth token exchange response status: {response.status_code}")
            print(f"Response content: {response.text}")

            if response.status_code != 200:
                print(f"Token exchange failed with status code: {response.status_code}")
                return logging.error("Token exchange failed.")

            token_data = response.json()
            print(f"Token exchange successful, received token data: {token_data}")

            if "access_token" not in token_data:
                print("Access token missing in token response.")
                raise HTTPException(status_code=400, detail="Failed to retrieve access token.")

            if "refresh_token" not in token_data:
                print("Refresh token missing in token response.")
                raise HTTPException(status_code=400, detail="Failed to retrieve refresh token.")

            if "id_token" not in token_data:
                print("ID token missing in token response.")
                raise HTTPException(status_code=400, detail="Failed to retrieve ID token.")

            return token_data
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during token exchange: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to exchange code for token: {str(e)}")

    async def refresh_access_token(self, refresh_token: str):
        """
        Use the refresh token to get a new access token.
        """
        data = {
            "client_id": self.key,
            "client_secret": self.secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(self.TOKEN_URL, data=data)

        if response.status_code != 200:
            logging.error(f"Failed to refresh access token: {response.text}")
            raise HTTPException(status_code=400, detail="Failed to refresh access token.")

        return response.json()

    async def get_google_data(self, local_user_id):
        google_clouds = []
        accounts = get_google_accounts(local_user_id)
        for account in accounts:
            access_token = await GoogleClass.refresh_access_token(self, account.get("refresh_token"))
            data = await get_google_data_for_lists(access_token)
            google_data = {
                "cloud_name": account.get("name") + " (Google Drive)",
                "cloud_data": data
            }
            print(google_data)
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


async def get_google_data_for_lists(access_token: str) -> dict:
    """
    Uses the access token to gather Google Drive account data and file metadata,
    returning a structured response for frontend consumption.
    """
    GOOGLE_DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"
    GOOGLE_DRIVE_ABOUT_URL = "https://www.googleapis.com/drive/v3/about?fields=storageQuota"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        storage_response = requests.get(GOOGLE_DRIVE_ABOUT_URL, headers=headers)

        if storage_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch Google Drive storage data: {storage_response.text}")

        storage_data = storage_response.json().get("storageQuota", {})

        used_storage = int(storage_data.get("usage", 0))
        total_storage = int(storage_data.get("limit", 0))  # Some accounts may not have a limit
        remaining_storage = total_storage - used_storage if total_storage else "Unlimited"

        params = {
            "q": "trashed = false",  # Only get files that are NOT in the trash
            "fields": "files(id, name, size, modifiedTime, parents, mimeType)",
            "pageSize": 1000,  # Adjust based on your needs
        }

        file_response = requests.get(GOOGLE_DRIVE_FILES_URL, headers=headers, params=params)

        if file_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch Google Drive files: {file_response.text}")

        files = file_response.json().get("files", [])

        file_count = len(files)
        largest_file = None
        largest_file_size = 0
        oldest_file = None
        oldest_file_time = None
        duplicates = {}

        for entry in files:
            file_name = entry.get("name", "")
            file_size = int(entry.get("size", 0)) if entry.get("size") else 0
            modified_time = entry.get("modifiedTime", "")

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
            }
        }

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Google Drive data: {str(e)}")