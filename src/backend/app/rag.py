from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
import json

# Cargar datos
def load_data():
    with open("../data/destinos.json") as f:
        return json.load(f)

# Configurar ChromaDB
def setup_chroma():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    documents = [item["content"] for item in load_data()]
    metadatas = [item["metadata"] for item in load_data()]
    
    vectordb = Chroma.from_texts(
        texts=documents,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory="/chroma/chroma_data",
    )
    return vectordb

# Buscar información relevante
def search(query, vectordb, k=2):
    results = vectordb.similarity_search(query, k=k)
    return [doc.page_content for doc in results]