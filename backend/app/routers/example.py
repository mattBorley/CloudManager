"""
Token refresh file
"""
from urllib.request import Request

from fastapi import Depends

from backend.app.utils.token_validation import validate_access_token

# router = exampleRouter()

# @router.post("/refresh")
# async def refresh(request: Request, email: str = Depends(validate_access_token)):
#     """
#     Example of a protected Route
#     """
#     return {"message": "Access granted"}