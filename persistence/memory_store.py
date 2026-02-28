"""
Gestor de persistencia local utilizando SQLite.
"""

import sqlite3
from datetime import datetime
import uuid


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
                    resumen TEXT
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
                INSERT INTO analisis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_analisis,
                fecha,
                datos.get("ruta_cv"),
                datos.get("score_llm"),
                datos.get("score_reglas"),
                datos.get("score_final"),
                str(datos.get("fortalezas")),
                str(datos.get("errores")),
                str(datos.get("mejoras")),
                datos.get("resumen_general"),
            ))

            conn.commit()

        return id_analisis, fecha