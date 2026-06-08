class ScraperError(Exception):
    """Base exception for all scraper errors."""


class ScraperConnectionError(ScraperError):
    """Raised when the target site cannot be reached (network or timeout)."""


class ResourceNotFoundError(ScraperError):
    """Raised when the requested resource does not exist (e.g. HTTP 404)."""

class ParseError(ScraperError):
    """Raised when the page was fetched but its structure could not be parsed."""