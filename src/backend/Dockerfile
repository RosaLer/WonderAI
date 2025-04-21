FROM python:3.8-slim-buster

# 1. Instalar dependencias base
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    python3-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar SQLite3 actualizado (con corrección de directorio)
WORKDIR /tmp
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3420000.tar.gz \
    && tar -xzvf sqlite-autoconf-3420000.tar.gz \
    && cd sqlite-autoconf-3420000 \
    && ./configure \
    && make \
    && make install \
    && rm -rf /tmp/sqlite-autoconf-3420000*

# 3. Instalar Rust en directorio explícito
WORKDIR /usr/src
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && chmod -R 777 /usr/local/lib

# 4. Configurar entorno
WORKDIR /app
ENV PATH="/root/.cargo/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/local/lib" \
    PYTHONPATH=/app \
    CHROMA_DB_PATH=/data/chroma

# 5. Instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip wheel \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copiar código
COPY . .

# 7. Comando de inicio
CMD ["sh", "-c", "python run_chroma.py & uvicorn app.main:app --host 0.0.0.0 --port 8000"]