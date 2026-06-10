from src.services.exceptions import ScraperError, ResourceNotFoundError


def test_default_message_when_raised_bare():
    error = ResourceNotFoundError()
    assert str(error) == "The requested resource was not found."


def test_custom_message_overrides_default():
    error = ResourceNotFoundError("Resource not found: Pythn")
    assert str(error) == "Resource not found: Pythn"


def test_format_message_includes_hint():
    error = ResourceNotFoundError()
    assert "Hint: Check the spelling" in error.format_message()


def test_format_message_without_hint_is_just_the_message():
    error = ScraperError()
    assert error.format_message() == "The scraper failed."