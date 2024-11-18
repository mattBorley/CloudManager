"""
Main file
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your React app's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def read_data():
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
