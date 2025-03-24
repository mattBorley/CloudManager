"""
Model for Dropbox OAuth
"""
import logging
from fastapi import HTTPException
from urllib.parse import urlparse, parse_qsl, urlencode
import dropbox
import httpx
import requests

from .dropbox_database import get_dropbox_accounts
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
        flow = self.create_flow(session)

        try:
            oauth_result = flow.finish(query_params)
            access_token = oauth_result.access_token
            user_id = oauth_result.account_id
            refresh_token = getattr(oauth_result, "refresh_token", None)

            return access_token, refresh_token, user_id
        except Exception as e:
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
            print(dropbox_data)
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

async def get_dropbox_data_for_list(access_token: str) -> dict:
    """
    Uses the access token to gather Dropbox account data and file metadata,
    returning a structured response for frontend consumption.
    """
    # API Endpoints
    space_usage_url = "https://api.dropboxapi.com/2/users/get_space_usage"
    list_folder_url = "https://api.dropboxapi.com/2/files/list_folder"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        space_usage_response = requests.post(space_usage_url, headers=headers)

        if not space_usage_response.text.strip():
            raise Exception("Received empty or None response for space usage data")

        if space_usage_response.status_code != 200:
            raise Exception(f"Failed to fetch storage data from Dropbox: {space_usage_response.text}")

        try:
            storage_data = space_usage_response.json()
            if not storage_data:
                raise ValueError("No data in response for space usage.")
        except ValueError as e:
            raise Exception("Failed to parse storage data from Dropbox.")

        used_storage = storage_data.get('used', 0)
        total_storage = storage_data.get('allocation', {}).get('allocated', 0)
        remaining_storage = total_storage - used_storage

        file_count = 0
        largest_file = None
        largest_file_size = 0
        oldest_file = None
        oldest_file_time = None
        duplicates = {}

        file_metadata_response = requests.post(list_folder_url, headers=headers, json={"path": "", "recursive": True})

        if not file_metadata_response.text.strip():
            raise Exception("Received empty or None response for file metadata")

        if file_metadata_response.status_code != 200:
            raise Exception(f"Failed to fetch file metadata from Dropbox: {file_metadata_response.text}")

        try:
            files = [entry for entry in file_metadata_response.json().get('entries', []) if entry.get('.tag') == 'file']
        except ValueError as e:
            raise Exception("Failed to parse file metadata from Dropbox.")

        if files:
            for entry in files:
                file_name = entry.get('name', '')
                file_size = entry.get('size', 0)
                client_modified = entry.get('client_modified', '')

                file_count += 1

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

        duplicate_count = sum(len(duplicate_files) for duplicate_files in duplicates.values() if len(duplicate_files) > 1)
        storage_used_by_duplicates = sum(file.get('size', 0) for duplicate_files in duplicates.values() if len(duplicate_files) > 1 for file in duplicate_files)

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
            }
        }
        return data

    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")


