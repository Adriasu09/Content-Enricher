from unittest.mock import Mock
from src.app import App
from src.models.article import Article
from src.services.export_service import TxtExporter


class ScriptedConsole:
    """A console that returns pre-set answers, scripting a full run."""

    def __init__(self, filename):
        self.filename = filename
        self.yes_no_answers = iter([True, True, True])  # enrich? translate? save?

    def ask_topic(self):
        return "Python"

    def ask_language(self):
        return "es"

    def ask_yes_no(self, question):
        return next(self.yes_no_answers)

    def ask_save_content(self, available):
        return "translated"

    def ask_save_format(self):
        return "txt"

    def ask_filename(self):
        return self.filename

    def render_article(self, article):
        pass

    def render_enriched(self, text):
        pass

    def render_translated(self, text):
        pass

    def show_message(self, message):
        pass


def test_full_flow_writes_translated_file(tmp_path):
    # Arrange: servicios mockeados (sin red ni dinero)
    scraper = Mock()
    scraper.fetch_html.return_value = "<html>fake</html>"
    scraper.parse.return_value = Article(title="Python", paragraphs=["First.", "Second."])

    ai_service = Mock()
    ai_service.enrich.return_value = "Enriched text."

    translate_service = Mock()
    translate_service.translate.return_value = "Texto traducido."

    # Exporter REAL escribiendo en la carpeta temporal
    exporters = {"txt": TxtExporter(output_dir=str(tmp_path))}

    console = ScriptedConsole(filename="result")

    app = App(
        console=console,
        scraper=scraper,
        ai_service=ai_service,
        translate_service=translate_service,
        exporters=exporters,
    )

    # Act: recorre todo el flujo lineal de principio a fin
    app.run()

    # Assert: el Article acumuló las tres versiones...
    saved_file = tmp_path / "result.txt"
    assert saved_file.exists()
    assert saved_file.read_text(encoding="utf-8") == "Texto traducido."