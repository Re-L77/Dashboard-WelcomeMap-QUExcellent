# app/main.py
from fastapi import FastAPI
from app.controllers import employee_controller, onboarding_controller, ml_controller

app = FastAPI(title="Brose Onboarding Dashboard")  # <-- Debe estar definido antes de usarlo

# Incluimos los routers
app.include_router(employee_controller.router)
app.include_router(onboarding_controller.router)
app.include_router(ml_controller.router)

@app.get("/")
async def root():
    return {"message": "Brose Onboarding API running"}
