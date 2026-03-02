"""
Agente encargado de generar una versión optimizada del currículum.
Multi-nivel según el score final.
"""

from typing import Dict, Any
from domain.state import EstadoCV
from infrastructure.gemini_client import ClienteGemini
from utils.text_cleaner import limpiar_markdown


def agente_optimizador(estado: EstadoCV) -> Dict[str, Any]:
    """
    Genera una versión mejorada del CV basada en el análisis ATS.
    La fuerza de optimización depende del score final:
        - Score alto (>=85): optimización ligera
        - Score medio (60-84): optimización media
        - Score bajo (<60): optimización fuerte
    Siempre devuelve 'version_optimizada' para mantener consistencia en la UI.
    """
    print("🔥 Ejecutando optimizador")

    texto_original = estado.get("texto_extraido")
    errores = estado.get("errores")
    mejoras = estado.get("mejoras")
    score = estado.get("score_final", 0)

    if not texto_original:
        raise ValueError("No hay texto original para optimizar.")

    cliente = ClienteGemini()

    # 🔹 Determinar nivel de optimización
    if score >= 85:
        nivel = "ligera"
        prompt_intro = "Optimización LIGERA: mejorar formato y títulos, manteniendo la esencia del CV."
    elif score >= 60:
        nivel = "media"
        prompt_intro = "Optimización MEDIA: corregir errores, mejorar redacción y claridad."
    else:
        nivel = "fuerte"
        prompt_intro = "Optimización FUERTE: reescribir CV para ATS, mejorar impacto y estructura profesional."

    prompt = f"""
    Actúa como un experto en redacción profesional de currículums.

    NIVEL DE OPTIMIZACIÓN: {nivel.upper()}
    {prompt_intro}

    IMPORTANTE:
    - NO devuelvas JSON.
    - NO devuelvas estructuras con llaves {{ }}.
    - NO devuelvas listas en formato JSON.
    - Devuelve únicamente texto plano.
    - El resultado debe parecer un CV listo para enviar en Word o PDF.

    Requisitos obligatorios:
    - Usa títulos en MAYÚSCULAS.
    - Usa separadores con líneas (-----).
    - NO uses ** ni * ni # ni guiones de Markdown.
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

    texto_limpio = limpiar_markdown(respuesta)
    estado["version_optimizada"] = texto_limpio

    print(f"✅ Versión optimizada generada (nivel {nivel})")

    return estado