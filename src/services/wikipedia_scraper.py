from bs4 import BeautifulSoup

from src.models.article import Article
from src.services.scraper import BaseScraper


class WikipediaScraper(BaseScraper):
    """Scrapes article title and first paragraphs from Wikipedia."""

    def __init__(self, lang: str = "en"):
        super().__init__(base_url=f"https://{lang}.wikipedia.org/wiki/")

    def parse(self, html: str) -> Article:
        soup = BeautifulSoup(html, "lxml")  # Convierte el HTML en un árbol navegable

        for tag in soup.find_all("sup"):
            tag.decompose()

        # .get_text() --> extrae solo el texto sin las etiquetas
        title = soup.find("h1", id="firstHeading").get_text()

        content = soup.find("div", class_="mw-parser-output")
        all_paragraphs = content.find_all("p")

        paragraphs = []
        for p in all_paragraphs:
            if p.get_text().strip(): #Filtra los <p> vacíos — si el texto está vacío, lo descarta
                paragraphs.append(p.get_text())
            if len(paragraphs) == 5:
                break

        return Article(title=title, paragraphs=paragraphs)