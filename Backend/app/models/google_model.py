import os

import requests

from backend.app.models.oauth import OAuthBase


class GoogleOAuth(OAuthBase):
    """
    Google OAuth implementation extending OAuthBase.
    """
    TOKEN_URL = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    DRIVE_URL = "https://www.googleapis.com/drive/v3/files"

    def __init__(self, key: str, secret: str, redirect_uri: str):
        super().__init__(key, secret, redirect_uri)

    # def get_user_info(self, access_token: str):
    #     """
    #     Fetch user information from Google.
    #     """
    #     response = requests.get(
    #         self.USER_INFO_URL,
    #         headers={"Authorization": f"Bearer {access_token}"}
    #     )
    #     return response.json()
    #
    # def get_drive_data(self, access_token: str):
    #     """
    #     Fetch user's Google Drive files.
    #     """
    #     response = requests.get(
    #         self.DRIVE_URL,
    #         headers={"Authorization": f"Bearer {access_token}"}
    #     )
    #     return response.json()