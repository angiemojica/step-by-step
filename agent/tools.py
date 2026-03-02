"""Herramientas del agente de soporte."""

import random
import requests
from typing import Annotated

from langchain_core.tools import tool

from agent.config import get_retriever


@tool
def consultar_base_conocimiento(
    query: Annotated[str, "Pregunta o tema a buscar en la base de conocimiento"]
) -> str:
    """Consulta la base de conocimiento (FAQ, políticas, reembolsos, horarios, etc.)
    para responder dudas del usuario."""
    print("[HERRAMIENTA] Consultando base de conocimiento...")
    retriever = get_retriever(k=3)
    docs = retriever.invoke(query)
    contexto = "\n\n".join([d.page_content for d in docs])
    return contexto if contexto else "No se encontró información relevante para tu consulta."

