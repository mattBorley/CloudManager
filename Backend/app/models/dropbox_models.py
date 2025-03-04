"""
Model for Dropbox OAuth
"""
import logging
from fastapi import HTTPException
from urllib.parse import urlparse, parse_qsl, urlencode
import dropbox
import httpx
import requests

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

async def store_credentials(local_access_token: str, refresh_token: str, user_id: str, cloud_name: str):
    """
    Adds Dropbox account to the database and logs key actions.
    """
    try:
        # Check if user_id or cloud_name is None and log a warning if so
        if not user_id:
            logging.warning("user_id is None or empty.")
        if not cloud_name:
            logging.warning("cloud_name is None or empty.")


        payload = get_payload_from_access(local_access_token)

        user_email = payload.get("email")
        logging.info(f"Extracted email: {user_email}")

        logging.debug(f"Getting user ID for email: {user_email}")
        local_user_id = get_user_id(user_email)
        logging.info(f"Retrieved local user ID: {local_user_id}")

        logging.debug(f"Inserting data into Dropbox table for user_id: {local_user_id}")
        if not local_user_id:
            raise HTTPException(status_code=400, detail="Missing local_user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user_id")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Missing refresh_token")
        if not cloud_name:
            raise HTTPException(status_code=400, detail="Missing cloud_name")
        insert_into_dropbox_table(local_user_id, user_id, refresh_token, cloud_name)
        logging.info(f"Credentials for user {local_user_id} successfully stored in {cloud_name}.")

    except Exception as e:
        logging.error(f"Error storing credentials for user {user_id} in cloud {cloud_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def get_data_for_list(access_token: str) -> dict:
    """
    Uses the access token to gather Dropbox account data and file metadata,
    returning a structured response for frontend consumption.
    """
    # API Endpoints
    space_usage_url = "https://api.dropboxapi.com/2/users/get_space_usage"
    list_folder_url = "https://api.dropboxapi.com/2/files/list_folder"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        # Fetch Space Usage Info
        logging.info("Fetching space usage data from Dropbox...")
        response = requests.post(space_usage_url, headers=headers)

        # Log the raw response for debugging
        logging.debug(f"Raw response from Dropbox (space usage): {response.text}")

        # Check if the response body is empty
        if not response.text.strip():
            logging.error(f"Received empty response for space usage data")
            raise Exception("Received empty response for space usage data")

        # Check for valid JSON
        if response.status_code != 200:
            logging.error(f"Error fetching storage data: {response.text}")
            raise Exception(f"Failed to fetch storage data from Dropbox: {response.text}")

        try:
            storage_data = response.json()
        except ValueError as e:
            logging.error(f"Error parsing JSON response for space usage: {str(e)}")
            logging.debug(f"Response content: {response.text}")
            raise Exception("Failed to parse storage data from Dropbox.")

        used_storage = storage_data['used']
        total_storage = storage_data['allocation']['allocated']
        remaining_storage = total_storage - used_storage

        logging.info(
            f"Storage data fetched successfully: Used {used_storage}, Total {total_storage}, Remaining {remaining_storage}")

        file_count = 0
        largest_file = None
        largest_file_size = 0
        oldest_file = None
        oldest_file_time = None
        largest_folder = None
        largest_folder_size = 0
        duplicates = {}

        file_metadata = []
        logging.info("Fetching file metadata from Dropbox...")
        response = requests.post(list_folder_url, headers=headers, json={"path": "", "recursive": True})

        # Log the raw response for debugging
        logging.debug(f"Raw response from Dropbox (file metadata): {response.text}")

        # Check if the response body is empty
        if not response.text.strip():
            logging.error(f"Received empty response for file metadata")
            raise Exception("Received empty response for file metadata")

        # Check for valid JSON
        if response.status_code != 200:
            logging.error(f"Error fetching file metadata: {response.text}")
            raise Exception(f"Failed to fetch file metadata from Dropbox: {response.text}")

        try:
            files = response.json()['entries']
        except ValueError as e:
            logging.error(f"Error parsing JSON response for file metadata: {str(e)}")
            logging.debug(f"Response content: {response.text}")
            raise Exception("Failed to parse file metadata from Dropbox.")

        for entry in files:
            if entry['.tag'] == 'file':
                file_count += 1
                file_size = entry['size']
                file_name = entry['name']
                client_modified = entry['client_modified']

                # Largest File
                if file_size > largest_file_size:
                    largest_file = entry
                    largest_file_size = file_size
                    logging.debug(f"Found new largest file: {file_name} with size {file_size}")

                # Oldest File
                if not oldest_file_time or client_modified < oldest_file_time:
                    oldest_file = entry
                    oldest_file_time = client_modified
                    logging.debug(f"Found new oldest file: {file_name} with modified time {client_modified}")

                # Duplicates
                if file_name in duplicates:
                    duplicates[file_name].append(entry)
                    logging.debug(f"Duplicate found: {file_name}")
                else:
                    duplicates[file_name] = [entry]

            elif entry['.tag'] == 'folder':
                folder_size = 0
                for file in files:
                    if file['.tag'] == 'file' and file['path_display'].startswith(entry['path_display']):
                        folder_size += file['size']

                # Largest Folder
                if folder_size > largest_folder_size:
                    largest_folder = entry
                    largest_folder_size = folder_size
                    logging.debug(f"Found new largest folder: {entry['name']} with size {folder_size}")

        # Duplicates Handling
        duplicate_count = sum(
            len(duplicate_files) for duplicate_files in duplicates.values() if len(duplicate_files) > 1)
        storage_used_by_duplicates = sum(
            file['size'] for duplicate_files in duplicates.values() if len(duplicate_files) > 1 for file in
            duplicate_files)

        logging.info(f"Found {duplicate_count} duplicate files using {storage_used_by_duplicates} bytes of storage.")

        # Compiling the Data
        data = {
            "storage": {
                "used_storage": used_storage,
                "total_storage": total_storage,
                "remaining_storage": remaining_storage
            },
            "file_metadata": {
                "file_count": file_count,
                "largest_file": {
                    "name": largest_file['name'],
                    "size": largest_file_size,
                    "path": largest_file['path_display']
                },
                "oldest_file": {
                    "name": oldest_file['name'],
                    "modified": oldest_file_time,
                    "path": oldest_file['path_display']
                }
            },
            "folder_metadata": {
                "largest_folder": {
                    "name": largest_folder['name'],
                    "size": largest_folder_size,
                    "path": largest_folder['path_display']
                }
            },
            "duplicates": {
                "duplicate_count": duplicate_count,
                "storage_used_by_duplicates": storage_used_by_duplicates
            },
            "sync_info": {
                "last_synced": oldest_file_time
            }
        }

        logging.info("Data compiled successfully. Returning the data.")
        return data

    except Exception as e:
        logging.error(f"Error while fetching Dropbox data: {str(e)}")
        raise Exception(f"Error fetching data: {str(e)}")
