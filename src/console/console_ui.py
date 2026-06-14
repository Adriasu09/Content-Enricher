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

    def ask_choice(self, prompt: str, options: list[str]) -> str:
        """Show a numbered menu of options and return the chosen one."""
        while True:
            print(prompt)
            for i, option in enumerate(options, start=1):
                print(f"[{i}] {option}")
            answer = input("Choose an option (number): ").strip()
            if answer.isdigit():
                index = int(answer)
                if 1 <= index <= len(options):
                    return options[index - 1]
            print(f"Please enter a number between 1 and {len(options)}.")

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
        """Ask which content version to save, as a numbered menu."""
        return self.ask_choice("Which version do you want to save?", available)

    def ask_save_format(self) -> str:
        """Ask for the export format, as a numbered menu."""
        return self.ask_choice("Which format do you want?", EXPORT_FORMATS)

    def ask_filename(self) -> str:
        """Ask for a non-empty file name, repeating until valid."""
        while True:
            filename = input("Enter the name you want to save the file as: ").strip()
            if filename:
                return filename
            print("The file name cannot be empty. Please try again.")
