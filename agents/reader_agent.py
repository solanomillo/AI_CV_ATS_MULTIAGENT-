"""
Agente encargado de leer el archivo del CV
usando la capa de infraestructura.
"""

from typing import Dict, Any
from infrastructure.cv_reader import CVReader
from domain.state import EstadoCV



def agente_lector_cv(estado: EstadoCV) -> Dict[str, Any]:
    print("📄 Ejecutando lector de CV")

    ruta = estado.get("ruta_cv")

    if not ruta:
        raise ValueError("No se proporcionó la ruta del CV.")

    reader = CVReader()
    texto = reader.read(ruta)

    return {
        "texto_extraido": texto
    }