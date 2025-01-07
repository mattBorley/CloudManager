"""
Users file
"""

from fastapi import APIRouter, HTTPException

from ..services.Signup import storeUserInDatabase
from ..utils.Password_Checks import *
from ..services.Login import verifyLogin
from ..models.UserModels import SignUpRequest, LoginRequest
from ..utils.Token_Generation import createAccessToken, createRefreshToken

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
    confirmPassword = request.confirmPassword
    if password != confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    is_valid, message = validate_password(password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    hashed_password = hash_password(password)

    result = await storeUserInDatabase(email, name, hashed_password)
    if not result:
        raise HTTPException(status_code=400, detail="Error storing user in database")

    access_token = createAccessToken(data={"sub":email})
    refresh_token = createRefreshToken(data={"sub":email})

    return {"message": "User signed up successfully", "success": True, "access_token": access_token, "refresh_token": refresh_token}


@router.post("/login")
async def login(request: LoginRequest):
    """
            Login endpoint
            Verifies password against database
            """
    email = request.email
    password = request.password

    result = verifyLogin(email, password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = createAccessToken(data={"sub": email})
    refresh_token = createRefreshToken(data={"sub": email})

    return {"message": "Login successful", "success": True, "access_token": access_token, "refresh_token": refresh_token}
