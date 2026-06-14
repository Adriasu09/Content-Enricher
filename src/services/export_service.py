import os
from abc import ABC, abstractmethod

from src.services.exceptions import ExportError


class Exporter(ABC):
    """Format-agnostic exporter: builds the output path, delegates writing."""

    extension = ""  # each subclass sets its own, e.g. ".txt"

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir

    def build_path(self, filename: str) -> str:
        """Ensure the output folder exists and return the full file path."""
        os.makedirs(self.output_dir, exist_ok=True)
        return os.path.join(self.output_dir, filename + self.extension)

    @abstractmethod
    def export(self, content: str, filename: str) -> str:
        """Write content to a file and return its absolute path."""

class TxtExporter(Exporter):
    """Exports content to a plain-text .txt file."""

    extension = ".txt"

    def export(self, content: str, filename: str) -> str:
        path = self.build_path(filename)
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
        except OSError as e:
            raise ExportError() from e
        return os.path.abspath(path)