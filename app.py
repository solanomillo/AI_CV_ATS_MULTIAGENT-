"""
Punto de entrada principal del sistema multi-agente AI CV ATS.
"""

import customtkinter as ctk
from dotenv import load_dotenv
from ui.main_window import VentanaPrincipal


def main() -> None:
    """
    Inicializa la aplicación.
    """
    load_dotenv()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = VentanaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()