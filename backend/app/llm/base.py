"""
Base classes for LLM providers.

The LLM integration enhances explanations only - never makes triage decisions.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EnhancementContext:
    """Context for LLM enhancement of triage explanations."""

    explanation: str
    """Original rule-based explanation text."""

    disposition: str
    """Triage disposition (CALL_911, ER_NOW, URGENT_CARE_TODAY, etc.)."""

    matched_rules: list[str] = field(default_factory=list)
    """Labels of rules that matched."""

    chief_complaint: str = ""
    """Primary symptom category (e.g., 'chest_pain')."""

    symptoms: dict[str, Any] = field(default_factory=dict)
    """Active symptoms provided by patient."""

    patient_age: int = 0
    """Patient age in years."""

    patient_sex: str = ""
    """Patient sex (male/female)."""

    reason_codes: list[str] = field(default_factory=list)
    """Reason codes explaining the disposition."""


@dataclass
class EnhancedResult:
    """Result of LLM enhancement."""

    enhanced_explanation: str
    """Enhanced, patient-friendly explanation text."""

    follow_up_questions: list[str] = field(default_factory=list)
    """Questions patient should be prepared to answer when seeking care."""

    from_cache: bool = False
    """Whether this result was served from cache."""


class LLMProvider(ABC):
    """Abstract base class for LLM providers.

    All providers must implement the enhance() method which takes
    an EnhancementContext and returns an EnhancedResult.

    The LLM is used ONLY for:
    - Making explanations clearer and more empathetic
    - Generating follow-up questions for the patient

    The LLM is NEVER used for:
    - Making triage decisions
    - Changing the disposition
    - Diagnosing conditions
    - Prescribing treatments
    """

    @abstractmethod
    async def enhance(self, context: EnhancementContext) -> EnhancedResult:
        """Enhance the explanation using the LLM.

        Args:
            context: The enhancement context with original explanation and metadata

        Returns:
            EnhancedResult with enhanced explanation and follow-up questions

        Note:
            Implementations should handle timeouts gracefully and return
            the original explanation if the LLM fails.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the LLM provider is available.

        Returns:
            True if the provider is healthy and ready to process requests
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of this provider (e.g., 'ollama', 'openai')."""
        pass
