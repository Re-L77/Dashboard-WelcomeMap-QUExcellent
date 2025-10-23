from fastapi import FastAPI
from app.controllers import employee_controller, onboarding_controller, ml_controller, auth_controller
app = FastAPI(title="Brose Onboarding Dashboard")

app.include_router(employee_controller.router)
app.include_router(auth_controller.router)
app.include_router(onboarding_controller.router)
app.include_router(ml_controller.router)


@app.get("/")
async def root():
    return {"message": "Brose Onboarding API running"}
def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return None
    if not verify_password(password, fake_user["hashed_password"]):
        return None
    return fake_user