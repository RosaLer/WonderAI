from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
import chromadb
import json

app = FastAPI()

# CORS para que React pueda acceder desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa Chroma en memoria
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="docs")

# Carga los documentos
with open("../chromadb/data/docs.json", "r") as f:
    data = json.load(f)
    for doc in data:
        collection.add(
            documents=[doc["content"]],
            metadatas=[doc["metadata"]],
            ids=[doc["id"]],
        )

# Carga el modelo de SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.post("/ask")
async def ask_question(request: Request):
    body = await request.json()
    query = body.get("query", "")

    if not query:
        return {"error": "No query provided"}

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1,
    )

    # results['documents'] es una lista de listas, así que hacemos flatten
    matched_docs = results['documents'][0] if results['documents'] else []

    return {
        "results": {
            "documents": matched_docs
        }
    }
