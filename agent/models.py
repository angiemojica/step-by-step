"""Esquemas Pydantic para extracción estructurada."""

from typing import Literal

from pydantic import BaseModel, Field

class SentimientoClasificado(BaseModel):
    """Clasificación de sentimiento del usuario."""

    sentimiento: Literal["positivo", "neutro", "negativo", "furioso"] = Field(
        description="Sentimiento detectado en el texto del usuario."
    )
