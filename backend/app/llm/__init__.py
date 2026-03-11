"""
LLM integration for explanation enhancement.

This module provides a provider abstraction layer for LLM-based
enhancement of triage explanations. The LLM is used ONLY for:
- Making explanations clearer and more empathetic
- Generating follow-up questions for patients

The LLM is NEVER used for triage decisions.
"""

from .base import EnhancementContext, EnhancedResult, LLMProvider
from .cache import LLMCache, get_cache, reset_cache
from .factory import get_llm_provider

__all__ = [
    "EnhancementContext",
    "EnhancedResult",
    "LLMProvider",
    "LLMCache",
    "get_cache",
    "reset_cache",
    "get_llm_provider",
]
