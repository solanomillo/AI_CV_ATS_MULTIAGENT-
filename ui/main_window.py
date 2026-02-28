import customtkinter as ctk
import json
import re
import time
import sqlite3
from application.graph_builder import construir_grafo
from tkinter import filedialog, messagebox
from utils.pdf_generator import generar_pdf
from persistence.memory_store import MemoryStore


class VentanaPrincipal(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()

        self.title("AI CV ATS - Sistema Multi-Agente")
        self.geometry("950x650")
        self.ruta_seleccionada = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._grafo = construir_grafo()
        self.estado_actual = None

        self._agentes = [
            "lector_cv",
            "extractor",
            "analizador_ats",
            "scoring",
            "optimizador",
            "persistencia"
        ]

        self._construir_interfaz()

    # -------------------
    # INTERFAZ
    # -------------------

    def _construir_interfaz(self) -> None:

        titulo = ctk.CTkLabel(
            self,
            text="AI CV ATS - Sistema Multi-Agente",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=15)

        # 🔹 Frame botones horizontales
        self.frame_botones = ctk.CTkFrame(self)
        self.frame_botones.pack(pady=10)

        self.boton_seleccionar = ctk.CTkButton(
            self.frame_botones,
            text="Seleccionar CV (.pdf / .docx)",
            command=self._seleccionar_archivo,
            width=220,
            height=40
        )
        self.boton_seleccionar.pack(side="left", padx=5)

        self.boton_prueba = ctk.CTkButton(
            self.frame_botones,
            text="Analizar CV",
            command=self._probar_extractor,
            width=180,
            height=40
        )
        self.boton_prueba.pack(side="left", padx=5)

        self.boton_descargar = ctk.CTkButton(
            self.frame_botones,
            text="📥 Descargar Reporte PDF",
            command=self._descargar_pdf,
            width=220,
            height=40,
            state="disabled"
        )
        self.boton_descargar.pack(side="left", padx=5)

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
        self.tab_historial = self.tabs.add("📁 Historial")

        self.resultado = ctk.CTkTextbox(self.tab_analisis, width=800, height=350)
        self.resultado.pack(pady=10)

        self.version_box = ctk.CTkTextbox(self.tab_version, width=800, height=350)
        self.version_box.pack(pady=10)

        # 🔹 Historial
        self.lista_historial = ctk.CTkTextbox(self.tab_historial, width=800, height=300)
        self.lista_historial.pack(pady=10)

        self.frame_historial_botones = ctk.CTkFrame(self.tab_historial)
        self.frame_historial_botones.pack(pady=5)

        self.boton_cargar_historial = ctk.CTkButton(
            self.frame_historial_botones,
            text="Cargar Seleccionado",
            command=self._cargar_historial
        )
        self.boton_cargar_historial.pack(side="left", padx=5)

        self.boton_borrar_historial = ctk.CTkButton(
            self.frame_historial_botones,
            text="Borrar Seleccionado",
            command=self._borrar_historial
        )
        self.boton_borrar_historial.pack(side="left", padx=5)

        self._actualizar_historial()

    # -------------------
    # SELECCIONAR ARCHIVO
    # -------------------

    def _seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar CV",
            filetypes=[("Archivos PDF", "*.pdf"), ("Archivos Word", "*.docx")]
        )

        if not archivo:
            return

        if not archivo.lower().endswith((".pdf", ".docx")):
            messagebox.showerror("Formato inválido", "Solo se permiten archivos PDF o DOCX.")
            return

        self.ruta_seleccionada = archivo
        messagebox.showinfo("Archivo seleccionado", f"CV cargado correctamente:\n{archivo}")

    # -------------------
    # EJECUCIÓN DEL GRAFO
    # -------------------

    def _probar_extractor(self):

        if not self.ruta_seleccionada:
            messagebox.showerror("Error", "Primero debes seleccionar un CV.")
            return

        estado_inicial = {
            "ruta_cv": self.ruta_seleccionada,
            "texto_extraido": None,
            "fortalezas": None,
            "errores": None,
            "mejoras": None,
            "resumen_general": None,
            "score_llm": None,
            "score_reglas": None,
            "score_final": None,
            "version_optimizada": None,
            "id_analisis": None,
            "fecha_analisis": None,
            "pdf_generado": None
        }

        self.boton_prueba.configure(state="disabled", text="Analizando CV...")
        self.progress.set(0)
        self.update()

        try:
            total_agentes = len(self._agentes)
            for i, agente_nombre in enumerate(self._agentes, start=1):
                self.score_label.configure(text=f"Ejecutando: {agente_nombre}...")
                self.progress.set(i / total_agentes)
                self.update()
                time.sleep(0.3)

            resultado = self._grafo.invoke(estado_inicial)

            self.estado_actual = resultado
            self.boton_descargar.configure(state="normal")

            self._actualizar_score(resultado.get("score_final"))
            self._mostrar_analisis(resultado)
            self._mostrar_version_optimizada(resultado)

            self.progress.set(1)
            self._actualizar_historial()

        except Exception as e:

            error_texto = str(e)

            if "429" in error_texto or "quota" in error_texto.lower():
                messagebox.showerror(
                    "Límite de API alcanzado",
                    "Has superado el límite de uso de la API (Error 429).\n\n"
                    "Verifica tu plan o intenta más tarde."
                )
            else:
                messagebox.showerror("Error", error_texto)

        finally:
            self.boton_prueba.configure(state="normal", text="Analizar CV")

    # -------------------
    # UI RESULTADOS
    # -------------------

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

        self.score_label.configure(text=f"SCORE ATS: {score}/100", text_color=color)

    def _mostrar_analisis(self, resultado):
        fortalezas = resultado.get("fortalezas") or []
        errores = resultado.get("errores") or []
        mejoras = resultado.get("mejoras") or []
        resumen = resultado.get("resumen_general", "")

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
        version = resultado.get("version_optimizada", "No se generó versión optimizada.")
        self.version_box.delete("1.0", "end")
        self.version_box.insert("1.0", version)

    # -------------------
    # PDF
    # -------------------

    def _descargar_pdf(self):
        if not self.estado_actual:
            messagebox.showerror("Error", "No hay análisis disponible.")
            return

        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivo PDF", "*.pdf")],
            title="Guardar reporte como..."
        )

        if not ruta_guardado:
            return

        try:
            generar_pdf(self.estado_actual, ruta_guardado)
            messagebox.showinfo("Éxito", "Reporte PDF generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")

    # -------------------
    # HISTORIAL
    # -------------------

    def _actualizar_historial(self):
        store = MemoryStore()
        historial = store.obtener_historial()

        self.lista_historial.delete("1.0", "end")

        if not historial:
            self.lista_historial.insert("1.0", "No hay análisis guardados.")
            return

        for item in historial:
            id_, fecha, ruta, score = item
            linea = f"{id_} | {fecha} | Score: {score}\n"
            self.lista_historial.insert("end", linea)

    def _cargar_historial(self):
        try:
            contenido = self.lista_historial.get("sel.first", "sel.last").strip()
        except:
            messagebox.showerror("Error", "Selecciona un análisis del historial.")
            return

        id_analisis = contenido.split("|")[0].strip()

        store = MemoryStore()
        datos = store.obtener_analisis_por_id(id_analisis)

        if not datos:
            messagebox.showerror("Error", "No se encontró el análisis.")
            return

        self.estado_actual = datos
        self._actualizar_score(datos.get("score_final"))
        self._mostrar_analisis(datos)
        self._mostrar_version_optimizada(datos)
        self.boton_descargar.configure(state="normal")

        messagebox.showinfo("Cargado", "Análisis cargado correctamente.")

    def _borrar_historial(self):
        try:
            contenido = self.lista_historial.get("sel.first", "sel.last").strip()
        except:
            messagebox.showerror("Error", "Selecciona un análisis para borrar.")
            return

        id_analisis = contenido.split("|")[0].strip()

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Seguro que deseas eliminar este análisis?"
        )

        if not confirmar:
            return

        store = MemoryStore()

        with sqlite3.connect(store.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analisis WHERE id = ?", (id_analisis,))
            conn.commit()

        self._actualizar_historial()
        messagebox.showinfo("Eliminado", "Análisis eliminado correctamente.")