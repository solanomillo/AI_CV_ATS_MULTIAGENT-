"""
Definición del estado compartido del sistema multi-agente.

Este archivo define la estructura tipada que circulará
entre los nodos del grafo de LangGraph.
"""

from typing import TypedDict, Optional, List


class EstadoCV(TypedDict):
    """
    Representa el estado global que fluye entre los agentes.

    Cada agente puede leer y modificar partes de este estado.
    """

    # Entrada
    ruta_cv: str
    texto_extraido: Optional[str]

    # Análisis ATS cualitativo
    fortalezas: Optional[List[str]]
    errores: Optional[List[str]]
    mejoras: Optional[List[str]]
    resumen_general: Optional[str]

    # Scoring
    score_llm: Optional[int]
    score_reglas: Optional[int]
    score_final: Optional[int]

    # Optimización
    version_optimizada: Optional[str]

    # Persistencia
    id_analisis: Optional[str]
    fecha_analisis: Optional[str]
    pdf_generado: Optional[str]