"""
Factory for creating LLM providers.
"""

import logging
from typing import TYPE_CHECKING

from .base import LLMProvider
from .providers import OllamaProvider, OpenAIProvider, AnthropicProvider

if TYPE_CHECKING:
    from app.config import Settings

logger = logging.getLogger(__name__)


def get_llm_provider(settings: "Settings") -> LLMProvider | None:
    """Get the configured LLM provider.

    Args:
        settings: Application settings

    Returns:
        Configured LLMProvider instance, or None if LLM is disabled
    """
    if not settings.llm_enabled:
        logger.info("LLM enhancement is disabled")
        return None

    provider_name = settings.llm_provider.lower()

    if provider_name == "ollama":
        logger.info(f"Using Ollama provider with model {settings.llm_model}")
        return OllamaProvider(settings)

    elif provider_name == "openai":
        logger.info(f"Using OpenAI provider with model {settings.llm_model}")
        return OpenAIProvider(settings)

    elif provider_name == "anthropic":
        logger.info(f"Using Anthropic provider with model {settings.llm_model}")
        return AnthropicProvider(settings)

    else:
        logger.error(f"Unknown LLM provider: {provider_name}")
        return None
