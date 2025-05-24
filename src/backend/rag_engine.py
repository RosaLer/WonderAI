# rag_engine.py
import json
import os
import textwrap
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from llama_cpp import Llama

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class RAGEngine:
    def __init__(self):
        # Configuración de logging
        self.logger = logging.getLogger('RAGEngine')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.info("Inicializando RAG Engine...")
        
        self.docs_path = os.path.join(BASE_DIR, "../chromadb/data/docs.json")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # Inicialización de ChromaDB
        self.client = chromadb.Client()
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.create_collection(
            name="wonder_docs", embedding_function=self.ef
        )
        self._load_documents()

        # Inicialización del modelo LLM
        model_path = os.path.join(BASE_DIR, "../models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf")
        self.logger.info(f"Cargando modelo desde: {model_path}")
        
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            n_gpu_layers=0,
            verbose=False,
        )
        self.logger.info("RAG Engine inicializado correctamente")

    def _load_documents(self):
        self.logger.info(f"Cargando documentos desde: {self.docs_path}")
        
        try:
            with open(self.docs_path, "r", encoding="utf-8") as f:
                docs = json.load(f)
                self.logger.info(f"Número de documentos encontrados: {len(docs)}")
                
                for i, doc in enumerate(docs):
                    if not all(k in doc for k in ["content", "metadata", "id"]):
                        self.logger.error(f"Documento {i} tiene estructura incorrecta: {doc.keys()}")
                        continue
                    
                    self.collection.add(
                        documents=[doc["content"]],
                        metadatas=[doc["metadata"]],
                        ids=[doc["id"]],
                    )
                    self.logger.debug(f"Documento agregado - ID: {doc['id']}")
                
                self.logger.info(f"Total documentos cargados en ChromaDB: {self.collection.count()}")
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Error al cargar el archivo JSON: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error inesperado al cargar documentos: {e}")
            raise

    def query(self, question: str, n_results: int = 1) -> str:
        try:
            self.logger.info(f"\n{'='*50}\nNueva consulta recibida: '{question}'\n{'='*50}")
            
            # Paso 1: Consulta a ChromaDB
            self.logger.debug(f"Buscando {n_results} resultados para la pregunta")
            results = self.collection.query(query_texts=[question], n_results=n_results)
            
            self.logger.debug(f"Resultados de ChromaDB (IDs): {results['ids']}")
            self.logger.debug(f"Distancias de los resultados: {results['distances']}")
            
            if not results["documents"] or not results["documents"][0]:
                self.logger.warning("No se encontraron documentos relevantes")
                return "No tengo información suficiente."

            # Paso 2: Procesamiento del contexto
            context = "\n".join([f"Información {i+1}: {doc.strip()}" for i, doc in enumerate(results["documents"][0])])
            self.logger.debug(f"\nContexto recuperado:\n{context}\n")

            # Paso 3: Construcción del prompt
            prompt = textwrap.dedent(f"""\
                [INST] DEBES responder en UN ÚNICO PÁRRAFO de 5-8 oraciones maximo.
                PROHIBIDO usar viñetas, números o saltos de línea.
                
                Usa SOLO esta información:
                {context}
    
                Pregunta:
                {question}

                Respuesta: [/INST] La ciudad de""")
            
            self.logger.debug(f"\nPrompt completo enviado al modelo:\n{prompt}\n")

            # Paso 4: Llamada al modelo
            self.logger.info("Enviando prompt al modelo LLM...")
            out = self.llm(
                prompt=prompt,
                max_tokens=300,
                temperature=0.6,
                top_p=0.95,
                repeat_penalty=1.2,
                stop=["Pregunta:", "Usuario:", "\n\n"]
            )
            
            self.logger.debug(f"\nRespuesta cruda del modelo: {out}")

            # Paso 5: Procesamiento de la respuesta
            response = out["choices"][0]["text"].strip()
            self.logger.info(f"Respuesta generada: '{response}'")
            
            return response

        except Exception as e:
            self.logger.error(f"Error durante la consulta: {str(e)}", exc_info=True)
            return "Ocurrió un error al procesar tu pregunta. Por favor intenta nuevamente."