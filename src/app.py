from src.services.exceptions import ScraperError, AIServiceError, TranslationError


class App:
    """Orchestrates the flow: console <-> services."""

    def __init__(self, console, scraper, ai_service, translate_service) -> None:
        self.console = console
        self.scraper = scraper
        self.ai_service = ai_service
        self.translate_service = translate_service

    def run(self) -> None:
        topic = self.console.ask_topic()
        language = self.console.ask_language()

        try:
            html = self.scraper.fetch_html(topic)
            article = self.scraper.parse(html)
        except ScraperError as e:
            self.console.show_message(str(e))
            return

        self.console.render_article(article)
        self._menu_loop(article, language)

    def _menu_loop(self, article, language) -> None:
        while True:
            option = self.console.ask_menu_option()
            if option == "1":
                self._enrich(article)
            elif option == "2":
                self._translate(article, language)
            elif option == "0":
                self.console.show_message("Goodbye!")
                return
            else:
                self.console.show_message("Invalid option. Please try again.")

    def _enrich(self, article) -> None:
        if article.enriched_content:
            self.console.show_message("Content is already enriched.")
            return
        self.console.show_message("Enriching content, please wait...")
        original_text = article.original_text()
        try:
            enriched = self.ai_service.enrich(original_text)
        except AIServiceError as e:
            self.console.show_message(str(e))
            return
        article.enriched_content = enriched
        self.console.render_enriched(enriched)

    def _translate(self, article, language) -> None:
        if article.translated_content:
            self.console.show_message("Content is already translated.")
            return
        self.console.show_message("Translating content, please wait...")
        text = article.original_text()
        if article.enriched_content:
            text = text + "\n\n" + article.enriched_content

        try:
            translated = self.translate_service.translate(text, language)
        except TranslationError as e:
            self.console.show_message(str(e))
            return
        article.translated_content = translated
        self.console.render_translated(translated)
