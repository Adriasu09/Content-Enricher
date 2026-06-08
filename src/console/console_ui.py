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