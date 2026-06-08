from unittest.mock import patch, MagicMock

import requests

from src.services.wikipedia_scraper import WikipediaScraper
from src.services.exceptions import ResourceNotFoundError, ScraperConnectionError

SAMPLE_HTML = """
<html>
  <h1 id="firstHeading">Python</h1>
  <div class="mw-parser-output">
    <p>Primer párrafo real.</p>
    <p></p>
    <p>Segundo párrafo real.</p>
    <p>Tercer párrafo real.</p>
    <p>Cuarto párrafo real.</p>
    <p>Quinto párrafo real.</p>
    <p>Sexto párrafo real.</p>
  </div>
</html>
"""


def test_parse_returns_correct_title_and_paragraphs():
    # Arrange
    scraper = WikipediaScraper()
    mock_response = MagicMock()
    mock_response.text = SAMPLE_HTML
    mock_response.status_code = 200

    # Act
    with patch("src.services.scraper.requests.get", return_value=mock_response):
        html = scraper.fetch_html("Python")
    article = scraper.parse(html)

    # Assert
    assert article.title == "Python"
    assert len(article.paragraphs) == 5
    assert article.paragraphs[0] == "Primer párrafo real."


def test_parse_with_no_valid_paragraphs():
    # Arrange
    scraper = WikipediaScraper()
    empty_html = """
    <html>
      <h1 id="firstHeading">Vacío</h1>
      <div class="mw-parser-output">
        <p></p>
        <p>   </p>
      </div>
    </html>
    """

    # Act
    article = scraper.parse(empty_html)

    # Assert
    assert article.title == "Vacío"
    assert len(article.paragraphs) == 0


def test_parse_with_fewer_than_five_paragraphs():
    # Arrange
    scraper = WikipediaScraper()
    short_html = """
    <html>
      <h1 id="firstHeading">Short Article</h1>
      <div class="mw-parser-output">
        <p>First paragraph.</p>
        <p>Second paragraph.</p>
        <p>Third paragraph.</p>
      </div>
    </html>
    """

    # Act
    article = scraper.parse(short_html)

    # Assert
    assert article.title == "Short Article"
    assert len(article.paragraphs) == 3
    assert article.paragraphs[2] == "Third paragraph."


def test_fetch_html_raises_not_found_on_404():
    # Arrange
    scraper = WikipediaScraper()
    mock_response = MagicMock()
    mock_response.status_code = 404

    # Act & Assert
    with patch("src.services.scraper.requests.get", return_value=mock_response):
        try:
            scraper.fetch_html("nonexistent")
            assert False, "Should have raised ResourceNotFoundError"
        except ResourceNotFoundError:
            pass


def test_fetch_html_translates_connection_error():
    # Arrange
    scraper = WikipediaScraper()

    # Act & Assert
    with patch("src.services.scraper.requests.get",
               side_effect=requests.exceptions.ConnectionError):
        try:
            scraper.fetch_html("Python")
            assert False, "Should have raised ScraperConnectionError"
        except ScraperConnectionError:
            pass