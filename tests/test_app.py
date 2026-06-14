from unittest.mock import Mock

from src.app import App
from src.services.exceptions import ResourceNotFoundError


def test_run_re_asks_topic_when_article_not_found():
    # Arrange: la consola devuelve "Pythn" y luego "Python"; el menú sale con "0"
    console = Mock()
    console.ask_topic.side_effect = ["Pythn", "Python"]
    console.ask_language.return_value = "es"
    console.ask_yes_no.return_value = False

    # Arrange: el scraper falla al primer intento y funciona al segundo
    scraper = Mock()
    scraper.fetch_html.side_effect = [ResourceNotFoundError(), "<html>"]

    app = App(console=console, scraper=scraper, ai_service=Mock(), translate_service=Mock(), exporters=Mock())

    # Act
    app.run()

    # Assert: ¿qué dos cosas demuestran que la app re-preguntó y reintentó?
    assert console.ask_topic.call_count == 2
    assert scraper.fetch_html.call_count == 2