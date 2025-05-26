# WonderAI

WonderAI es una aplicación estilo chat basada en documentos sobre viajes. Combina un modelo de lenguaje (TinyLlama) y una base de datos vectorial (ChromaDB) para ofrecer respuestas coherentes y útiles sobre el contenido cargado, como apuntes o documentos de viajes.

## ¿Qué hace WonderAI?

- Permite hacer preguntas sobre documentos cargados de viajes.
- Utiliza un modelo LLM ligero (TinyLlama) para generar respuestas naturales.
- Usa ChromaDB para recuperar fragmentos relevantes del contenido.
- Ahora mismo corre completamente en local (sin conexión a internet, ni uso de APIs externas).
- Interfaz amigable con React + backend en Python (FastAPI).

## Estructura del Proyecto

WONDERAI/
├── src/
│   ├── .venv3/  
│   ├── backend/ 
│   ├── chromadb/
│   └── frontend/
│   └── models/  
├── run.sh       
└── README.md

## Requisitos

- Python 3.10+
- Node.js y npm
- pip + venv recomendado
- git (opcional)


## Instalación

1. **Clona el repositorio**
   bash:
   git clone https://github.com/RosaLer/WonderAI.git
   cd wonderai
   cd src/
   python -m venv .venv
   source .venv/bin/activate

2. **Instala dependencias del backend**
   pip install --upgrade pip
   pip install -r requirements.txt 

3. **Instala dependencias del frontend**

   cd ../frontend
   npm install

4. **Ejecución**

    ./run.sh
    Esto hace:
    - Lanza el backend con FastAPI en http://localhost:8001.
    - Lanza el frontend React en http://localhost:3000.
    - El backend se detiene automáticamente cuando se cierra el frontend.

## Modelos

WonderAI usa:
- Embeddings: all-MiniLM-L6-v2 (de sentence-transformers)
- LLM: TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf (ligero, corre en CPU)