class Article:
    """Represents a Wikipedia article and its versions."""
    def __init__(self, title: str, paragraphs: list[str]):
        self.title = title
        self.paragraphs = paragraphs
        self.enriched_content = ""
        self.translated_content = ""
        self.summary = ""