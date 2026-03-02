"""Aplicación Flask para el agente de soporte."""

from flask import Flask, jsonify, request, send_file
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from agent import create_app as create_agent_app

app = Flask(__name__)
agent = create_agent_app(checkpointer=MemorySaver())


@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint único para la conversación.

    Body JSON:
        - message (str): Mensaje del usuario
        - thread_id (str, opcional): ID de conversación para mantener contexto

    Returns:
        JSON con la respuesta del agente, flujo de nodos ejecutados y sentimiento (si aplica).
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "El campo 'message' es requerido"}), 400

    thread_id = data.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [HumanMessage(content=message)]}

    ultima_respuesta = None
    flow = []
    sentimiento = None

    for event in agent.stream(inputs, config=config, stream_mode="updates"):
        for node_name, state_update in event.items():
            flow.append(node_name)
            if "sentimiento" in state_update:
                sentimiento = state_update["sentimiento"]
            if "messages" in state_update and state_update["messages"]:
                for msg in reversed(state_update["messages"]):
                    if isinstance(msg, AIMessage) and msg.content:
                        ultima_respuesta = msg.content
                        break

    response = {"response": ultima_respuesta}
    if sentimiento is not None:
        response["sentimiento"] = sentimiento

    return jsonify(response)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
