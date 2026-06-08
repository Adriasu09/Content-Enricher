from src.config.settings import WIKIPEDIA_LANG
from src.services.wikipedia_scraper import WikipediaScraper
from src.services.exceptions import ResourceNotFoundError, ScraperConnectionError


def main():
    print("=== Content Enricher ===")
    topic = input("Enter a topic to search on Wikipedia: ")

    scraper = WikipediaScraper(lang=WIKIPEDIA_LANG)

    try:
        html = scraper.fetch_html(topic)
        article = scraper.parse(html)
    except ResourceNotFoundError:
        print(f"Article not found: '{topic}'. Try a different topic.")
        return
    except ScraperConnectionError:
        print("Could not connect to Wikipedia. Check your internet connection.")
        return

    if not article.paragraphs:
        print(f"Article '{article.title}' exists but has no readable content.")
        return

    print(f"\n📄 {article.title}")
    print("-" * 40)
    for i, paragraph in enumerate(article.paragraphs, start=1):
        print(f"\n[{i}] {paragraph}")


if __name__ == "__main__":
    main()