SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "it", "pt"]

class ConsoleUI:
    """Handles all interaction with the user (input and output)."""

    def ask_topic(self) -> str:
        """Ask for a non-empty topic, repeating until valid."""
        while True:
            topic = input("Enter a topic to search on Wikipedia: ").strip()
            if topic:
                return topic
            print("The topic cannot be empty. Please try again.")

    def ask_language(self) -> str:
        """Ask for a supported target language, repeating until valid."""
        while True:
            language = input(f"Enter the target language {SUPPORTED_LANGUAGES}: ").strip().lower()
            if language in SUPPORTED_LANGUAGES:
                return language
            print(f"Unsupported language. Choose one of: {SUPPORTED_LANGUAGES}")

    def render_article(self, article) -> None:
        """Display an article's title and paragraphs."""
        print(f"\n📄 {article.title}")
        print("-" * 40)
        for i, paragraph in enumerate(article.paragraphs, start=1):
            print(f"\n[{i}] {paragraph}")

    def show_message(self, message: str) -> None:
        """Display a simple message to the user."""
        print(message)

    def ask_menu_option(self) -> str:
        """Show the action menu and return the chosen option."""
        print("\nWhat would you like to do?")
        print("[1] Enrich the content with AI")
        print("[0] Exit")
        return input("Choose an option: ").strip()

    def render_enriched(self, enriched_text: str) -> None:
        """Display the AI-enriched content."""
        print("\n✨ Enriched content")
        print("-" * 40)
        print(enriched_text)