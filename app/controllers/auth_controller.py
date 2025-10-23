# app/controllers/auth_controller.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    token = login_user(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
