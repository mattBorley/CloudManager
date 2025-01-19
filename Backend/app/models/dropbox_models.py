"""
Model for DropBox
"""

import dropbox
from ..utils.token_generation import generate_csrf_token

class DropboxOAuthClass:
    """
    Class for Dropbox OAuth
    """
    def __init__(self, key: str, secret: str, redirect_uri: str, csrf_token_session_key: str = generate_csrf_token()):
        self.app_key = key
        self.app_secret = secret
        self.redirect_uri = redirect_uri
        self.csrf_token_session_key = csrf_token_session_key

    def create_flow(self, session: dict) -> dropbox.DropboxOAuth2Flow:
        """
        Create a DropboxOAuth2Flow instance with the given session.
        """
        return dropbox.DropboxOAuth2Flow(
            consumer_key=self.app_key,
            consumer_secret=self.app_secret,
            redirect_uri=self.redirect_uri,
            session=session,
            csrf_token_session_key=self.csrf_token_session_key,
        )

    def get_authorization_url(self, session: dict) -> str:
        """
        Generate the Dropbox authorization URL.
        """
        flow = self.create_flow(session)
        return flow.start()

    def finish_auth(self, session: dict, query_params: dict) -> tuple:
        """
        Complete the Dropbox OAuth flow and retrieve the access token.
        """
        flow = self.create_flow(session)
        return flow.finish(query_params)  # Returns (access_token, user_id, url_state)
