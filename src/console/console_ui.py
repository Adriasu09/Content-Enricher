SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "it", "pt"]
EXPORT_FORMATS = ["txt", "pdf"]


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

    def ask_yes_no(self, question: str) -> bool:
        """Ask a yes/no question, repeating until valid. Returns True for yes."""
        while True:
            answer = input(f"{question} (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please answer 'y' or 'n'.")

    def render_article(self, article) -> None:
        """Display an article's title and paragraphs."""
        print(f"\n📄 {article.title}")
        print("-" * 40)
        for i, paragraph in enumerate(article.paragraphs, start=1):
            print(f"\n[{i}] {paragraph}")

    def show_message(self, message: str) -> None:
        """Display a simple message to the user."""
        print(message)

    def render_enriched(self, enriched_text: str) -> None:
        """Display the AI-enriched content."""
        print("\n✨ Enriched content")
        print("-" * 40)
        print(enriched_text)

    def render_translated(self, translated_text: str) -> None:
        """Display the translated content."""
        print("\n✨ Translated content")
        print("-" * 40)
        print(translated_text)

    def ask_save_content(self, available: list[str]) -> str:
        """Ask which content version to save, repeating until valid."""
        while True:
            version = input(f"Enter the content version {available}: ").strip().lower()
            if version in available:
                return version
            print(f"Unsupported version. Choose one of: {available}")

    def ask_save_format(self) -> str:
        """Ask for a supported export format, repeating until valid."""
        while True:
            export_format = input(f"Enter the export format {EXPORT_FORMATS}: ").strip().lower()
            if export_format in EXPORT_FORMATS:
                return export_format
            print(f"Unsupported format. Choose one of: {EXPORT_FORMATS}")

    def ask_filename(self) -> str:
        """Ask for a non-empty file name, repeating until valid."""
        while True:
            filename = input("Enter the name you want to save the file as: ").strip()
            if filename:
                return filename
            print("The file name cannot be empty. Please try again.")
