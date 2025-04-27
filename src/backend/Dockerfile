FROM python:3.8-slim-buster

# 1. Instalar SQLite3 actualizado
WORKDIR /tmp
RUN apt-get update && apt-get install -y \
    wget build-essential python3-dev curl \
    && wget https://www.sqlite.org/2023/sqlite-autoconf-3420000.tar.gz \
    && tar -xzvf sqlite-autoconf-3420000.tar.gz \
    && cd sqlite-autoconf-3420000 \
    && ./configure \
    && make \
    && make install \
    && rm -rf /tmp/sqlite* \
    && apt-get clean

# 2. Instalar Rust
WORKDIR /usr/src
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && chmod -R 777 /usr/local/lib

# 3. Configurar entorno
WORKDIR /app
ENV PATH="/root/.cargo/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/local/lib" \
    PYTHONPATH=/app \ 
    CHROMA_DB_PATH=/data/chroma

# 4. Instalar dependencias (CON la versión específica de ChromaDB)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pysqlite3-binary

# 5. Copiar código (estructura optimizada)
COPY ./app ./app  
COPY run_chroma.py .

# 6. Comando de inicio
CMD ["sh", "-c", "python run_chroma.py --port 8001 & uvicorn app.main:app --host 0.0.0.0 --port 8000"]