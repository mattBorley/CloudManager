"""
Main file
"""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

try:
    from app.utils.token_generation import generate_secret_key
except ImportError:
    from utils.token_generation import generate_session_key


try:
    from app.routers.users import router as usersRouter
except ImportError:
    from routers.users import router as usersRouter

try:
    from app.routers.tokens import router as tokensRouter
except ImportError:
    from routers.tokens import router as tokensRouter

try:
    from app.routers.dropbox import router as dropboxRouter
except ImportError:
    from routers.dropbox import router as dropboxRouter

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("API_SECRET_KEY")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your React app's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usersRouter, prefix="/api/users", tags=["users"])
app.include_router(tokensRouter, prefix="/api/tokens", tags=["tokens"])
app.include_router(dropboxRouter, prefix="/api/dropbox", tags=["dropbox"])


app.middleware("http")
async def session_key_middleware(request: Request, call_next):
    if "session_key" not in request.session:
        session_key = generate_session_key()
        request.session["session_key"] = session_key

    response = await call_next(request)
    return response

@app.get("/")
def read_data():
    """
    Main function
    :return: Test Text to frontend
    """
    return {
        "message": "Hello from FastAPI!",
        "status": "success",
        "data": {"id": 1, "name": "Sample Item"},
    }
