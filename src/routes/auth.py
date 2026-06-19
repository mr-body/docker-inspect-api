from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.util.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(payload: LoginRequest):
    if payload.username == "admin" and payload.password == "admin":
        token = create_access_token({"sub": payload.username})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
