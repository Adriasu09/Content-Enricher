class ScraperError(Exception):
    """Base exception for all scraper errors."""


class ScraperConnectionError(ScraperError):
    """Raised when the target site cannot be reached (network or timeout)."""


class ResourceNotFoundError(ScraperError):
    """Raised when the requested resource does not exist (e.g. HTTP 404)."""


class ParseError(ScraperError):
    """Raised when the page was fetched but its structure could not be parsed."""


class AIServiceError(Exception):
    """Base exception for all AI service errors."""


class AIAuthError(AIServiceError):
    """Raised when the AI API key is missing or invalid."""


class AIConnectionError(AIServiceError):
    """Raised when the AI service cannot be reached (network or timeout)."""


class AIResponseError(AIServiceError):
    """Raised when the AI service returns an error response."""


class TranslationError(Exception):
    """Base exception for all translation errors."""


class UnsupportedLanguageError(TranslationError):
    """Raised when the target language is not supported by the translator."""