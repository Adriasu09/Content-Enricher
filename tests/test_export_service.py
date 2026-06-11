import os
from unittest.mock import patch

import pytest

from src.services.export_service import TxtExporter
from src.services.exceptions import ExportError


def test_txt_exporter_writes_file(tmp_path):
    # Arrange
    exporter = TxtExporter(output_dir=str(tmp_path))

    # Act
    path = exporter.export("Hello, file!", "article")

    # Assert
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as file:
        assert file.read() == "Hello, file!"


def test_export_translates_oserror(tmp_path):
    exporter = TxtExporter(output_dir=str(tmp_path))

    with patch("builtins.open", side_effect=OSError):
        # Act & Assert
        with pytest.raises(ExportError):
            exporter.export("Hello, file!", "article")