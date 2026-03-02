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

@tool
def radicar_ticket(
    documento: Annotated[str, "Número de documento de identidad del usuario"],
    motivo: Annotated[str, "Descripción detallada del problema o queja"],
) -> str:
    """Radica un ticket de soporte con el documento y motivo proporcionados.
    Usar solo cuando el usuario haya dado explícitamente ambos datos."""
    print("[HERRAMIENTA] Radicando ticket...")
    ticket_id = f"TKT-{random.randint(1000, 9999)}"
    print(f"[HERRAMIENTA] Ticket radicado correctamente. ID: {ticket_id}")
    return (
        f"✅ Ticket **{ticket_id}** radicado correctamente.\n"
        f"Documento: {documento}\n"
        f"Motivo: {motivo}\n\n"
        "Nuestro equipo lo revisará en las próximas 24 horas."
    )