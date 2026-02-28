"""
Agente encargado de guardar el análisis en la base de datos local.
"""

from typing import Dict, Any
from domain.state import EstadoCV
from persistence.memory_store import MemoryStore


def agente_persistencia(estado: EstadoCV) -> Dict[str, Any]:
    """
    Guarda el análisis final en SQLite.
    """

    print("🔥 Ejecutando agente de persistencia")

    store = MemoryStore()

    id_analisis, fecha = store.guardar_analisis(estado)

    return {
        "id_analisis": id_analisis,
        "fecha_analisis": fecha
    }