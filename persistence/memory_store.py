"""
Gestor de persistencia local utilizando SQLite.
"""

import sqlite3
from datetime import datetime
import uuid
import json


class MemoryStore:
    """
    Maneja la base de datos local del sistema.
    """

    def __init__(self, db_name: str = "analisis_cv.db"):
        self.db_name = db_name
        self._crear_tabla()

    def _crear_tabla(self):
        """
        Crea la tabla si no existe.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analisis (
                    id TEXT PRIMARY KEY,
                    fecha TEXT,
                    ruta_cv TEXT,
                    score_llm INTEGER,
                    score_reglas INTEGER,
                    score_final INTEGER,
                    fortalezas TEXT,
                    errores TEXT,
                    mejoras TEXT,
                    resumen TEXT,
                    version_optimizada TEXT
                )
            """)
            conn.commit()

    def guardar_analisis(self, datos: dict):
        """
        Guarda un análisis en la base de datos.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            id_analisis = str(uuid.uuid4())
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO analisis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_analisis,
                fecha,
                datos.get("ruta_cv"),
                datos.get("score_llm"),
                datos.get("score_reglas"),
                datos.get("score_final"),
                json.dumps(datos.get("fortalezas")),
                json.dumps(datos.get("errores")),
                json.dumps(datos.get("mejoras")),
                datos.get("resumen_general"),
                datos.get("version_optimizada")
            ))

            conn.commit()

        return id_analisis, fecha

    # 🔥 FASE 8 — HISTORIAL

    def obtener_historial(self):
        """
        Devuelve lista resumida de análisis.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, fecha, ruta_cv, score_final
                FROM analisis
                ORDER BY fecha DESC
            """)
            return cursor.fetchall()

    def obtener_analisis_por_id(self, id_analisis: str):
        """
        Devuelve análisis completo por ID.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM analisis WHERE id = ?
            """, (id_analisis,))
            fila = cursor.fetchone()

            if not fila:
                return None

            return {
                "id_analisis": fila[0],
                "fecha_analisis": fila[1],
                "ruta_cv": fila[2],
                "score_llm": fila[3],
                "score_reglas": fila[4],
                "score_final": fila[5],
                "fortalezas": json.loads(fila[6]) if fila[6] else [],
                "errores": json.loads(fila[7]) if fila[7] else [],
                "mejoras": json.loads(fila[8]) if fila[8] else [],
                "resumen_general": fila[9],
                "version_optimizada": fila[10],
            }
        
    def eliminar_analisis(self, id_analisis: str):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analisis WHERE id = ?", (id_analisis,))
            conn.commit()