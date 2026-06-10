from bs4 import BeautifulSoup

from src.models.article import Article
from src.services.scraper import BaseScraper
from src.services.exceptions import ParseError


class WikipediaScraper(BaseScraper):
    """Scrapes article title and first paragraphs from Wikipedia."""

    def __init__(self, lang: str = "en", headers: dict | None = None, timeout: int | None = None):
        super().__init__(
            base_url=f"https://{lang}.wikipedia.org/wiki/",
            headers=headers,
            timeout=timeout,
        )

    def parse(self, html: str) -> Article:
        soup = BeautifulSoup(html, "lxml")  # Convierte el HTML en un árbol navegable

        for tag in soup.find_all("sup"):
            tag.decompose()

        # .get_text() --> extrae solo el texto sin las etiquetas
        heading = soup.find("h1", id="firstHeading")
        if heading is None:
            raise ParseError("Could not find the article title in the page.")
        title = heading.get_text()

        content = soup.find("div", class_="mw-parser-output")
        if content is None:
            raise ParseError("Could not find the article content in the page.")
        all_paragraphs = content.find_all("p")

        paragraphs = []
        for p in all_paragraphs:
            if p.get_text().strip(): #Filtra los <p> vacíos — si el texto está vacío, lo descarta
                paragraphs.append(p.get_text())
            if len(paragraphs) == 5:
                break

        return Article(title=title, paragraphs=paragraphs)