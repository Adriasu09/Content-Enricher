from unittest.mock import patch, MagicMock
from src.services.wikipedia_service import (
    WikipediaService,
    ArticleNotFoundError,
    WikipediaConnectionError,
)

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


def test_parse_article_returns_correct_title_and_paragraphs():
    # Arrange
    service = WikipediaService()
    mock_response = MagicMock()
    mock_response.text = SAMPLE_HTML
    mock_response.status_code = 200

    # Act
    with patch("src.services.wikipedia_service.requests.get", return_value=mock_response):
        html = service.fetch_html("Python")
    article = service.parse_article(html)

    # Assert
    assert article.title == "Python"
    assert len(article.paragraphs) == 5
    assert article.paragraphs[0] == "Primer párrafo real."

def test_parse_article_with_no_valid_paragraphs():
    # Arrange
    service = WikipediaService()
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
    article = service.parse_article(empty_html)

    # Assert
    assert article.title == "Vacío"
    assert len(article.paragraphs) == 0

def test_parse_article_with_fewer_than_five_paragraphs():
    # Arrange
    service = WikipediaService()
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
    article = service.parse_article(short_html)

    # Assert
    assert article.title == "Short Article"
    assert len(article.paragraphs) == 3
    assert article.paragraphs[2] == "Third paragraph."

def test_fetch_html_raises_on_404():
    # Arrange
    service = WikipediaService()
    mock_response = MagicMock()
    mock_response.status_code = 404

    # Act & Assert
    with patch("src.services.wikipedia_service.requests.get", return_value=mock_response):
        try:
            service.fetch_html("tema_inexistente")
            assert False, "Debería haber lanzado ArticleNotFoundError"
        except ArticleNotFoundError:
            pass


def test_fetch_html_raises_on_connection_error():
    # Arrange
    service = WikipediaService()

    # Act & Assert
    with patch("src.services.wikipedia_service.requests.get",
               side_effect=WikipediaConnectionError("No internet connection.")):
        try:
            service.fetch_html("Python")
            assert False, "Debería haber lanzado WikipediaConnectionError"
        except WikipediaConnectionError:
            pass