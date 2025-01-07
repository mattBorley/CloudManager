"""
Main file
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.routers.Users import router as usersRouter
except ImportError:
    from routers.Users import router as usersRouter

try:
    from app.routers.Tokens import router as  tokensRouter
except ImportError:
    from routers.Tokens import router as tokensRouter
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your React app's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usersRouter, prefix="/api/users", tags=["users"])
app.include_router(tokensRouter, prefix="/api/tokens", tags=["tokens"])

@app.get("/")
def read_data():
    """
    Main function
    :return: Test Text to Frontend
    """
    return {
        "message": "Hello from FastAPI!",
        "status": "success",
        "data": {
            "id": 1,
            "name": "Sample Item"
        }
    }