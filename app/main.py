from fastapi import FastAPI
from app.controllers import employee_controller, onboarding_controller, ml_controller

app = FastAPI(title="Brose Onboarding Dashboard")

app.include_router(employee_controller.router)
app.include_router(onboarding_controller.router)
app.include_router(ml_controller.router)  # 👈 Asegúrate de agregar esta línea

@app.get("/")
async def root():
    return {"message": "Brose Onboarding API running"}
