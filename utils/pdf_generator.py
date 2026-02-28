from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generar_pdf(estado: dict, ruta: str):
    """
    Genera un PDF profesional con:
    - Score ATS
    - Fortalezas, errores y mejoras
    - Resumen general
    - Versión optimizada del CV
    """

    doc = SimpleDocTemplate(ruta)
    elementos = []

    estilos = getSampleStyleSheet()
    estilo_normal = estilos["Normal"]

    # --- Datos principales ---
    score = estado.get("score_final", "N/A")
    fortalezas = estado.get("fortalezas", [])
    errores = estado.get("errores", [])
    mejoras = estado.get("mejoras", [])
    resumen = estado.get("resumen_general", "")
    version_opt = estado.get("version_optimizada", "")

    # --- Título ---
    elementos.append(Paragraph("<b>AI CV ATS - Reporte Profesional</b>", estilos["Title"]))
    elementos.append(Spacer(1, 0.3 * inch))

    # --- Score ATS ---
    elementos.append(Paragraph(f"<b>Score ATS:</b> {score}/100", estilo_normal))
    elementos.append(Spacer(1, 0.2 * inch))

    # --- Fortalezas ---
    elementos.append(Paragraph("<b>Fortalezas:</b>", estilo_normal))
    if fortalezas:
        for f in fortalezas:
            elementos.append(Paragraph(f"- {f}", estilo_normal))
    else:
        elementos.append(Paragraph("No detectadas.", estilo_normal))
    elementos.append(Spacer(1, 0.2 * inch))

    # --- Errores ---
    elementos.append(Paragraph("<b>Errores:</b>", estilo_normal))
    if errores:
        for e in errores:
            elementos.append(Paragraph(f"- {e}", estilo_normal))
    else:
        elementos.append(Paragraph("No detectados.", estilo_normal))
    elementos.append(Spacer(1, 0.2 * inch))

    # --- Mejoras ---
    elementos.append(Paragraph("<b>Mejoras:</b>", estilo_normal))
    if mejoras:
        for m in mejoras:
            elementos.append(Paragraph(f"- {m}", estilo_normal))
    else:
        elementos.append(Paragraph("No detectadas.", estilo_normal))
    elementos.append(Spacer(1, 0.3 * inch))

    # --- Resumen general ---
    elementos.append(Paragraph("<b>Resumen General:</b>", estilo_normal))
    elementos.append(Paragraph(resumen or "N/A", estilo_normal))
    elementos.append(Spacer(1, 0.3 * inch))

    # --- Versión optimizada ---
    elementos.append(Paragraph("<b>Versión Optimizada del CV:</b>", estilo_normal))
    elementos.append(Paragraph(version_opt or "No se generó versión optimizada.", estilo_normal))

    # --- Generar PDF ---
    doc.build(elementos)