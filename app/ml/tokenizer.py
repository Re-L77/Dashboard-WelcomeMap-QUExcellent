from transformers import AutoTokenizer

# Modelo preentrenado para tokenización
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_comments(comments):
    """
    Recibe una lista de strings (comentarios)
    y devuelve un diccionario con input_ids y attention_mask
    """
    encoding = tokenizer(
        comments,
        padding=True,
        truncation=True,
        return_tensors="pt"  # tensores de PyTorch
    )
    return encoding
