from src.config.settings import WIKIPEDIA_LANG
from src.console.console_ui import ConsoleUI
from src.services.wikipedia_scraper import WikipediaScraper
from src.app import App


def main():
    console = ConsoleUI()
    scraper = WikipediaScraper(lang=WIKIPEDIA_LANG)
    app = App(console=console, scraper=scraper)
    app.run()


if __name__ == "__main__":
    main()