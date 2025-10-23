from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.controllers import employee_controller, onboarding_controller, ml_controller, auth_controller

app = FastAPI(title="Brose Onboarding Dashboard")

# Mount static files and templates so the `/` route can render HTML views
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="views")

app.include_router(employee_controller.router)
app.include_router(auth_controller.router)
app.include_router(onboarding_controller.router)
app.include_router(ml_controller.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Render the main dashboard HTML located at app/views/dashboard.html"""
    return templates.TemplateResponse("dashboard.html", {"request": request})
def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return None
    if not verify_password(password, fake_user["hashed_password"]):
        return None
    return fake_user