"""
Users endpoints
"""

from fastapi import APIRouter, HTTPException

from ..services.signup import store_user_in_database
from ..utils.password_checks import validate_password, hash_password
from ..services.login import verify_login
from ..models.user_models import SignUpRequest, LoginRequest
from ..utils.token_generation import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/signup")
async def signup(request: SignUpRequest):
    """
    SignUp endpoint
    Validate password meets criteria and stores the information in the database (users table)
    """
    email = request.email
    name = request.name
    password = request.password
    confirm_password = request.confirm_password
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    is_valid, message = validate_password(password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    hashed_password = hash_password(password)


    if not store_user_in_database(email, name, hashed_password):
        raise HTTPException(status_code=400, detail="Error storing user in database")

    access_token = create_access_token(data={"sub": email})
    refresh_token = create_refresh_token(data={"sub": email})

    return {
        "message": "User signed up successfully",
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/login")
async def login(request: LoginRequest):
    """
    Login endpoint
    Verifies password against database
    """
    email = request.email
    password = request.password

    # Verify login with the modified function
    if not verify_login(email, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If login is successful, create access tokens
    access_token = create_access_token(data={"sub": email})
    refresh_token = create_refresh_token(data={"sub": email})

    return {
        "message": "Login successful",
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
