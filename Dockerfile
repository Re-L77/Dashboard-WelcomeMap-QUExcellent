FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar el controlador ODBC para SQL Server
RUN apt-get update && \
    apt-get install -y curl gnupg2 wget && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg && \
    chmod 644 /etc/apt/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar el driver de SQL Server para Python y dependencias adicionales para la API
RUN pip install --no-cache-dir pyodbc fastapi uvicorn python-jose python-multipart pydantic email-validator

# Instalar dependencias para manejo de CORS y autenticación
RUN pip install --no-cache-dir fastapi-cors python-jose[cryptography] passlib[bcrypt]

COPY app/ /app/

EXPOSE 8000

# Configuración para la API
ENV PYTHONPATH=/
ENV API_PREFIX=/api/v1
ENV CORS_ORIGINS="http://localhost:8000,http://localhost:3000"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]