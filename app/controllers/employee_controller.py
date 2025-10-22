from fastapi import APIRouter
from app.utils.generate_data import generate_data

router = APIRouter(prefix="/employees", tags=["Employees"])

# Generar datos simulados al iniciar
employees, surveys, predictions = generate_data(n_employees=20)

@router.get("/")
async def get_employees():
    return employees

@router.get("/surveys")
async def get_surveys():
    return surveys

@router.get("/predictions")
async def get_predictions():
    return predictions
