"""
Disposition selector for the rules engine.

Selects the highest urgency disposition from matched rules and applies
risk modifier effects.
"""

from app.models.enums import Disposition, RiskModifierEffect
from app.models.rules import DecisionRule, RiskModifier


class DispositionSelector:
    """Selects the final disposition based on matched rules and modifiers."""

    # Disposition order from most urgent to least
    DISPOSITION_ORDER = [
        Disposition.CALL_911,
        Disposition.ER_NOW,
        Disposition.URGENT_CARE_TODAY,
        Disposition.PRIMARY_CARE_24_72H,
        Disposition.SELF_CARE,
    ]

    def select_highest(
        self,
        matched_rules: list[DecisionRule],
        default: Disposition = Disposition.SELF_CARE
    ) -> Disposition:
        """
        Select the highest urgency disposition from matched rules.

        Args:
            matched_rules: List of rules that matched
            default: Default disposition if no rules matched

        Returns:
            The most urgent disposition
        """
        if not matched_rules:
            return default

        dispositions = [rule.disposition for rule in matched_rules]
        return self._get_most_urgent(dispositions)

    def apply_modifiers(
        self,
        base_disposition: Disposition,
        matched_modifiers: list[RiskModifier]
    ) -> tuple[Disposition, list[str]]:
        """
        Apply risk modifiers to escalate the disposition.

        Args:
            base_disposition: The starting disposition
            matched_modifiers: List of risk modifiers that matched

        Returns:
            Tuple of (final_disposition, list of applied modifier IDs)
        """
        current = base_disposition
        applied = []

        for modifier in matched_modifiers:
            effect = modifier.effect

            match effect.type:
                case RiskModifierEffect.ESCALATE_DISPOSITION_BY_ONE_LEVEL:
                    new_disposition = self._escalate_by_one(current)
                    # Respect max_disposition limit
                    if effect.max_disposition:
                        if self._is_more_urgent(new_disposition, effect.max_disposition):
                            new_disposition = effect.max_disposition
                    if new_disposition != current:
                        current = new_disposition
                        applied.append(modifier.id)

                case RiskModifierEffect.FORCE_MINIMUM_DISPOSITION:
                    if effect.minimum_disposition:
                        if self._is_more_urgent(effect.minimum_disposition, current):
                            current = effect.minimum_disposition
                            applied.append(modifier.id)

                case RiskModifierEffect.APPEND_REASON_CODE:
                    # This effect doesn't change disposition
                    applied.append(modifier.id)

                case RiskModifierEffect.APPEND_EXPLANATION_KEY:
                    # This effect doesn't change disposition
                    applied.append(modifier.id)

        return current, applied

    def _get_most_urgent(self, dispositions: list[Disposition]) -> Disposition:
        """Get the most urgent disposition from a list."""
        if not dispositions:
            return Disposition.SELF_CARE

        best_index = len(self.DISPOSITION_ORDER)
        for d in dispositions:
            try:
                index = self.DISPOSITION_ORDER.index(d)
                if index < best_index:
                    best_index = index
            except ValueError:
                continue

        return self.DISPOSITION_ORDER[best_index] if best_index < len(self.DISPOSITION_ORDER) else Disposition.SELF_CARE

    def _escalate_by_one(self, disposition: Disposition) -> Disposition:
        """Escalate a disposition by one level."""
        try:
            current_index = self.DISPOSITION_ORDER.index(disposition)
            if current_index > 0:
                return self.DISPOSITION_ORDER[current_index - 1]
            return disposition
        except ValueError:
            return disposition

    def _is_more_urgent(self, a: Disposition, b: Disposition) -> bool:
        """Check if disposition a is more urgent than b."""
        try:
            index_a = self.DISPOSITION_ORDER.index(a)
            index_b = self.DISPOSITION_ORDER.index(b)
            return index_a < index_b
        except ValueError:
            return False
