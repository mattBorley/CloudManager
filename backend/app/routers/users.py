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

    print(f"Signup attempt for email: {email}")

    if password != confirm_password:
        print(f"Password mismatch for email: {email}")
        raise HTTPException(status_code=400, detail="Passwords do not match")

    is_valid, message = validate_password(password)
    if not is_valid:
        print(f"Password validation failed for email: {email} - Reason: {message}")
        raise HTTPException(status_code=400, detail=message)

    hashed_password = hash_password(password)
    print(f"Password hashed for email: {email}")

    check = await store_user_in_database(email, name, hashed_password)
    if not check:
        print(f"Failed to store user in database: {email}")
        raise HTTPException(status_code=400, detail="Error storing user in database")

    print(f"User {email} successfully stored in the database")

    access_token = create_access_token(data={"sub": email})
    refresh_token = create_refresh_token(data={"sub": email})

    print(f"Tokens generated for user: {email}")

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

    print(f"🔐 Login attempt for email: {email}")

    check = verify_login(email, password)
    if not check:
        print(f"❌ Invalid login credentials for email: {email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print(f"✅ Login credentials verified for email: {email}")

    # If login is successful, create access tokens
    access_token = create_access_token(data={"sub": email})
    refresh_token = create_refresh_token(data={"sub": email})

    print(f"🪙 Access and refresh tokens generated for email: {email}")

    return {
        "message": "Login successful",
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "Welsby": "TWat"
    }

