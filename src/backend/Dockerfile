FROM python:3.9-slim

WORKDIR /app

# Instala dependencias del sistema (necesarias para algunas librerías)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . .

# Variables de entorno 
ENV PYTHONPATH=/app \
    CHROMA_DB_HOST="chromadb" \
    CHROMA_DB_PORT=8000

EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]