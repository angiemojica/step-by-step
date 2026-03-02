"""Definición del estado del agente."""

from typing import Annotated, Optional, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """Estado compartido del grafo del agente.

    - messages: Historial de mensajes (LangGraph concatena automáticamente)
    - intent: Clasificación de intención (faq | radicar_ticket)
    - documento: Número de identificación del usuario
    - motivo: Descripción del problema/queja
    - sentimiento: Clasificación tras radicar ticket (positivo, neutro, negativo, furioso)
    """

    messages: Annotated[list, add_messages]
    intent: Optional[str]
    documento: Optional[str]
    motivo: Optional[str]
    sentimiento: Optional[str]
