"""
Agente encargado de limpiar y normalizar el texto del CV.
"""

from typing import Dict, Any

from domain.state import EstadoCV


def agente_extractor(estado: EstadoCV) -> Dict[str, Any]:
    """
    Limpia el texto extraído del CV y lo normaliza.

    Parámetros:
        estado: EstadoCV actual del sistema.

    Retorna:
        Diccionario con las modificaciones del estado.
    """
    print("🔥 Ejecutando extractor")
    
    texto = estado.get("texto_extraido")

    if not texto:
        raise ValueError("No hay texto para procesar en el estado.")

    texto_limpio = " ".join(texto.split())

    return {
        "texto_extraido": texto_limpio
    }