from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agent.state import AgentState
from agent.nodes import agent_node


def create_app(checkpointer: MemorySaver | None = None):
    builder = StateGraph(AgentState)

    builder.add_node("agent", agent_node)

    builder.add_edge(START, "agent")
    builder.add_edge("agent", END)

    return builder.compile(checkpointer=checkpointer)
