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

@tool
def consultar_estado_orden(
    order_id: Annotated[str, "ID numérico de la solicitud de soporte proporcionado por el usuario. Ejemplo: '5'. No llamar esta herramienta si el usuario no ha dado el ID."]
) -> str:
    """Consulta el estado de una solicitud de soporte usando su ID numérico.
    Solo llamar cuando el usuario haya proporcionado el ID explícitamente."""
    print(f"[HERRAMIENTA] Consultando estado de la solicitud {order_id}...")
    try:
        order_id_int = int(order_id)
        response = requests.get(f"https://jsonplaceholder.typicode.com/todos/{order_id_int}", timeout=5)
        print(response.json())
        if response.status_code == 200:
            data = response.json()
            estado = "Completada" if data["completed"] else "En tránsito"
            return f"La solicitud #{order_id_int} tiene el siguiente estado: {estado}."
        return f"No se encontró ninguna solicitud con el ID {order_id}."
    except ValueError:
        return "El ID proporcionado no es válido. Debe ser un número entero."
    except Exception as e:
        return f"Error al consultar la API: {str(e)}"