"""
Minimal Groq client. Groq's API is OpenAI-compatible, so this is just a
POST to /chat/completions. Kept deliberately small and side-effect-free
(injectable httpx.Client) so it's cheap to unit test with a mock transport.
"""

import httpx

from app.core.config import settings

GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"


class GroqError(Exception):
    pass


def chat_completion(
    messages: list[dict[str, str]],
    client: httpx.Client | None = None,
    max_tokens: int = 200,
    temperature: float = 0.4,
) -> str:
    """Returns the assistant message text. Raises GroqError on any failure."""
    if not settings.groq_api_key:
        raise GroqError("GROQ_API_KEY is not configured")

    owns_client = client is None
    client = client or httpx.Client(timeout=15.0)

    try:
        resp = client.post(
            GROQ_CHAT_COMPLETIONS_URL,
            headers={
                "Authorization": f"Bearer {settings.groq_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.groq_model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except httpx.HTTPError as exc:
        raise GroqError(f"Groq request failed: {exc}") from exc
    except (KeyError, IndexError, ValueError) as exc:
        raise GroqError(f"Unexpected Groq response shape: {exc}") from exc
    finally:
        if owns_client:
            client.close()
