class AppError(Exception):
    """Base class for all application errors."""
    default_message = "Something went wrong."
    hint = ""

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)

    def format_message(self) -> str:
        """User-facing text: message plus an optional hint."""
        if self.hint:
            return f"{self.message}\nHint: {self.hint}"
        return self.message


class ScraperError(AppError):
    """Base exception for all scraper errors."""
    default_message = "The scraper failed."


class ScraperConnectionError(ScraperError):
    """Raised when the target site cannot be reached (network or timeout)."""
    default_message = "Could not connect to the source."


class ResourceNotFoundError(ScraperError):
    """Raised when the requested resource does not exist (e.g. HTTP 404)."""
    default_message = "The requested resource was not found."
    hint = "Check the spelling or try a different topic."


class ParseError(ScraperError):
    """Raised when the page was fetched but its structure could not be parsed."""
    default_message = "The page could not be parsed."


class AIServiceError(AppError):
    """Base exception for all AI service errors."""
    default_message = "The AI service failed."


class AIAuthError(AIServiceError):
    """Raised when the AI API key is missing or invalid."""
    default_message = "Missing or invalid AI API key."
    hint = "Set GROQ_API_KEY in your .env file."


class AIConnectionError(AIServiceError):
    """Raised when the AI service cannot be reached (network or timeout)."""
    default_message = "Could not connect to the AI service."


class AIResponseError(AIServiceError):
    """Raised when the AI service returns an error response."""
    default_message = "The AI service returned an error. Please try again."


class TranslationError(AppError):
    """Base exception for all translation errors."""
    default_message = "The translation service failed. Please try again."


class UnsupportedLanguageError(TranslationError):
    """Raised when the target language is not supported by the translator."""
    default_message = "The target language is not supported."