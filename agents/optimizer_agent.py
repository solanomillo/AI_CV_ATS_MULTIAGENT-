"""
Agente encargado de generar una versión optimizada del currículum.
"""

from typing import Dict, Any
from domain.state import EstadoCV
from infrastructure.gemini_client import ClienteGemini


def agente_optimizador(estado: EstadoCV) -> Dict[str, Any]:
    """
    Genera una versión mejorada del CV basada en el análisis ATS.
    """
    print("🔥 Ejecutando optimizador")

    texto_original = estado.get("texto_extraido")
    errores = estado.get("errores")
    mejoras = estado.get("mejoras")

    if not texto_original:
        raise ValueError("No hay texto original para optimizar.")

    cliente = ClienteGemini()

    prompt = f"""
    Actúa como un experto en redacción profesional de currículums.

    IMPORTANTE:
    - NO devuelvas JSON.
    - NO devuelvas estructuras con llaves {{ }}.
    - NO devuelvas listas en formato JSON.
    - Devuelve únicamente texto plano.
    - El resultado debe parecer un CV listo para enviar en Word o PDF.

    Requisitos obligatorios:
    - Usa títulos en MAYÚSCULAS.
    - Usa separadores con líneas (-----).
    - Usa viñetas con "•".
    - Mantén formato limpio y profesional.
    - No incluyas explicaciones ni comentarios adicionales.

    Errores detectados:
    {errores}

    Mejoras sugeridas:
    {mejoras}

    CV original:
    {texto_original}

    Devuelve únicamente el CV optimizado en TEXTO PLANO.
    """

    respuesta = cliente.generar_respuesta(prompt)

    return {
        "version_optimizada": respuesta.strip()
    }