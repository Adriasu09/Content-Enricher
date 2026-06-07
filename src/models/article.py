class Article:
    def __init__(self, title: str, paragraphs: list[str]):
        self.title = title
        self.paragraphs = paragraphs
        self.enriched_content = ""
        self.translated_content = ""
        self.summary = ""