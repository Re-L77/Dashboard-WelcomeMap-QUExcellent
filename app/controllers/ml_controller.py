# app/controllers/ml_controller.py
from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer

# 🔹 Creamos el router para incluirlo en main.py
router = APIRouter(prefix="/ml", tags=["Machine Learning"])

# 🔹 Cargamos un modelo de tokenización (puedes cambiar el modelo)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")

# 🔹 Definimos el modelo de entrada (lista de textos)
class TextInput(BaseModel):
    texts: list[str]

# 🔹 Endpoint de tokenización
@router.post("/tokenize/")
async def tokenize_texts(data: TextInput):
    """
    Recibe una lista de textos y devuelve sus tokens.
    Ejemplo de entrada:
    {
        "texts": ["Me gustó el onboarding", "El curso fue confuso"]
    }
    """
    encoded = tokenizer(
        data.texts,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    # Convertimos tensores a listas para devolverlos en JSON
    return {
        "input_ids": encoded["input_ids"].tolist(),
        "attention_mask": encoded["attention_mask"].tolist(),
        "tokens": [tokenizer.convert_ids_to_tokens(ids) for ids in encoded["input_ids"]]
    }
