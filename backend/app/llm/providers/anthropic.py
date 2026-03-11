"""
Anthropic LLM provider implementation (stub).

This is a stub implementation for future use.
To enable, set LLM_PROVIDER=anthropic and provide LLM_API_KEY.
"""

import logging
from typing import TYPE_CHECKING

from ..base import EnhancementContext, EnhancedResult, LLMProvider

if TYPE_CHECKING:
    from app.config import Settings

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    """Anthropic LLM provider (stub implementation).

    This provider uses the Anthropic API for text generation.
    Requires an API key to be configured.

    Note: This is a stub. Full implementation requires the anthropic package.
    """

    def __init__(self, settings: "Settings"):
        self._api_key = settings.llm_api_key
        self._model = settings.llm_model or "claude-3-haiku-20240307"
        self._timeout = settings.llm_timeout_seconds

        if not self._api_key:
            logger.warning("Anthropic provider initialized without API key")

    @property
    def provider_name(self) -> str:
        return "anthropic"

    async def health_check(self) -> bool:
        """Check if Anthropic is configured and accessible."""
        if not self._api_key:
            return False

        # TODO: Implement actual health check with anthropic package
        # try:
        #     import anthropic
        #     client = anthropic.AsyncAnthropic(api_key=self._api_key)
        #     # Make a minimal request to check connectivity
        #     return True
        # except Exception:
        #     return False

        logger.warning("Anthropic health check not implemented - stub provider")
        return False

    async def enhance(self, context: EnhancementContext) -> EnhancedResult:
        """Enhance the explanation using Anthropic.

        Note: This is a stub that returns the original explanation.
        Full implementation requires the anthropic package.
        """
        logger.warning("Anthropic enhancement not implemented - returning original")

        # TODO: Implement with anthropic package
        # import anthropic
        # client = anthropic.AsyncAnthropic(api_key=self._api_key)
        # message = await client.messages.create(
        #     model=self._model,
        #     max_tokens=500,
        #     system=ENHANCEMENT_SYSTEM_PROMPT,
        #     messages=[
        #         {"role": "user", "content": format_enhancement_prompt(...)}
        #     ]
        # )
        # enhanced = message.content[0].text

        return EnhancedResult(
            enhanced_explanation=context.explanation,
            follow_up_questions=[],
            from_cache=False
        )
