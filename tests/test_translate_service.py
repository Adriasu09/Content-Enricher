from unittest.mock import patch, MagicMock
import pytest
from src.services.translate_service import TranslateService
from src.services.exceptions import UnsupportedLanguageError
from deep_translator.exceptions import LanguageNotSupportedException


def test_translate_returns_translated_text():
    # Arrange: build fake response
    fake_translated = "Hola mundo"

    with patch("src.services.translate_service.GoogleTranslator") as MockTranslator:
        mock_instance = MagicMock()
        mock_instance.translate.return_value = fake_translated
        MockTranslator.return_value = mock_instance

        # Act
        result = TranslateService().translate("Hello world", "es")

    # Assert
    assert result == fake_translated


def test_translate_unsupported_language_raises_error():
    with patch("src.services.translate_service.GoogleTranslator") as MockTranslator:
        # Arrange
        mock_instance = MagicMock()
        mock_instance.translate.side_effect = LanguageNotSupportedException("xx")
        MockTranslator.return_value = mock_instance

        # Act & Assert
        with pytest.raises(UnsupportedLanguageError):
            TranslateService().translate("Hello", "xx")
