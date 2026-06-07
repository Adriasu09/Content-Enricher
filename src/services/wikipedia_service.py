import requests
from src.config.settings import WIKIPEDIA_LANG

class WikipediaService:
    BASE_URL = "https://{lang}.wikipedia.org/wiki/{topic}"
    HEADERS = {
        "User-Agent": "ContentEnricher/1.0 (bootcamp project; educational use)"
    }
    TIMEOUT = 10

    def fetch_html(self, topic: str) -> str:
        url = self.BASE_URL.format(lang=WIKIPEDIA_LANG, topic=topic)
        response = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
        return response.text