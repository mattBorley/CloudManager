"""
Users file
"""

from fastapi import APIRouter, HTTPException

from ..services.Signup import storeUserInDatabase
from ..utils.Password_Checks import *
from ..services.Login import login
from ..models.UserModels import SignUpRequest

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

    result = storeUserInDatabase(email, name, hashed_password)
    if result:
        return {"message": "User signed up successfully", "success": True}
    else:
        raise HTTPException(status_code=400, detail="Error storing user in database")


@router.post("/login")
async def login(email: str, password: str):
    """
            Login endpoint
            Verifies password against database
            """
    result = login(email, password)
    if result:
        return {"message": "Login successful", "success": True}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

