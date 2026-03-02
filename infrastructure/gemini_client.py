"""
Cliente centralizado para interactuar con la API de Gemini.

Este módulo encapsula la configuración y ejecución
de llamadas al modelo generativo utilizando el SDK oficial actualizado.
"""

import os
from typing import Any
from google import genai


class ClienteGemini:
    """
    Cliente responsable de interactuar con el modelo Gemini.
    """

    def __init__(self, modelo: str = "gemini-2.5-flash") -> None:
        """
        Inicializa el cliente configurando la API Key.
        """
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("La variable de entorno GEMINI_API_KEY no está configurada.")

        self._client = genai.Client(api_key=api_key)
        self._modelo = modelo

    def generar_respuesta(self, prompt: str) -> str:
        """
        Envía un prompt al modelo y devuelve el texto generado en formato plano.
        """
        try:
            response = self._client.models.generate_content(
                model=self._modelo,
                contents=prompt
                # 🔥 Eliminamos response_mime_type para evitar JSON forzado
            )

            if not response or not response.text:
                raise ValueError("El modelo no devolvió contenido.")

            return response.text.strip()

        except Exception as e:
            raise RuntimeError(f"Error al generar respuesta con Gemini: {e}") from e