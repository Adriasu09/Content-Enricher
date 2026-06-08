from abc import ABC, abstractmethod

import requests

from src.models.article import Article
from src.services.exceptions import ScraperConnectionError, ResourceNotFoundError


class BaseScraper(ABC):
    """Source-agnostic scraper: fetches HTML and delegates parsing to subclasses."""
    # Valores por defecto, se pueden pasar otros valores
    DEFAULT_HEADERS = {
        "User-Agent": "ContentEnricher/1.0 (bootcamp project; educational use)"
    }
    DEFAULT_TIMEOUT = 10

    def __init__(self, base_url: str, headers: dict | None = None, timeout: int | None = None):
        self.base_url = base_url
        self.headers = headers or self.DEFAULT_HEADERS
        self.timeout = timeout or self.DEFAULT_TIMEOUT

    def fetch_html(self, query: str) -> str:
        url = self.build_url(query)
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise ScraperConnectionError(f"Request timed out for: {query}")
        except requests.exceptions.ConnectionError:
            raise ScraperConnectionError("Could not connect to the source.")

        if response.status_code == 404:
            raise ResourceNotFoundError(f"Resource not found: {query}")

        return response.text

    def build_url(self, query: str) -> str:
        """Build the full URL for a query. Subclasses may override if needed."""
        return self.base_url + query

    @abstractmethod
    def parse(self, html: str) -> Article:
        """Parse raw HTML into an Article. Each source defines its own logic."""