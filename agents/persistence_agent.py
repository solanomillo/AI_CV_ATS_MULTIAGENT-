"""
Agente encargado de registrar metadatos del análisis.
(No genera PDF automáticamente)
"""

from typing import Dict, Any
from domain.state import EstadoCV
from persistence.memory_store import MemoryStore


def agente_persistencia(estado: EstadoCV) -> Dict[str, Any]:
    """
    Guarda el análisis en SQLite pero mantiene el estado completo.
    """

    print("💾 Ejecutando agente de persistencia")

    try:
        store = MemoryStore()
        id_analisis, fecha = store.guardar_analisis(estado)

        # 🔥 IMPORTANTE: devolver el estado actualizado
        estado["id_analisis"] = id_analisis
        estado["fecha_analisis"] = fecha

    except Exception as e:
        print(f"⚠️ Error en persistencia: {e}")

    # 👇 MUY IMPORTANTE: retornar TODO el estado
    return estado