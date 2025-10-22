# app/controllers/onboarding_controller.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/onboarding",
    tags=["Onboarding"]
)

@router.get("/")
async def get_onboarding():
    return {"message": "Onboarding data"}

@router.post("/add")
async def add_onboarding(employee_id: int):
    return {"message": f"Added employee {employee_id} to onboarding"}