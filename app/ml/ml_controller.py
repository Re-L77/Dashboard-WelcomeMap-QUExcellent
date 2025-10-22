from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer

router = APIRouter()

tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

class TextList(BaseModel):
    texts: list[str]

@router.post("/tokenize/")
async def tokenize(text_list: TextList):
    tokens = [tokenizer.encode(text, add_special_tokens=True) for text in text_list.texts]
    return {"tokens": tokens}
