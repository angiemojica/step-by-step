"""Definición del estado del agente."""

from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """Estado compartido del grafo del agente.

    - messages: Historial de mensajes (LangGraph concatena automáticamente)
    """

    messages: Annotated[list, add_messages]
