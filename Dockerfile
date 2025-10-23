FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema para compilación y ML
# Esta capa se cachea y NO se reconstruye a menos que cambien las dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libgomp1 \
    curl \
    gnupg2 \
    wget && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg && \
    chmod 644 /etc/apt/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar SOLO requirements.txt ANTES del código
# Si requirements.txt no cambia, Docker reutiliza esta capa
COPY requirements.txt .

# Instalar dependencias Python (se cachea si requirements.txt no cambió)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código DESPUÉS de instalar dependencias
# Solo esta parte se reconstruye cuando cambias el código
COPY app/ /app/
COPY static/ /static/
COPY views/ /views/

EXPOSE 8000

# Configuración para la API
ENV PYTHONPATH=/
ENV API_PREFIX=/api/v1
ENV CORS_ORIGINS="http://localhost:8000,http://localhost:3000"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]