import random
from datetime import datetime, timedelta

# --------------------------
# Generación de empleados
# --------------------------
def generate_employees(n=20):
    first_names = ["John", "Jane", "Alice", "Bob", "Carlos", "Lucia", "Maria", "David", "Sofia", "Luis"]
    last_names = ["Doe", "Smith", "Garcia", "Lopez", "Martinez", "Hernandez", "Perez", "Torres"]
    departments = ["Manufacturing", "HR", "IT", "Quality", "Maintenance", "Logistics"]
    
    employees = []
    for i in range(1, n+1):
        employee = {
            "id": i,
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "start_date": (datetime.today() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "department": random.choice(departments),
            "onboarding_completed": random.choice([True, False]),
        }
        employees.append(employee)
    return employees

# --------------------------
# Generación de encuestas
# --------------------------
def generate_surveys(employees):
    survey_comments = [
        "Very happy with onboarding",
        "It could be better",
        "Training was excellent",
        "Too much information at once",
        "Supportive team",
        "Some topics unclear"
    ]
    
    surveys = []
    for emp in employees:
        survey = {
            "employee_id": emp["id"],
            "satisfaction": random.randint(1, 5),
            "comments": random.choice(survey_comments)
        }
        surveys.append(survey)
    return surveys

# --------------------------
# Generación de predicciones iniciales
# --------------------------
def generate_predictions(employees):
    predictions = []
    for emp in employees:
        prediction = {
            "employee_id": emp["id"],
            "onboarding_success_prob": round(random.uniform(0.5, 1.0), 2),  # probabilidad de éxito
            "stress_risk_level": random.choice(["Low", "Medium", "High"])   # riesgo de estrés
        }
        predictions.append(prediction)
    return predictions

# --------------------------
# Función principal
# --------------------------
def generate_data(n_employees=20):
    employees = generate_employees(n_employees)
    surveys = generate_surveys(employees)
    predictions = generate_predictions(employees)
    return employees, surveys, predictions

# --------------------------
# Test rápido
# --------------------------
if __name__ == "__main__":
    emps, surs, preds = generate_data()
    print("=== Employees ===")
    for e in emps:
        print(e)
    print("\n=== Surveys ===")
    for s in surs:
        print(s)
    print("\n=== Predictions ===")
    for p in preds:
        print(p)
