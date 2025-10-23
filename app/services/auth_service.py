from app.utils.security import verify_password, hash_password

fake_user = {
    "username": "admin",
    "hashed_password": hash_password("brose123")
}

def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return None
    if not verify_password(password, fake_user["hashed_password"]):
        return None
    return fake_user