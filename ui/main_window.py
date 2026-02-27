"""
Ventana principal del sistema ATS Multi-Agente.
Versión mejorada con UI profesional.
"""

import customtkinter as ctk
import json
import re
from application.graph_builder import construir_grafo


class VentanaPrincipal(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()

        self.title("AI CV ATS - Sistema Multi-Agente")
        self.geometry("950x650")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._grafo = construir_grafo()

        self._construir_interfaz()

    def _construir_interfaz(self) -> None:

        titulo = ctk.CTkLabel(
            self,
            text="AI CV ATS - Sistema Multi-Agente",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=15)

        self.boton_prueba = ctk.CTkButton(
            self,
            text="Analizar CV",
            command=self._probar_extractor,
            width=200,
            height=40
        )
        self.boton_prueba.pack(pady=10)

        self.score_label = ctk.CTkLabel(
            self,
            text="SCORE ATS: --",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.score_label.pack(pady=5)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=5)

        self.tabs = ctk.CTkTabview(self, width=850, height=400)
        self.tabs.pack(pady=20)

        self.tab_analisis = self.tabs.add("📊 Análisis ATS")
        self.tab_version = self.tabs.add("✨ Versión Optimizada")

        self.resultado = ctk.CTkTextbox(self.tab_analisis, width=800, height=350)
        self.resultado.pack(pady=10)

        self.version_box = ctk.CTkTextbox(self.tab_version, width=800, height=350)
        self.version_box.pack(pady=10)

    def _probar_extractor(self) -> None:

        estado_inicial = {
            "ruta_cv": "",
            "texto_extraido": """
            Desarrollador backend con experiencia en Python.
            Trabajé en APIs y bases de datos.
            """,
            "analisis_ats": None,
            "version_optimizada": None,
            "score_final": None,
            "fortalezas": None,
            "errores": None,
            "mejoras": None,
            "pdf_generado": None
        }

        self.boton_prueba.configure(state="disabled", text="Analizando CV...")
        self.update()

        try:
            resultado = self._grafo.invoke(estado_inicial)

            self._actualizar_score(resultado.get("score_final"))
            self._mostrar_analisis(resultado)
            self._mostrar_version_optimizada(resultado)

        except Exception as e:
            self.resultado.delete("1.0", "end")
            self.resultado.insert("1.0", f"Error:\n\n{e}")

        finally:
            self.boton_prueba.configure(state="normal", text="Analizar CV")

    def _actualizar_score(self, score):

        if not score:
            return

        porcentaje = score / 100
        self.progress.set(porcentaje)

        if score < 40:
            color = "red"
        elif score < 70:
            color = "orange"
        else:
            color = "green"

        self.score_label.configure(
            text=f"SCORE ATS: {score}/100",
            text_color=color
        )

    def _mostrar_analisis(self, resultado):

        fortalezas = resultado.get("fortalezas") or []
        errores = resultado.get("errores") or []
        mejoras = resultado.get("mejoras") or []
        resumen = resultado.get("analisis_ats", "")

        texto = "FORTALEZAS:\n"
        texto += "- " + "\n- ".join(fortalezas) if fortalezas else "No detectadas."

        texto += "\n\nERRORES:\n"
        texto += "- " + "\n- ".join(errores) if errores else "No detectados."

        texto += "\n\nMEJORAS:\n"
        texto += "- " + "\n- ".join(mejoras) if mejoras else "No detectadas."

        texto += f"\n\nRESUMEN GENERAL:\n{resumen}"

        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", texto)

    def _mostrar_version_optimizada(self, resultado):

        version = resultado.get("version_optimizada")

        self.version_box.delete("1.0", "end")

        if not version:
            self.version_box.insert("1.0", "No se generó versión optimizada.")
            return

        version_limpia = self._normalizar_respuesta(version)

        self.version_box.insert("1.0", version_limpia)

    # 🔥 NORMALIZADOR INTELIGENTE

    def _normalizar_respuesta(self, respuesta):

        if not isinstance(respuesta, str):
            return str(respuesta)

        # Quitar bloques ```json
        respuesta = re.sub(r"```json|```", "", respuesta).strip()

        # Intentar parsear JSON
        try:
            data = json.loads(respuesta)
            return self._json_a_texto(data)
        except Exception:
            return respuesta

    def _json_a_texto(self, data):

        if not isinstance(data, dict):
            return str(data)

        texto = []

        texto.append(data.get("nombre", "").upper())
        texto.append(data.get("titulo", "").upper())
        texto.append("-" * 50)

        contacto = data.get("contacto", {})
        if contacto:
            texto.append("\nCONTACTO")
            for key, value in contacto.items():
                texto.append(f"{key.capitalize()}: {value}")

        resumen = data.get("resumenProfesional")
        if resumen:
            texto.append("\nRESUMEN PROFESIONAL")
            texto.append(resumen)

        experiencia = data.get("experienciaLaboral", [])
        if experiencia:
            texto.append("\nEXPERIENCIA LABORAL")
            for exp in experiencia:
                texto.append(f"\n{exp.get('posicion')} - {exp.get('empresa')}")
                texto.append(f"{exp.get('fechaInicio')} - {exp.get('fechaFin')}")
                for r in exp.get("responsabilidades", []):
                    texto.append(f"• {r}")

        return "\n".join(texto)