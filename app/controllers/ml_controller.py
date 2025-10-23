from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import tensorflow as tf
from typing import List, Union

# ---------------------------------------------
# Inicializamos el router
# ---------------------------------------------
router = APIRouter(prefix="/ml", tags=["Machine Learning"])

# ---------------------------------------------
# Carga de modelos y transformadores
# ---------------------------------------------
try:
    scaler = joblib.load("scaler.joblib")
    lgb_model = joblib.load("lgb_model.joblib")
    le_dict = joblib.load("le_dict-2.joblib")
    modal_values = joblib.load("modal_values.joblib")
    nn_model = tf.keras.models.load_model("nn_model.keras")
    print("Modelos y preprocesadores cargados correctamente")
except Exception as e:
    print(f"Error al cargar modelos: {e}")

# ---------------------------------------------
# Esquema de entrada
# ---------------------------------------------
class FeaturesInput(BaseModel):
    features: List[dict]  # Lista de diccionarios con las variables de entrada
    model_type: str = "lgb"  # o "nn" para la red neuronal

# ---------------------------------------------
# Función de preprocesamiento
# ---------------------------------------------
def preprocess_input(data: List[dict]):
    import pandas as pd
    df = pd.DataFrame(data)

    # Rellenar valores faltantes con modales
    for col, val in modal_values.items():
        if col in df.columns:
            df[col] = df[col].fillna(val)

    # Aplicar LabelEncoders a columnas categóricas
    for col, le in le_dict.items():
        if col in df.columns:
            try:
                df[col] = le.transform(df[col])
            except ValueError:
                # Manejo de valores no vistos durante el entrenamiento
                df[col] = df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

    # Escalar los datos numéricos
    df_scaled = scaler.transform(df)
    return df_scaled

# ---------------------------------------------
# Endpoint para predicción
# ---------------------------------------------
@router.post("/predict/")
async def predict(data: FeaturesInput):
    """
    Endpoint para hacer predicciones con modelos ML o NN.
    Ejemplo de entrada:
    {
        "model_type": "lgb",
        "features": [
            {"col1": 0.3, "col2": "A", "col3": 5.6},
            {"col1": 0.7, "col2": "B", "col3": 4.1}
        ]
    }
    """
    try:
        X = preprocess_input(data.features)

        if data.model_type == "lgb":
            preds = lgb_model.predict(X)
        elif data.model_type == "nn":
            preds = nn_model.predict(X).flatten()
        else:
            raise HTTPException(status_code=400, detail="Tipo de modelo no válido (usa 'lgb' o 'nn').")

        return {"predictions": preds.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {e}")