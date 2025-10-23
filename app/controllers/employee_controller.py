from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/employees", tags=["Employees"])

# Lista de empleados en memoria (temporal, se reinicia al reiniciar el server)
employees = []

# Modelo de empleado
class Employee(BaseModel):
    name: str
    position: str
    email: str


@router.post("/")
def add_employee(employee: Employee, current_user: str = Depends(get_current_user)):
    employees.append(employee.dict())  # <--- guarda el empleado en memoria
    return {"message": f"Empleado agregado por {current_user}", "employee": employee.dict()}

# Endpoint para listar empleados
@router.get("/")
def list_employees(current_user: str = Depends(get_current_user)):
    return {"current_user": current_user, "employees": employees}

