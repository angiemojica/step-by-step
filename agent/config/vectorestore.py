"""Configuración del vectorstore (Pinecone) y retriever."""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

INDEX_NAME = "soporte-faq"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Ruta a la base de conocimiento
KNOWLEDGE_PATH = os.environ.get("PATH_BASE_KNOWLEDGE")

# Configuración del splitter para fragmentar el texto
TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def _load_documents_from_txt(path: Path | str = KNOWLEDGE_PATH):
    """Carga y fragmenta el archivo TXT en documentos para el vectorstore."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró la base de conocimiento: {path}")

    loader = TextLoader(str(path), encoding="utf-8")
    docs = loader.load()
    return TEXT_SPLITTER.split_documents(docs)


def _ensure_index(pc: Pinecone) -> None:
    """Crea o recrea el índice de Pinecone."""
    if INDEX_NAME in pc.list_indexes().names():
        pc.delete_index(INDEX_NAME)
    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIM,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )


_retriever = None


def get_retriever(k: int = 2, knowledge_path: Path | str | None = None):
    """Retorna el retriever configurado para consultas RAG (singleton).
    
    Carga la base de conocimiento desde data/base_knowledge.txt por defecto.
    """
    global _retriever
    if _retriever is None:
        docs = _load_documents_from_txt(knowledge_path or KNOWLEDGE_PATH)
        if not docs:
            raise ValueError(
                f"La base de conocimiento está vacía o no se pudieron cargar documentos "
                f"desde {knowledge_path or KNOWLEDGE_PATH}"
            )

        api_key = os.environ.get("PINECONE_API_KEY")
        pc = Pinecone(api_key=api_key)
        _ensure_index(pc)

        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectorstore = PineconeVectorStore.from_documents(
            docs, embeddings, index_name=INDEX_NAME
        )
        _retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return _retriever
