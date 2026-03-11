"""
Condition evaluator for the rules engine.

Evaluates individual conditions against a context dictionary.
"""

from typing import Any

from app.models.enums import ConditionOperator
from app.models.rules import Condition


class ConditionEvaluator:
    """Evaluates conditions against a context."""

    def evaluate(self, condition: Condition, context: dict[str, Any]) -> bool:
        """
        Evaluate a single condition against the context.

        Args:
            condition: The condition to evaluate
            context: Dictionary containing patient data, symptoms, labs, etc.

        Returns:
            True if the condition matches, False otherwise
        """
        field_value = self._resolve_field(condition.field, context)
        operator = condition.operator

        match operator:
            case ConditionOperator.EQ:
                return field_value == condition.value
            case ConditionOperator.NEQ:
                return field_value != condition.value
            case ConditionOperator.GT:
                return self._safe_compare(field_value, condition.value, lambda a, b: a > b)
            case ConditionOperator.GTE:
                return self._safe_compare(field_value, condition.value, lambda a, b: a >= b)
            case ConditionOperator.LT:
                return self._safe_compare(field_value, condition.value, lambda a, b: a < b)
            case ConditionOperator.LTE:
                return self._safe_compare(field_value, condition.value, lambda a, b: a <= b)
            case ConditionOperator.IN:
                return field_value in (condition.value or [])
            case ConditionOperator.NOT_IN:
                return field_value not in (condition.value or [])
            case ConditionOperator.CONTAINS:
                return self._check_contains(field_value, condition.value)
            case ConditionOperator.NOT_CONTAINS:
                return not self._check_contains(field_value, condition.value)
            case ConditionOperator.EXISTS:
                return field_value is not None
            case ConditionOperator.NOT_EXISTS:
                return field_value is None
            case ConditionOperator.BETWEEN:
                return self._check_between(
                    field_value, condition.value_min, condition.value_max
                )
            case ConditionOperator.IS_TRUE:
                return field_value is True
            case ConditionOperator.IS_FALSE:
                return field_value is False
            case _:
                raise ValueError(f"Unknown operator: {operator}")

    def _resolve_field(self, field_path: str, context: dict[str, Any]) -> Any:
        """
        Resolve a dotted field path to its value in the context.

        Examples:
            'symptoms.chest_pressure' -> context['symptoms']['chest_pressure']
            'patient.age' -> context['patient']['age']
            'derived.lab_status.troponin' -> context['derived']['lab_status']['troponin']
        """
        parts = field_path.split(".")
        value = context

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                return None

            if value is None:
                return None

        return value

    def _safe_compare(
        self,
        field_value: Any,
        compare_value: Any,
        comparator: callable
    ) -> bool:
        """Safely compare values, returning False if comparison is invalid."""
        if field_value is None or compare_value is None:
            return False
        try:
            return comparator(field_value, compare_value)
        except TypeError:
            return False

    def _check_contains(self, field_value: Any, search_value: Any) -> bool:
        """Check if field_value contains search_value."""
        if field_value is None:
            return False
        if isinstance(field_value, str):
            return str(search_value) in field_value
        if isinstance(field_value, (list, tuple, set)):
            return search_value in field_value
        return False

    def _check_between(
        self,
        field_value: Any,
        value_min: Any,
        value_max: Any
    ) -> bool:
        """Check if field_value is between min and max (inclusive)."""
        if field_value is None or value_min is None or value_max is None:
            return False
        try:
            return value_min <= field_value <= value_max
        except TypeError:
            return False
