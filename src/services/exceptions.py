class ScraperError(Exception):
    """Base exception for all scraper errors."""


class ScraperConnectionError(ScraperError):
    """Raised when the target site cannot be reached (network or timeout)."""


class ResourceNotFoundError(ScraperError):
    """Raised when the requested resource does not exist (e.g. HTTP 404)."""