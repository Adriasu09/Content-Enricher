import os

from fpdf import FPDF
from fpdf.errors import FPDFException

from src.services.export_service import Exporter
from src.services.exceptions import ExportError


class PdfExporter(Exporter):
    """Exports content to a PDF file."""

    extension = ".pdf"

    def export(self, content: str, filename: str) -> str:
        path = self.build_path(filename)
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            pdf.multi_cell(0, 8, content)
            pdf.output(path)
        except (OSError, FPDFException) as e:
            raise ExportError() from e
        return os.path.abspath(path)