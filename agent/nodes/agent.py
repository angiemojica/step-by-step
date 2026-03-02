"""Nodo del agente: LLM con herramientas."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agent.config import get_llm
from agent.prompts import AGENT_SYSTEM_PROMPT
from agent.state import AgentState

# Chain construida una vez, reutilizada en cada invocación
_chain = (
    ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ])
    | get_llm()
)


def agent_node(state: AgentState) -> dict:
    """Nodo que ejecuta el LLM con herramientas enlazadas."""
    print("[NODO] Agente: Ejecutando...")
    response = _chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}

