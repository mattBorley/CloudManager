import os

import requests
from fastapi import HTTPException

from ..models.oauth import OAuthBase


class GoogleOAuth(OAuthBase):
    """
    Google OAuth implementation extending OAuthBase.
    """
    TOKEN_URL = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    # USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    # DRIVE_URL = "https://www.googleapis.com/drive/v3/files"

    def __init__(self, key: str, secret: str, redirect_uri: str):
        super().__init__(key, secret, redirect_uri)
        self.key = key
        self.secret = secret
        self.redirect_uri = redirect_uri

    def exchange_code_for_token(self, code: str):
        """
        Exchange the authorization code for an access token and refresh token.
        """
        data = {
            "code": code,
            "client_id": self.key,
            "client_secret": self.secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "access_type": "offline",  # Requests refresh token
            "prompt": "consent",  # Forces Google to return a refresh token every time
        }

        response = requests.post(self.TOKEN_URL, data=data)

        if response.status_code != 200:
            return None

        return response.json()  # Returns access_token and refresh_token

    def refresh_access_token(self, refresh_token: str):
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
            return None

        return response.json()

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