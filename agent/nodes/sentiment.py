"""Nodo de clasificación de sentimiento tras radicar un ticket."""

from langchain_core.messages import HumanMessage

from agent.config import get_llm
from agent.models import SentimientoClasificado
from agent.state import AgentState


def sentiment_node(state: AgentState) -> dict:
    """Clasifica el sentimiento del usuario tras radicar un ticket.
    Usa el motivo o los últimos mensajes del usuario para el análisis."""
    messages = state.get("messages", [])
    texto_analizar = None

    # Buscar el último mensaje humano o el motivo en tool_calls
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage) and hasattr(msg, "content") and msg.content:
            texto_analizar = msg.content
            break

    if not texto_analizar:
        return {"sentimiento": "neutro"}

    llm = get_llm()
    result = llm.with_structured_output(SentimientoClasificado).invoke(
        f"Clasifica el sentimiento del usuario en este texto. "
        f"Considera: positivo (agradecido, satisfecho), neutro (informativo), "
        f"negativo (molesto, frustrado), furioso (muy enojado, agresivo).\n\n"
        f"Texto: {texto_analizar}"
    )

    return {"sentimiento": result.sentimiento}
