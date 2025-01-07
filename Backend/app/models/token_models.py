"""
Refresh Token Model
"""

from pydantic.v1 import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str
