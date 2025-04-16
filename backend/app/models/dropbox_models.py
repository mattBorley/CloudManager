"""
Model for Dropbox OAuth
"""
import logging
from fastapi import HTTPException
from urllib.parse import urlparse, parse_qsl, urlencode
import dropbox
import httpx
import requests
import os
from .dropbox_database import get_dropbox_accounts, remove_from_dropbox_table
from .user_models import get_user_id

try:
    from app.models.dropbox_database import DropboxAccount, insert_into_dropbox_table
except ImportError:
    from ..models.dropbox_database import DropboxAccount, insert_into_dropbox_table

try:
    from app.models.oauth import OAuthBase
except ImportError:
    from ..models.oauth import OAuthBase

try:
    from app.utils.token_generation import generate_csrf_token, get_payload_from_access
except ImportError:
    from ..utils.token_generation import generate_csrf_token, get_payload_from_access


class DropboxClass(OAuthBase):
    """
    Class for Dropbox OAuth
    """
    def __init__(self, key: str, secret: str, redirect_uri: str):
        super().__init__(key, secret, redirect_uri)

    def create_flow(self, session: dict) -> dropbox.DropboxOAuth2Flow:
        """
        Create a DropboxOAuth2Flow instance with CSRF token handling.
        """
        csrf_token = session.get("csrf_token", generate_csrf_token())
        return dropbox.DropboxOAuth2Flow(
            consumer_key=self.app_key,
            consumer_secret=self.app_secret,
            redirect_uri=self.redirect_uri,
            session=session,
            csrf_token_session_key=csrf_token,
        )

    def get_authorization_url(self, session: dict, csrf_token: str) -> str:
        """
        Generate Dropbox Authorization URL with CSRF token
        """
        session["csrf_token"] = csrf_token
        flow = self.create_flow(session)
        auth_url = flow.start()

        parsed_url = urlparse(auth_url)
        query_params = dict(parse_qsl(parsed_url.query))
        query_params["token_access_type"] = "offline"
        query_params["state"] = session[csrf_token]

        updated_query = urlencode(query_params)
        updated_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{updated_query}"

        return updated_url

    async def finish_auth(self, session: dict, query_params: dict) -> tuple:
        """
        Complete the Dropbox OAuth flow and retrieve access & refresh tokens.
        """
        print("Starting OAuth flow completion...")
        flow = self.create_flow(session)

        try:
            print("Finishing OAuth flow with provided query parameters...")
            oauth_result = flow.finish(query_params)
            access_token = oauth_result.access_token
            user_id = oauth_result.account_id
            refresh_token = getattr(oauth_result, "refresh_token", None)

            print(f"OAuth flow completed successfully. User ID: {user_id}")
            return access_token, refresh_token, user_id
        except Exception as e:
            print(f"Error during OAuth flow: {str(e)}")
            raise Exception(f"Failed to complete OAuth: {str(e)}")

    async def refresh_access_token(self, refresh_token: str) -> str:
        """
        Refresh expired access token
        """
        token_url = "https://api.dropbox.com/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.app_key,
            "client_secret": self.app_secret,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            if response.status_code != 200:
                raise Exception(f"Failed to refresh token: {response.text}")
            return response.json().get("access_token")

    async def get_dropbox_data(self, local_user_id):
        dropbox_clouds = []
        accounts = get_dropbox_accounts(local_user_id)
        for account in accounts:
            access_token = await DropboxClass.refresh_access_token(self, account.get('refresh_token'))
            data = await get_dropbox_data_for_list(access_token)
            dropbox_data = {
                "cloud_name": account.get("name") + " (Dropbox)",
                "cloud_data": data
            }
            dropbox_clouds.append(dropbox_data)
        return dropbox_clouds


async def dropbox_store_credentials(local_access_token: str, refresh_token: str, user_id: str, cloud_name: str):
    """
    Adds Dropbox account to the database and logs key actions.
    """
    try:
        payload = get_payload_from_access(local_access_token)
        user_email = payload.get("sub")

        local_user_id = get_user_id(user_email)

        if not local_user_id:
            raise HTTPException(status_code=400, detail="Missing local_user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user_id")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Missing refresh_token")
        if not cloud_name:
            raise HTTPException(status_code=400, detail="Missing cloud_name")
        insert_into_dropbox_table(local_user_id, user_id, refresh_token, cloud_name)

    except Exception as e:
        logging.error(f"Error storing credentials for user {user_id} in cloud {cloud_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def remove_dropbox_account(cloud_name, local_access_token):
    """
    Removes account from the database and logs key actions.
    """

    try:
        payload = get_payload_from_access(local_access_token)

        user_email = payload.get("sub")

        local_user_id = get_user_id(user_email)

        remove_from_dropbox_table(local_user_id, cloud_name[:-10])

    except Exception as e:
        print(f"Error occurred during dropbox account removal: {e}")



async def get_folder_structure(path: str, headers: dict) -> list:
    """
    Recursively fetches the folder structure from Dropbox, starting at the given path.
    """
    folder_structure = []
    params = {"path": path}
    while True:
        response = requests.post("https://api.dropboxapi.com/2/files/list_folder", headers=headers, json=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch folder data from Dropbox: {response.text}")

        data = response.json()
        entries = data.get('entries', [])

        for entry in entries:
            if entry['.tag'] == 'folder':
                children = await get_folder_structure(entry['path_display'], headers)
                folder_structure.append({
                    'name': entry['name'],
                    'type': 'folder',
                    'path': entry['path_display'],
                    'children': children
                })
            elif entry['.tag'] == 'file':
                folder_structure.append({
                    'name': entry['name'],
                    'type': 'file',
                    'path': entry['path_display'],
                    'size': entry.get('size', 0),
                    'client_modified': entry.get('client_modified', ''),
                })

        if not data.get('has_more', False):
            break

        params = {"cursor": data.get('cursor')}

    return folder_structure

def process_file_metadata(entry, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types):
    """
    Process file metadata and update file-related statistics.
    """
    file_name = entry.get('name', '')
    file_size = entry.get('size', 0)
    client_modified = entry.get('client_modified', '')

    file_count += 1

    file_extension = os.path.splitext(file_name)[1].lower()
    if file_extension:
        file_types[file_extension] = file_types.get(file_extension, 0) + 1

    if file_size > largest_file_size:
        largest_file = entry
        largest_file_size = file_size

    if not oldest_file_time or client_modified < oldest_file_time:
        oldest_file = entry
        oldest_file_time = client_modified

    if file_name in duplicates:
        duplicates[file_name].append(entry)
    else:
        duplicates[file_name] = [entry]

    return file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types

async def traverse_folders(folders, process_file_metadata, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types):
    """
    Traverse through the folder structure recursively and process file metadata.
    """
    for folder in folders:
        if folder['type'] == 'file':
            file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types = process_file_metadata(
                folder, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types
            )
        elif folder['type'] == 'folder':
            file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types = await traverse_folders(
                folder.get('children', []), process_file_metadata, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types
            )

    return file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types

async def get_dropbox_data_for_list(access_token: str) -> dict:
    """
    Uses the access token to gather Dropbox account data and file metadata,
    returning a structured response for frontend consumption, including the folder structure.
    """
    space_usage_url = "https://api.dropboxapi.com/2/users/get_space_usage"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        space_usage_response = requests.post(space_usage_url, headers=headers)
        if not space_usage_response.text.strip():
            raise Exception("Received empty or None response for space usage data")

        if space_usage_response.status_code != 200:
            raise Exception(f"Failed to fetch storage data from Dropbox: {space_usage_response.text}")

        storage_data = space_usage_response.json()
        used_storage = storage_data.get('used', 0)
        total_storage = storage_data.get('allocation', {}).get('allocated', 0)
        remaining_storage = total_storage - used_storage

        folder_structure = await get_folder_structure("", headers)

        file_count = 0
        largest_file = None
        largest_file_size = 0
        oldest_file = None
        oldest_file_time = None
        duplicates = {}
        file_types = {}

        file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types = await traverse_folders(
            folder_structure, process_file_metadata, file_count, largest_file, largest_file_size, oldest_file, oldest_file_time, duplicates, file_types
        )

        duplicate_count = sum(len(dupes) for dupes in duplicates.values() if len(dupes) > 1)
        storage_used_by_duplicates = sum(file.get('size', 0) for dupes in duplicates.values() if len(dupes) > 1 for file in dupes)

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
                    "modified": oldest_file_time if oldest_file else 'N/A',
                }
            },
            "duplicates": {
                "duplicate_count": duplicate_count,
                "storage_used_by_duplicates": storage_used_by_duplicates
            },
            "sync_info": {
                "last_synced": oldest_file_time if oldest_file else 'N/A'
            },
            "file_types": file_types,
            "folder_structure": folder_structure
        }

        return data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise Exception(f"Error fetching data: {str(e)}")