"""
Base model for OAuth
"""
import requests
from fastapi import HTTPException


class OAuthBase:
    """
    Base class for handling OAuth
    """
    def __init__(self, key: str, secret: str, redirect_uri: str):
        self.app_key = key
        self.app_secret = secret
        self.redirect_uri = redirect_uri

    def exchange_code_for_token(self, code: str, token_url: str):
        """
        Exchange authorization code for an access token.
        """
        data = {
            "code": code,
            "client_id": self.app_key,
            "client_secret": self.app_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=data)
        token_data = response.json()

        if "access_token" not in token_data:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token")

        return token_data["access_token"]