from src.config.settings import WIKIPEDIA_LANG, GROQ_API_KEY, AI_BASE_URL, AI_MODEL
from src.console.console_ui import ConsoleUI
from src.services.wikipedia_scraper import WikipediaScraper
from src.services.ai_service import AIService
from src.services.translate_service import TranslateService
from src.services.export_service import TxtExporter
from src.services.exceptions import AIAuthError
from src.app import App


def main():
    console = ConsoleUI()
    scraper = WikipediaScraper(lang=WIKIPEDIA_LANG)

    try:
        ai_service = AIService(api_key=GROQ_API_KEY, base_url=AI_BASE_URL, model=AI_MODEL)
    except AIAuthError as e:
        console.show_message(e.format_message())
        return

    translate_service = TranslateService()
    exporters = {"txt": TxtExporter()}

    app = App(console=console, scraper=scraper, ai_service=ai_service, translate_service=translate_service, exporters=exporters)
    app.run()


if __name__ == "__main__":
    main()