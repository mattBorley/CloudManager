"""
Base model for OAuth
"""

class OAuthBase:
    """
    Base class for handling OAuth
    """
    def __init__(self, key: str, secret: str, redirect_uri: str):
        self.app_key = key
        self.app_secret = secret
        self.redirect_uri = redirect_uri