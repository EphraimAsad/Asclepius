"""
Explanation generator for the rules engine.

Generates human-readable explanations and safety warnings from catalog entries.
"""

from app.models.rules import Rulebook, DecisionRule, CatalogEntry


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
