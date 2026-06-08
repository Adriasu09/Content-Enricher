from src.services.wikipedia_service import (
    WikipediaService,
    ArticleNotFoundError,
    WikipediaConnectionError,
)


def main():
    print("=== Content Enricher ===")
    topic = input("Enter a topic to search on Wikipedia: ")

    service = WikipediaService()

    try:
        html = service.fetch_html(topic)
        article = service.parse_article(html)
    except ArticleNotFoundError:
        print(f"Article not found: '{topic}'. Try a different topic.")
        return
    except WikipediaConnectionError:
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