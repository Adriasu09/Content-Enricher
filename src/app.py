from src.services.exceptions import ScraperError


class App:
    """Orchestrates the flow: console <-> services."""

    def __init__(self, console, scraper):
        self.console = console
        self.scraper = scraper

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
                self.console.show_message("Enrichment coming soon...")  # placeholder (CE-12)
            elif option == "0":
                self.console.show_message("Goodbye!")
                return
            else:
                self.console.show_message("Invalid option. Please try again.")