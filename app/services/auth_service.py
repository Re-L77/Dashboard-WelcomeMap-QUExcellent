# app/services/auth_service.py
from app.utils.security import verify_password, create_access_token, hash_password

# Usuario simulado (ejemplo)
fake_user_db = {
    "brose_user": {
        "username": "brose_user",
        "hashed_password": hash_password("brose123"),
    }
}

def authenticate_user(username: str, password: str):
    user = fake_user_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def login_user(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        return None
    access_token = create_access_token({"sub": user["username"]})
    return access_token
