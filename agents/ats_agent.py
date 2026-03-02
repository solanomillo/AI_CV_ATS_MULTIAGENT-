"""
Agente encargado de analizar el CV como sistema ATS profesional.
"""

import json
from typing import Dict, Any

from pydantic import ValidationError

from domain.state import EstadoCV
from domain.models import ResultadoATS
from infrastructure.gemini_client import ClienteGemini
from utils.text_cleaner import limpiar_markdown, limpiar_lista_textos


def agente_analizador_ats(estado: EstadoCV) -> Dict[str, Any]:
    """
    Analiza el CV utilizando Gemini y devuelve un análisis estructurado.
    """
    print("🔥 Ejecutando analizador ATS")

    texto_cv = estado.get("texto_extraido")

    if not texto_cv:
        raise ValueError("No existe texto limpio para analizar.")

    cliente = ClienteGemini()

    prompt = f"""
    Actúa como un sistema ATS profesional utilizado por grandes empresas.

    Analiza el siguiente currículum de manera crítica y objetiva.

    Evalúa:
    1. Claridad y estructura
    2. Uso de palabras clave
    3. Impacto profesional
    4. Uso de métricas cuantificables
    5. Coherencia laboral

    Devuelve EXCLUSIVAMENTE un JSON válido con esta estructura:

    {{
        "score_ats": número entre 0 y 100,
        "fortalezas": ["lista de fortalezas"],
        "errores": ["lista de errores"],
        "mejoras": ["lista de mejoras accionables"],
        "resumen_general": "evaluación final profesional"
    }}

    Currículum:
    {texto_cv}
    """

    respuesta = cliente.generar_respuesta(prompt)

    if not respuesta:
        raise ValueError("El modelo no devolvió ninguna respuesta.")

    # Limpieza defensiva por si el modelo envía markdown
    respuesta = respuesta.strip()

    if respuesta.startswith("```"):
        respuesta = respuesta.replace("```json", "").replace("```", "").strip()

    try:
        datos = json.loads(respuesta)
        resultado = ResultadoATS(**datos)
        # 🔥 Limpieza profesional del contenido
        resultado.fortalezas = limpiar_lista_textos(resultado.fortalezas)
        resultado.errores = limpiar_lista_textos(resultado.errores)
        resultado.mejoras = limpiar_lista_textos(resultado.mejoras)
        resultado.resumen_general = limpiar_markdown(resultado.resumen_general)

    except json.JSONDecodeError as error:
        print("Respuesta cruda del modelo:")
        print(respuesta)
        raise ValueError(f"Error decodificando JSON: {error}")

    except ValidationError as error:
        print("JSON recibido:")
        print(respuesta)
        raise ValueError(f"Error validando estructura con Pydantic: {error}")
    
    return {
    "score_llm": resultado.score_ats,
    "fortalezas": resultado.fortalezas,
    "errores": resultado.errores,
    "mejoras": resultado.mejoras,
    "resumen_general": resultado.resumen_general
    }