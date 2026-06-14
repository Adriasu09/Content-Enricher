class Article:
    """Represents a Wikipedia article and its versions."""
    def __init__(self, title: str, paragraphs: list[str]):
        self.title = title
        self.paragraphs = paragraphs
        self.enriched_content = ""
        self.translated_content = ""
        self.summary = ""

    def original_text(self) -> str:
        """Return title and paragraphs as a single plain-text block."""
        return self.title + "\n\n" + "\n\n".join(self.paragraphs)