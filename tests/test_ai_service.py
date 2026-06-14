from unittest.mock import patch, MagicMock

import httpx
import pytest
from openai import APIConnectionError

from src.services.ai_service import AIService
from src.services.exceptions import AIAuthError, AIConnectionError


def test_enrich_returns_enriched_text():
    # Arrange: build a fake API response
    fake_message = MagicMock()
    fake_message.content = "Enriched text."
    fake_choice = MagicMock()
    fake_choice.message = fake_message
    fake_completion = MagicMock()
    fake_completion.choices = [fake_choice]

    with patch("src.services.ai_service.OpenAI") as MockOpenAI:
        MockOpenAI.return_value.chat.completions.create.return_value = fake_completion
        service = AIService(api_key="fake-key", base_url="http://fake", model="fake-model")

        # Act
        result = service.enrich("Some original text.")

    # Assert
    assert result == "Enriched text."


def test_missing_key_raises_auth_error():
    # Act & Assert: no key → AIAuthError, before any network call
    with pytest.raises(AIAuthError):
        AIService(api_key="", base_url="http://fake", model="fake-model")


def test_enrich_translates_connection_error():
    # Arrange
    request = httpx.Request("POST", "http://fake")

    with patch("src.services.ai_service.OpenAI") as MockOpenAI:
        MockOpenAI.return_value.chat.completions.create.side_effect = APIConnectionError(request=request)
        service = AIService(api_key="fake-key", base_url="http://fake", model="fake-model")

        # Act & Assert: the openai error is translated into our own
        with pytest.raises(AIConnectionError):
            service.enrich("Some original text.")