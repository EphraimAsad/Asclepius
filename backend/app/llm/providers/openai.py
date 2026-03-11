"""
OpenAI LLM provider implementation (stub).

This is a stub implementation for future use.
To enable, set LLM_PROVIDER=openai and provide LLM_API_KEY.
"""

import logging
from typing import TYPE_CHECKING

from ..base import EnhancementContext, EnhancedResult, LLMProvider

if TYPE_CHECKING:
    from app.config import Settings

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider (stub implementation).

    This provider uses the OpenAI API for text generation.
    Requires an API key to be configured.

    Note: This is a stub. Full implementation requires the openai package.
    """

    def __init__(self, settings: "Settings"):
        self._api_key = settings.llm_api_key
        self._model = settings.llm_model or "gpt-4o-mini"
        self._timeout = settings.llm_timeout_seconds

        if not self._api_key:
            logger.warning("OpenAI provider initialized without API key")

    @property
    def provider_name(self) -> str:
        return "openai"

    async def health_check(self) -> bool:
        """Check if OpenAI is configured and accessible."""
        if not self._api_key:
            return False

        # TODO: Implement actual health check with openai package
        # try:
        #     import openai
        #     client = openai.AsyncOpenAI(api_key=self._api_key)
        #     await client.models.list()
        #     return True
        # except Exception:
        #     return False

        logger.warning("OpenAI health check not implemented - stub provider")
        return False

    async def enhance(self, context: EnhancementContext) -> EnhancedResult:
        """Enhance the explanation using OpenAI.

        Note: This is a stub that returns the original explanation.
        Full implementation requires the openai package.
        """
        logger.warning("OpenAI enhancement not implemented - returning original")

        # TODO: Implement with openai package
        # import openai
        # client = openai.AsyncOpenAI(api_key=self._api_key)
        # response = await client.chat.completions.create(
        #     model=self._model,
        #     messages=[
        #         {"role": "system", "content": ENHANCEMENT_SYSTEM_PROMPT},
        #         {"role": "user", "content": format_enhancement_prompt(...)}
        #     ],
        #     temperature=0.7,
        #     max_tokens=500
        # )
        # enhanced = response.choices[0].message.content

        return EnhancedResult(
            enhanced_explanation=context.explanation,
            follow_up_questions=[],
            from_cache=False
        )
