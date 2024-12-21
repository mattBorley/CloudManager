from pydantic import BaseModel

# Define the request model to validate the data sent from the client
class SignUpRequest(BaseModel):
    email: str
    name: str
    password: str
    confirmPassword: str

class LoginRequest(BaseModel):
    email: str
    password: str
