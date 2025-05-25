from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rag_engine import RAGEngine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGEngine()

@app.post("/ask")
async def ask_question(request: Request):
    body = await request.json()
    query = body.get("query", "").strip()

    if not query:
        return {"error": "No query provided"}

    answer = rag.query(query)
    return {"response": answer}
