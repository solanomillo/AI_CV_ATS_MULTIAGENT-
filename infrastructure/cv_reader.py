from pathlib import Path
from typing import Union
from pypdf import PdfReader
from docx import Document


class CVReader:
    """
    Responsible for reading CV files (PDF or DOCX)
    and returning clean extracted text.
    """

    SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

    def read(self, file_path: Union[str, Path]) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError("El archivo no existe.")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("Formato no soportado. Solo PDF o DOCX.")

        if path.suffix.lower() == ".pdf":
            text = self._read_pdf(path)
        elif path.suffix.lower() == ".docx":
            text = self._read_docx(path)

        return self._clean_text(text)

    def _read_pdf(self, path: Path) -> str:
        try:
            reader = PdfReader(str(path))
            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            if not text.strip():
                raise ValueError("No se pudo extraer texto del PDF.")

            return text

        except Exception as e:
            raise ValueError(f"Error leyendo PDF: {str(e)}")

    def _read_docx(self, path: Path) -> str:
        try:
            doc = Document(str(path))
            text = "\n".join([para.text for para in doc.paragraphs])

            if not text.strip():
                raise ValueError("No se pudo extraer texto del DOCX.")

            return text

        except Exception as e:
            raise ValueError(f"Error leyendo DOCX: {str(e)}")

    def _clean_text(self, text: str) -> str:
        """
        Basic text normalization:
        - Remove excessive spaces
        - Normalize line breaks
        """
        text = text.replace("\r", "\n")
        text = "\n".join(line.strip() for line in text.splitlines())
        text = "\n".join(line for line in text.splitlines() if line)

        return text.strip()