"""Construcción del grafo del agente con LangGraph."""

from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.nodes import agent_node
from agent.state import AgentState
from agent.tools import consultar_base_conocimiento, radicar_ticket

def _tools_condition(state: AgentState):
    """Wrapper para tools_condition con messages_key por defecto."""
    return tools_condition(state, messages_key="messages")


def create_app(checkpointer=None):
    """Compila y retorna la aplicación del grafo.

    Flujo: agent -> tools -> [sentiment si radicar_ticket] -> agent
    """
    if checkpointer is None:
        checkpointer = MemorySaver()

    tools = [consultar_base_conocimiento, radicar_ticket]
    tool_node = ToolNode(tools)

    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges("agent", _tools_condition, {"tools": "tools", "__end__": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=checkpointer)


app = create_app()
