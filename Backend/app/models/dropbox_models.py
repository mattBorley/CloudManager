"""
Model for Dropbox OAuth
"""
from urllib.parse import urlparse, parse_qsl, urlencode
import dropbox
import httpx

try:
    from app.models.oauth import OAuthBase
except ImportError:
    from ..models.oauth import OAuthBase

try:
    from app.utils.token_generation import generate_csrf_token
except ImportError:
    from ..utils.token_generation import generate_csrf_token


class DropboxOAuthClass(OAuthBase):
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
        query_params["state"] = csrf_token

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
