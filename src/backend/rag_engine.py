import json
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from transformers import pipeline

class RAGEngine:
    def __init__(self):
        self.docs_path = os.path.abspath('../chromadb/data/docs.json')
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.Client()
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.collection = self.client.create_collection(name="wonder_docs", embedding_function=self.ef)
        self.load_documents()

        self.llm = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", device_map="auto", trust_remote_code=True)

    def load_documents(self):
        with open(self.docs_path, "r", encoding="utf-8") as f:
            docs = json.load(f)

        for doc in docs:
            self.collection.add(
                documents=[doc["content"]],
                metadatas=[doc["metadata"]],
                ids=[doc["id"]]
            )

    def query(self, question):
        results = self.collection.query(query_texts=[question], n_results=1)
        context = results["documents"][0][0]

        prompt = f"Contexto: {context}\n\nPregunta: {question}\nRespuesta:"
        res = self.llm(prompt, max_new_tokens=100)[0]["generated_text"]

        return res.replace(prompt, "").strip()
