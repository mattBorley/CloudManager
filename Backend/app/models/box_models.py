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
    from app.models.box_database import insert_into_box_table, get_box_accounts, update_refresh_token
    from app.utils.token_generation import get_payload_from_access
    from app.models.oauth import OAuthBase
except ImportError:
    from ..models.box_database import insert_into_box_table, get_box_accounts, update_refresh_token
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

async def get_box_data_for_list(access_token: str) -> dict:
    """
    Uses the access token to gather Box account data and file metadata,
    returning a structured response for frontend consumption.
    """
    print (access_token)

    # API Endpoints
    space_usage_url = "https://api.box.com/2.0/users/me"
    list_folder_url = "https://api.box.com/2.0/folders/0/items"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        print("Fetching space usage data from Box...")  # Logging space usage request
        space_usage_response = requests.get(space_usage_url, headers=headers)
        print(f"Space usage data response: {space_usage_response}")

        if not space_usage_response.text.strip():
            print("Received empty or None response for space usage data. Defaulting to 0.")
            used_storage = total_storage = remaining_storage = 0
        elif space_usage_response.status_code != 200:
            raise Exception(f"Failed to fetch storage data from Box: {space_usage_response.text}")
        else:
            print("Successfully fetched space usage data.")  # Success log
            try:
                storage_data = space_usage_response.json()
                used_storage = storage_data.get('space_used', 0)
                total_storage = storage_data.get('space_amount', 0)
                remaining_storage = total_storage - used_storage
            except (ValueError, KeyError) as e:
                print(f"Error parsing space usage data: {str(e)}. Defaulting to 0.")
                used_storage = total_storage = remaining_storage = 0

        print(f"Used storage: {used_storage}, Total storage: {total_storage}, Remaining storage: {remaining_storage}")  # Log space usage

        file_count = 0
        largest_file = None
        largest_file_size = 0
        oldest_file = None
        oldest_file_time = None
        duplicates = {}

        print("Fetching file metadata from Box...")  # Logging file metadata request
        # Get file metadata (recursive request to get all files)
        file_metadata_response = requests.get(list_folder_url, headers=headers, params={"fields": "id,name,size,created_at", "limit": 1000})

        if not file_metadata_response.text.strip():
            print("Received empty or None response for file metadata. Defaulting to empty file list.")
            files = []
        elif file_metadata_response.status_code != 200:
            raise Exception(f"Failed to fetch file metadata from Box: {file_metadata_response.text}")
        else:
            print("Successfully fetched file metadata.")  # Success log
            try:
                files = [entry for entry in file_metadata_response.json().get('entries', []) if entry.get('type') == 'file']
            except ValueError as e:
                print(f"Error parsing file metadata: {str(e)}. Defaulting to empty file list.")
                files = []

        print(f"Found {len(files)} files.")  # Log file count

        if files:
            for entry in files:
                file_name = entry.get('name', '')
                file_size = entry.get('size', 0)
                created_at = entry.get('created_at', '')

                file_count += 1

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

                # Log progress for every file processed
                print(f"Processing file: {file_name}, Size: {file_size}, Created at: {created_at}")

        # Log duplicate details
        duplicate_count = sum(len(duplicate_files) for duplicate_files in duplicates.values() if len(duplicate_files) > 1)
        storage_used_by_duplicates = sum(file.get('size', 0) for duplicate_files in duplicates.values() if len(duplicate_files) > 1 for file in duplicate_files)
        print(f"Found {duplicate_count} duplicates, taking up {storage_used_by_duplicates} bytes of storage.")  # Log duplicates

        # Prepare final response
        data = {
            "storage": {
                "used_storage": used_storage,
                "total_storage": total_storage,
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
            }
        }

        # Logging the structured data going into the response
        print("Preparing final response:")
        print(f"Storage: {data['storage']}")
        print(f"File Metadata: {data['file_metadata']}")
        print(f"Duplicates: {data['duplicates']}")
        print(f"Sync Info: {data['sync_info']}")

        print("Data successfully fetched and structured.")  # Success log
        return data

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error
        raise Exception(f"Error fetching data: {str(e)}")
