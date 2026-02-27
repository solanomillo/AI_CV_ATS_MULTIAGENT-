"""
Modelos de dominio utilizados para validar respuestas del sistema.
"""

from typing import List
from pydantic import BaseModel, Field


class ResultadoATS(BaseModel):
    """
    Representa la estructura obligatoria
    que debe devolver el agente ATS.
    """

    score_ats: int = Field(..., ge=0, le=100)
    fortalezas: List[str]
    errores: List[str]
    mejoras: List[str]
    resumen_general: str