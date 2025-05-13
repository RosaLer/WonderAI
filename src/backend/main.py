from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rag_engine import RAGEngine
from pydantic import BaseModel

app = FastAPI()
rag = RAGEngine()

# Permitir llamadas desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Question(BaseModel):
    question: str

@app.post("/api/ask")
async def ask_question(q: Question):
    answer = rag.query(q.question)
    return {"answer": answer}
