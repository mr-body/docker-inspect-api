from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.util.auth import create_access_token
import os

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(payload: LoginRequest):
    username = os.getenv("ADMIN_USER", "admin")
    password = os.getenv("ADMIN_PASSWORD", "admin")

    if payload.username == username and payload.password == password:
        token = create_access_token({"sub": payload.username})
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")