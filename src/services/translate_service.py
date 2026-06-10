from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException, BaseError

from src.services.exceptions import TranslationError, UnsupportedLanguageError


class TranslateService:
    """Translates text into a target language using deep-translator."""

    def translate(self, text: str, target_lang: str) -> str:
        """Translate text into the target language code (e.g. 'es', 'en')."""
        try:
            return GoogleTranslator(source="auto", target=target_lang).translate(text)
        except LanguageNotSupportedException as e:
            raise UnsupportedLanguageError(f"Unsupported target language: {target_lang}") from e
        except BaseError as e:
            raise TranslationError() from e