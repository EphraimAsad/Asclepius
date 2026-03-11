"""
Ollama LLM provider implementation.

Uses the Ollama API at http://127.0.0.1:11434 for local LLM inference.
"""

import json
import logging
from typing import TYPE_CHECKING

import httpx

from ..base import EnhancementContext, EnhancedResult, LLMProvider
from ..prompts import (
    ENHANCEMENT_SYSTEM_PROMPT,
    FOLLOWUP_QUESTIONS_SYSTEM_PROMPT,
    format_enhancement_prompt,
    format_followup_prompt,
)
from ..cache import get_cache

if TYPE_CHECKING:
    from app.config import Settings

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    """Ollama LLM provider for local inference.

    Uses the Ollama HTTP API for text generation.
    Requires Ollama to be running locally with the configured model.
    """

    def __init__(self, settings: "Settings"):
        self._base_url = settings.llm_base_url.rstrip("/")
        self._model = settings.llm_model
        self._timeout = settings.llm_timeout_seconds
        self._cache = get_cache(
            max_size=1000,
            ttl_seconds=settings.llm_cache_ttl_seconds
        )

    @property
    def provider_name(self) -> str:
        return "ollama"

    async def health_check(self) -> bool:
        """Check if Ollama is running and the model is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self._base_url}/api/tags")
                if response.status_code != 200:
                    return False

                data = response.json()
                models = [m.get("name", "") for m in data.get("models", [])]

                # Check if our model (or a variant) is available
                model_base = self._model.split(":")[0]
                return any(model_base in m for m in models)

        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False

    async def enhance(self, context: EnhancementContext) -> EnhancedResult:
        """Enhance the explanation using Ollama.

        First checks the cache for a matching result. If not found,
        calls Ollama to generate the enhancement and follow-up questions.
        """
        # Check cache first
        cache_key = self._cache.make_key(
            matched_rules=context.matched_rules,
            chief_complaint=context.chief_complaint,
            symptoms=context.symptoms
        )

        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.debug(f"Cache hit for key {cache_key}")
            return cached

        # Generate enhancement
        try:
            enhanced_explanation = await self._generate_enhancement(context)
            follow_up_questions = await self._generate_followup_questions(context)

            result = EnhancedResult(
                enhanced_explanation=enhanced_explanation,
                follow_up_questions=follow_up_questions,
                from_cache=False
            )

            # Cache the result
            self._cache.set(cache_key, result)

            return result

        except Exception as e:
            logger.error(f"Ollama enhancement failed: {e}")
            # Return original explanation on failure
            return EnhancedResult(
                enhanced_explanation=context.explanation,
                follow_up_questions=[],
                from_cache=False
            )

    async def _generate_enhancement(self, context: EnhancementContext) -> str:
        """Generate the enhanced explanation."""
        prompt = format_enhancement_prompt(
            explanation=context.explanation,
            disposition=context.disposition,
            chief_complaint=context.chief_complaint,
            symptoms=context.symptoms
        )

        response = await self._call_ollama(
            system_prompt=ENHANCEMENT_SYSTEM_PROMPT,
            user_prompt=prompt
        )

        if response:
            return response.strip()

        return context.explanation

    async def _generate_followup_questions(self, context: EnhancementContext) -> list[str]:
        """Generate follow-up questions for the patient."""
        prompt = format_followup_prompt(
            chief_complaint=context.chief_complaint,
            symptoms=context.symptoms,
            disposition=context.disposition
        )

        response = await self._call_ollama(
            system_prompt=FOLLOWUP_QUESTIONS_SYSTEM_PROMPT,
            user_prompt=prompt
        )

        if response:
            return self._parse_questions_json(response)

        return []

    async def _call_ollama(self, system_prompt: str, user_prompt: str) -> str | None:
        """Make a request to the Ollama API."""
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                payload = {
                    "model": self._model,
                    "prompt": user_prompt,
                    "system": system_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 500
                    }
                }

                response = await client.post(
                    f"{self._base_url}/api/generate",
                    json=payload
                )

                if response.status_code != 200:
                    logger.error(f"Ollama returned status {response.status_code}")
                    return None

                data = response.json()
                return data.get("response", "")

        except httpx.TimeoutException:
            logger.warning(f"Ollama request timed out after {self._timeout}s")
            return None

        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            return None

    def _parse_questions_json(self, response: str) -> list[str]:
        """Parse the JSON array of questions from the response."""
        # Clean up response - remove any markdown code blocks
        text = response.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

        # Try to find JSON array in response
        try:
            # First try direct parse
            questions = json.loads(text)
            if isinstance(questions, list):
                return [str(q) for q in questions if isinstance(q, str)]

        except json.JSONDecodeError:
            pass

        # Try to extract array from text
        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start >= 0 and end > start:
                questions = json.loads(text[start:end])
                if isinstance(questions, list):
                    return [str(q) for q in questions if isinstance(q, str)]

        except json.JSONDecodeError:
            pass

        logger.warning(f"Failed to parse questions JSON: {text[:100]}")
        return []
