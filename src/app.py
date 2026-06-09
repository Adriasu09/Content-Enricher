from src.services.exceptions import ScraperError, AIServiceError


class App:
    """Orchestrates the flow: console <-> services."""

    def __init__(self, console, scraper, ai_service) -> None:
        self.console = console
        self.scraper = scraper
        self.ai_service = ai_service

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
        self._menu_loop(article)

    def _menu_loop(self, article) -> None:
        while True:
            option = self.console.ask_menu_option()
            if option == "1":
                self._enrich(article)
            elif option == "0":
                self.console.show_message("Goodbye!")
                return
            else:
                self.console.show_message("Invalid option. Please try again.")

    def _enrich(self, article) -> None:
        self.console.show_message("Enriching content, please wait...")
        original_text = article.title + "\n\n" + "\n\n".join(article.paragraphs) #Une los párrafos en un solo texto, separados por línea en blanco
        try:
            enriched = self.ai_service.enrich(original_text)
        except AIServiceError as e:
            self.console.show_message(str(e))
            return
        article.enriched_content = enriched
        self.console.render_enriched(enriched)