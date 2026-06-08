import requests
from src.config.settings import WIKIPEDIA_LANG
from bs4 import BeautifulSoup
from src.models.article import Article

class WikipediaConnectionError(Exception):
    pass

class ArticleNotFoundError(Exception):
    pass

class WikipediaService:
    BASE_URL = "https://{lang}.wikipedia.org/wiki/{topic}"
    HEADERS = {
        "User-Agent": "ContentEnricher/1.0 (bootcamp project; educational use)"
    }
    TIMEOUT = 10

    def fetch_html(self, topic: str) -> str:
        url = self.BASE_URL.format(lang=WIKIPEDIA_LANG, topic=topic)
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
        except requests.exceptions.Timeout:
            raise WikipediaConnectionError(f"Request timed out for topic: {topic}")
        except requests.exceptions.ConnectionError:
            raise WikipediaConnectionError("No internet connection.")

        if response.status_code == 404:
            raise ArticleNotFoundError(f"Article not found: {topic}")

        return response.text

    def parse_article(self, html: src) -> Article:
        soup = BeautifulSoup(html, "lxml") # Convierte el HTML en un árbol navegable

        for tag in soup.find_all("sup"):
            tag.decompose()

        #.get_text() --> extrae solo el texto sin las etiquetas
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
