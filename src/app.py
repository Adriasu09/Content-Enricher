from src.services.exceptions import ScraperError, AIServiceError, TranslationError, ResourceNotFoundError, ExportError


class App:
    """Orchestrates the flow: console <-> services."""

    def __init__(self, console, scraper, ai_service, translate_service, exporters) -> None:
        self.console = console
        self.scraper = scraper
        self.ai_service = ai_service
        self.translate_service = translate_service
        self.exporters = exporters

    def run(self) -> None:
        topic = self.console.ask_topic()
        language = self.console.ask_language()

        while True:
            try:
                html = self.scraper.fetch_html(topic)
                article = self.scraper.parse(html)
                break  # éxito → salimos del bucle
            except ResourceNotFoundError as e:  # recuperable → otro intento
                self.console.show_message(e.format_message())
                topic = self.console.ask_topic()
            except ScraperError as e:  # el resto → avisar y salir
                self.console.show_message(e.format_message())
                return

        self.console.render_article(article)

        if self.console.ask_yes_no("Do you want to enrich the content with AI?"):
            self._enrich(article)

        if self.console.ask_yes_no("Do you want to translate the content?"):
            self._translate(article, language)

        if self.console.ask_yes_no("Do you want to save the content to a file?"):
            self._save(article)

    def _enrich(self, article) -> None:
        self.console.show_message("Enriching content, please wait...")
        original_text = article.original_text()
        try:
            enriched = self.ai_service.enrich(original_text)
        except AIServiceError as e:
            self.console.show_message(e.format_message())
            return
        article.enriched_content = enriched
        self.console.render_enriched(enriched)

    def _translate(self, article, language) -> None:
        self.console.show_message("Translating content, please wait...")
        text = article.original_text()
        if article.enriched_content:
            text = text + "\n\n" + article.enriched_content

        try:
            translated = self.translate_service.translate(text, language)
        except TranslationError as e:
            self.console.show_message(e.format_message())
            return
        article.translated_content = translated
        self.console.render_translated(translated)

    def _save(self, article) -> None:
        available = self._available_versions(article)
        version = self.console.ask_save_content(available)
        content = self._content_for(article, version)
        export_format = self.console.ask_save_format()
        filename = self.console.ask_filename()
        exporter = self.exporters.get(export_format)
        try:
            path = exporter.export(content, filename)
        except ExportError as e:
            self.console.show_message(e.format_message())
            return
        self.console.show_message(f"Saved! Your file is at: {path}")

    def _content_for(self, article, version: str) -> str:
        """Return the article content matching the chosen version."""
        if version == "original":
            return article.original_text()
        if version == "enriched":
            return article.enriched_content
        return article.translated_content

    def _available_versions(self, article) -> list[str]:
        """Return the versions that currently have content."""
        versions = ["original"]
        if article.enriched_content:
            versions.append("enriched")
        if article.translated_content:
            versions.append("translated")
        return versions
