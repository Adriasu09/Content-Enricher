from openai import (
    OpenAI,
    AuthenticationError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    APIError,
)

from src.services.exceptions import (
    AIAuthError,
    AIConnectionError,
    AIResponseError,
)

ENRICH_SYSTEM_PROMPT = (
    "You are a helpful assistant that enriches encyclopedic content. "
    "Expand and improve the given text with useful context and clearer wording, "
    "while staying accurate and concise. Respond in the same language as the input."
)


class AIService:
    """Enriches text using an OpenAI-compatible AI provider."""

    DEFAULT_MAX_TOKENS = 400

    def __init__(self, api_key: str, base_url: str, model: str, max_tokens: int | None = None):
        if not api_key:
            raise AIAuthError()
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS

    def enrich(self, text: str) -> str:
        """Send text to the AI and return the enriched version."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ENRICH_SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                max_tokens=self.max_tokens,
            )
        except AuthenticationError as e:
            raise AIAuthError() from e
        except (APIConnectionError, APITimeoutError) as e:
            raise AIConnectionError() from e
        except (RateLimitError, APIError) as e:
            raise AIResponseError() from e

        content = response.choices[0].message.content
        if content is None:
            raise AIResponseError("The AI returned an empty response.")
        return content
