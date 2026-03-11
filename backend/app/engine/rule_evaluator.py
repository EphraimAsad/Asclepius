"""
Rule evaluator for the rules engine.

Evaluates decision rules against a context using the condition evaluator.
"""

from typing import Any

from app.models.enums import JoinType
from app.models.rules import DecisionRule, Condition
from .condition_evaluator import ConditionEvaluator


class RuleEvaluator:
    """Evaluates decision rules against a context."""

    def __init__(self, condition_evaluator: ConditionEvaluator | None = None):
        self.condition_evaluator = condition_evaluator or ConditionEvaluator()

    def evaluate(self, rule: DecisionRule, context: dict[str, Any]) -> bool:
        """
        Evaluate a decision rule against the context.

        Args:
            rule: The decision rule to evaluate
            context: Dictionary containing patient data, symptoms, labs, etc.

        Returns:
            True if the rule matches, False otherwise
        """
        # First check required_context if present
        if rule.required_context:
            if not self._evaluate_conditions(rule.required_context, JoinType.ALL, context):
                return False

        # Evaluate main conditions
        main_result = self._evaluate_conditions(rule.conditions, rule.join, context)

        if not main_result:
            return False

        # If context_conditions exist, evaluate them
        if rule.context_conditions:
            context_join = rule.context_join or JoinType.ALL
            context_result = self._evaluate_conditions(
                rule.context_conditions, context_join, context
            )
            return context_result

        return True

    def _evaluate_conditions(
        self,
        conditions: list[Condition],
        join: JoinType,
        context: dict[str, Any]
    ) -> bool:
        """
        Evaluate a list of conditions with a join type.

        Args:
            conditions: List of conditions to evaluate
            join: How to combine results ('all' or 'any')
            context: The evaluation context

        Returns:
            True if conditions match according to join logic
        """
        if not conditions:
            return True

        results = [
            self.condition_evaluator.evaluate(condition, context)
            for condition in conditions
        ]

        if join == JoinType.ALL:
            return all(results)
        elif join == JoinType.ANY:
            return any(results)
        else:
            raise ValueError(f"Unknown join type: {join}")

    def evaluate_rules(
        self,
        rules: list[DecisionRule],
        context: dict[str, Any]
    ) -> list[DecisionRule]:
        """
        Evaluate multiple rules and return those that match.

        Args:
            rules: List of rules to evaluate
            context: The evaluation context

        Returns:
            List of rules that matched
        """
        return [rule for rule in rules if self.evaluate(rule, context)]
