# app/config.py

from dotenv import load_dotenv
import os

# Carga las variables del archivo .env en el entorno
load_dotenv()

# Variables de configuración globales
SECRET_KEY = os.getenv("SECRET_KEY", "clave_de_prueba_no_usar_en_produccion")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "60"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
