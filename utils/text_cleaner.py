"""
Utilidades para limpieza de texto generado por LLM.
Elimina formato Markdown y caracteres no deseados.
"""

import re


def limpiar_markdown(texto: str) -> str:
    """
    Elimina formato Markdown común de respuestas LLM.
    """
    if not texto:
        return texto

    texto = texto.replace("**", "")
    texto = texto.replace("*", "")
    texto = texto.replace("#", "")

    # Eliminar bloques de código ``` ```
    texto = re.sub(r"```.*?```", "", texto, flags=re.DOTALL)

    return texto.strip()


def limpiar_lista_textos(lista: list[str]) -> list[str]:
    """
    Limpia una lista de textos.
    """
    return [limpiar_markdown(item) for item in lista]