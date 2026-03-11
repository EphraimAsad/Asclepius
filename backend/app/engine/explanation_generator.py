"""
Explanation generator for the rules engine.

Generates human-readable explanations and safety warnings from catalog entries.
Optionally enhances explanations using LLM providers.
"""

import logging
from typing import TYPE_CHECKING

from app.models.rules import Rulebook, DecisionRule, CatalogEntry

if TYPE_CHECKING:
    from app.llm import LLMProvider, EnhancementContext

logger = logging.getLogger(__name__)


class ExplanationGenerator:
    """Generates explanations and safety warnings from catalogs."""

    def __init__(self, rulebook: Rulebook):
        self.explanation_catalog = rulebook.explanation_catalog
        self.safety_net_catalog = rulebook.safety_net_catalog
        self.reason_codes = rulebook.reason_codes

    def generate_explanation(
        self,
        matched_rules: list[DecisionRule],
        additional_keys: list[str] | None = None
    ) -> str:
        """
        Generate a combined explanation from matched rules.

        Args:
            matched_rules: Rules that matched during evaluation
            additional_keys: Additional explanation keys to include

        Returns:
            Combined explanation text
        """
        explanation_parts = []
        seen_keys = set()

        # Gather explanation keys from all matched rules
        for rule in matched_rules:
            for key in rule.explanation_keys:
                if key not in seen_keys:
                    seen_keys.add(key)
                    entry = self.explanation_catalog.get(key)
                    if entry:
                        explanation_parts.append(self._format_entry(entry))

        # Add any additional keys
        if additional_keys:
            for key in additional_keys:
                if key not in seen_keys:
                    seen_keys.add(key)
                    entry = self.explanation_catalog.get(key)
                    if entry:
                        explanation_parts.append(self._format_entry(entry))

        if not explanation_parts:
            return "Based on the information provided, we have assessed your situation."

        return "\n\n".join(explanation_parts)

    def generate_safety_warnings(
        self,
        matched_rules: list[DecisionRule],
        additional_keys: list[str] | None = None
    ) -> list[str]:
        """
        Generate safety warnings from matched rules.

        Args:
            matched_rules: Rules that matched during evaluation
            additional_keys: Additional safety net keys to include

        Returns:
            List of safety warning strings
        """
        warnings = []
        seen_keys = set()

        # Gather safety net keys from all matched rules
        for rule in matched_rules:
            for key in rule.safety_net_keys:
                if key not in seen_keys:
                    seen_keys.add(key)
                    warning = self.safety_net_catalog.get(key)
                    if warning:
                        warnings.append(warning)

        # Add any additional keys
        if additional_keys:
            for key in additional_keys:
                if key not in seen_keys:
                    seen_keys.add(key)
                    warning = self.safety_net_catalog.get(key)
                    if warning:
                        warnings.append(warning)

        return warnings

    def collect_reason_codes(
        self,
        matched_rules: list[DecisionRule],
        additional_codes: list[str] | None = None
    ) -> list[str]:
        """
        Collect unique reason codes from matched rules.

        Args:
            matched_rules: Rules that matched during evaluation
            additional_codes: Additional reason codes to include

        Returns:
            List of unique reason codes
        """
        codes = []
        seen = set()

        for rule in matched_rules:
            for code in rule.reason_codes:
                if code not in seen:
                    seen.add(code)
                    codes.append(code)

        if additional_codes:
            for code in additional_codes:
                if code not in seen:
                    seen.add(code)
                    codes.append(code)

        return codes

    def get_reason_description(self, code: str) -> str | None:
        """Get the human-readable description for a reason code."""
        return self.reason_codes.get(code)

    def _format_entry(self, entry: CatalogEntry) -> str:
        """Format a catalog entry for display."""
        return f"**{entry.title}**\n{entry.body}"

    async def enhance_explanation(
        self,
        explanation: str,
        disposition: str,
        matched_rules: list[DecisionRule],
        chief_complaint: str,
        symptoms: dict,
        patient_age: int,
        patient_sex: str,
        reason_codes: list[str],
        llm_provider: "LLMProvider | None"
    ) -> tuple[str, list[str], bool]:
        """
        Optionally enhance the explanation using an LLM provider.

        Args:
            explanation: Original rule-based explanation
            disposition: Triage disposition string
            matched_rules: Rules that matched
            chief_complaint: Primary symptom category
            symptoms: Active symptoms dict
            patient_age: Patient age in years
            patient_sex: Patient sex
            reason_codes: Reason codes for the disposition
            llm_provider: LLM provider instance, or None to skip enhancement

        Returns:
            Tuple of (enhanced_explanation, follow_up_questions, was_enhanced)
        """
        if llm_provider is None:
            return explanation, [], False

        try:
            from app.llm import EnhancementContext

            context = EnhancementContext(
                explanation=explanation,
                disposition=disposition,
                matched_rules=[rule.label for rule in matched_rules],
                chief_complaint=chief_complaint,
                symptoms=symptoms,
                patient_age=patient_age,
                patient_sex=patient_sex,
                reason_codes=reason_codes,
            )

            result = await llm_provider.enhance(context)

            return (
                result.enhanced_explanation,
                result.follow_up_questions,
                True
            )

        except Exception as e:
            logger.error(f"LLM enhancement failed: {e}")
            return explanation, [], False
