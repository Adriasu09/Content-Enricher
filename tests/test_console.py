from src.console.console_ui import ConsoleUI
from src.app import App
from src.models.article import Article
from unittest.mock import MagicMock


def test_ask_topic_repeats_until_valid(monkeypatch):
    # Arrange
    console = ConsoleUI()
    answers = iter(["", "   ", "Python"])     # dos inválidas, luego válida
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    # Act
    result = console.ask_topic()

    # Assert
    assert result == "Python"

def test_ask_language_rejects_unsupported(monkeypatch):
    # Arrange
    console = ConsoleUI()
    answers = iter(["xx", "klingon", "es"])   # dos inválidos, luego válido
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    # Act
    result = console.ask_language()

    # Assert
    assert result == "es"

class FakeConsole:
    """A fake console that feeds fixed answers and records what was shown."""

    def __init__(self):
        self.shown_article = None
        self.menu_calls = 0

    def ask_topic(self):
        return "Python"

    def ask_language(self):
        return "es"

    def render_article(self, article):
        self.shown_article = article

    def show_message(self, message):
        pass

    def ask_menu_option(self):
        # First call: choose exit, to leave the menu loop immediately
        self.menu_calls += 1
        return "0"


class FakeScraper:
    """A fake scraper that returns a fixed Article without touching the network."""

    def fetch_html(self, topic):
        return "<html>fake</html>"

    def parse(self, html):
        return Article(title="Python", paragraphs=["First.", "Second."])


def test_app_flow_shows_article_and_exits():
    # Arrange
    console = FakeConsole()
    scraper = FakeScraper()
    app = App(console=console, scraper=scraper, ai_service=MagicMock())

    # Act
    app.run()

    # Assert
    assert console.shown_article is not None
    assert console.shown_article.title == "Python"