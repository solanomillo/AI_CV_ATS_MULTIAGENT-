"""
Agente encargado de calcular el score híbrido del CV.

Combina score LLM + reglas determinísticas.
"""

import re
from typing import Dict, Any
from domain.state import EstadoCV


def agente_scoring(estado: EstadoCV) -> Dict[str, Any]:
    """
    Calcula el score basado en reglas objetivas
    y lo combina con el score del LLM.
    """

    print("🔥 Ejecutando agente de scoring híbrido")

    score_llm = estado.get("score_llm")
    fortalezas = estado.get("fortalezas") or []
    errores = estado.get("errores") or []
    texto = estado.get("texto_extraido") or ""

    # ----------- SCORE POR REGLAS -----------

    score_reglas = 50  # base neutral

    # Sumar por fortalezas
    score_reglas += min(len(fortalezas) * 5, 20)

    # Restar por errores
    score_reglas -= min(len(errores) * 7, 35)

    # Detectar métricas cuantificables (números, %)
    if re.search(r"\d+%|\d+", texto):
        score_reglas += 10

    # Limitar entre 0 y 100
    score_reglas = max(0, min(100, score_reglas))

    # ----------- SCORE FINAL HÍBRIDO -----------

    if score_llm is not None:
        score_final = int((score_llm * 0.6) + (score_reglas * 0.4))
    else:
        score_final = score_reglas

    return {
        "score_reglas": score_reglas,
        "score_final": score_final
    }