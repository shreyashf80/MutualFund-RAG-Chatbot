"""
Groq LLM Client for Mutual Fund FAQ Assistant.
Wraps the Groq API for chat completion with automatic
fallback to a secondary model and retry logic.
"""

import logging
import time
from typing import Optional

from groq import Groq, APIError, RateLimitError, APIConnectionError

from src.config.settings import (
    GROQ_API_KEY,
    LLM_MODEL,
    LLM_FALLBACK_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
)

logger = logging.getLogger(__name__)

# Retry configuration
_MAX_RETRIES = 3
_BASE_DELAY = 1.0  # seconds, doubled each retry


class GroqClient:
    """
    Client for Groq LLM inference.

    Uses llama-3.3-70b-versatile as the primary model with automatic
    fallback to llama-3.1-8b-instant. Retries on rate limits and
    transient errors with exponential backoff.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        fallback_model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        self._api_key = api_key or GROQ_API_KEY
        if not self._api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Please configure it in your .env file."
            )

        self._client = Groq(api_key=self._api_key)
        self._model = model or LLM_MODEL
        self._fallback_model = fallback_model or LLM_FALLBACK_MODEL
        self._temperature = temperature if temperature is not None else LLM_TEMPERATURE
        self._max_tokens = max_tokens if max_tokens is not None else LLM_MAX_TOKENS

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate a chat completion using Groq.

        Tries the primary model first. On failure, falls back to the
        secondary model. Retries with exponential backoff on rate limits
        and transient API errors.

        Args:
            system_prompt: The system instruction for the LLM.
            user_prompt: The user's message (query + context).

        Returns:
            The generated text response.

        Raises:
            RuntimeError: If all retries and fallback are exhausted.
        """
        models_to_try = [self._model, self._fallback_model]

        for model in models_to_try:
            try:
                return self._call_with_retries(model, system_prompt, user_prompt)
            except Exception as e:
                logger.warning(
                    f"Model '{model}' failed after retries: {e}. "
                    f"{'Trying fallback...' if model == self._model else 'No more fallbacks.'}"
                )
                if model == self._fallback_model:
                    raise RuntimeError(
                        "All LLM models failed. Please try again later."
                    ) from e

        # Should not reach here, but just in case
        raise RuntimeError("LLM generation failed unexpectedly.")

    def _call_with_retries(
        self, model: str, system_prompt: str, user_prompt: str
    ) -> str:
        """
        Call the Groq API with exponential backoff on retryable errors.
        """
        last_error = None

        for attempt in range(_MAX_RETRIES):
            try:
                response = self._client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=self._temperature,
                    max_tokens=self._max_tokens,
                )

                content = response.choices[0].message.content
                if not content:
                    logger.warning(f"Empty response from model '{model}'.")
                    return ""

                logger.info(
                    f"Groq response generated. Model: {model}, "
                    f"Tokens: {response.usage.total_tokens if response.usage else 'N/A'}"
                )
                return content.strip()

            except RateLimitError as e:
                last_error = e
                delay = _BASE_DELAY * (2 ** attempt)
                logger.warning(
                    f"Rate limited (attempt {attempt + 1}/{_MAX_RETRIES}). "
                    f"Retrying in {delay}s..."
                )
                time.sleep(delay)

            except APIConnectionError as e:
                last_error = e
                delay = _BASE_DELAY * (2 ** attempt)
                logger.warning(
                    f"Connection error (attempt {attempt + 1}/{_MAX_RETRIES}). "
                    f"Retrying in {delay}s..."
                )
                time.sleep(delay)

            except APIError as e:
                last_error = e
                if e.status_code and e.status_code >= 500:
                    delay = _BASE_DELAY * (2 ** attempt)
                    logger.warning(
                        f"Server error {e.status_code} "
                        f"(attempt {attempt + 1}/{_MAX_RETRIES}). "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    # Non-retryable API error (4xx)
                    raise

        raise last_error or RuntimeError(f"All {_MAX_RETRIES} retries exhausted.")
