from fastapi import FastAPI
from rag import setup_chroma, search

app = FastAPI()
vectordb = setup_chroma()

@app.get("/ask")
def ask(query: str):
    context = search(query, vectordb)
    return {"context": context, "query": query}