from flask import Flask, request, jsonify
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from agent import create_app

flask_app = Flask(__name__)

_checkpointer = MemorySaver()
agent = create_app(checkpointer=_checkpointer)


@flask_app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True)
    if not body or "message" not in body or "thread_id" not in body:
        return jsonify({"error": "Se requieren los campos 'message' y 'thread_id'"}), 400

    message = body["message"]
    thread_id = body["thread_id"]

    config = {"configurable": {"thread_id": thread_id}}
    result = agent.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=config,
    )

    return jsonify({"response": result["messages"][-1].content})


if __name__ == "__main__":
    flask_app.run(debug=True, port=5000)
