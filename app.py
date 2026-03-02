from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from agent import create_app

agent = create_app(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "test-1"}}

result = agent.invoke(
    {"messages": [HumanMessage("Hola, ¿qué puedes hacer?")]},
    config=config,
)
print(result["messages"][-1].content)
