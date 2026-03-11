"""
Tests for the rule evaluator.
"""

import pytest
from app.models.enums import ConditionOperator, JoinType, Disposition, Priority
from app.models.rules import Condition, DecisionRule
from app.engine import RuleEvaluator


class TestRuleEvaluator:
    """Tests for RuleEvaluator."""

    def test_all_join_all_conditions_match(self, rule_evaluator, sample_context):
        """Test 'all' join when all conditions match."""
        rule = DecisionRule(
            id="test_all_match",
            label="Test All Match",
            join=JoinType.ALL,
            conditions=[
                Condition(field="symptoms.chest_pressure", operator=ConditionOperator.IS_TRUE, value=True),
                Condition(field="symptoms.shortness_of_breath", operator=ConditionOperator.IS_TRUE, value=True),
            ],
            disposition=Disposition.ER_NOW,
            priority=Priority.HIGH,
            reason_codes=[],
            explanation_keys=[],
            safety_net_keys=[],
        )
        assert rule_evaluator.evaluate(rule, sample_context) is True

    def test_all_join_some_conditions_match(self, rule_evaluator, sample_context):
        """Test 'all' join when some conditions don't match."""
        rule = DecisionRule(
            id="test_partial",
            label="Test Partial",
            join=JoinType.ALL,
            conditions=[
                Condition(field="symptoms.chest_pressure", operator=ConditionOperator.IS_TRUE, value=True),
                Condition(field="symptoms.sweating", operator=ConditionOperator.IS_TRUE, value=True),  # False in context
            ],
            disposition=Disposition.ER_NOW,
            priority=Priority.HIGH,
            reason_codes=[],
            explanation_keys=[],
            safety_net_keys=[],
        )
        assert rule_evaluator.evaluate(rule, sample_context) is False

    def test_any_join_one_matches(self, rule_evaluator, sample_context):
        """Test 'any' join when at least one condition matches."""
        rule = DecisionRule(
            id="test_any_match",
            label="Test Any Match",
            join=JoinType.ANY,
            conditions=[
                Condition(field="symptoms.chest_pressure", operator=ConditionOperator.IS_TRUE, value=True),
                Condition(field="symptoms.sweating", operator=ConditionOperator.IS_TRUE, value=True),  # False
            ],
            disposition=Disposition.CALL_911,
            priority=Priority.CRITICAL,
            reason_codes=[],
            explanation_keys=[],
            safety_net_keys=[],
        )
        assert rule_evaluator.evaluate(rule, sample_context) is True

    def test_any_join_none_match(self, rule_evaluator, sample_context):
        """Test 'any' join when no conditions match."""
        rule = DecisionRule(
            id="test_none_match",
            label="Test None Match",
            join=JoinType.ANY,
            conditions=[
                Condition(field="symptoms.sweating", operator=ConditionOperator.IS_TRUE, value=True),
                Condition(field="symptoms.fainting", operator=ConditionOperator.IS_TRUE, value=True),
            ],
            disposition=Disposition.CALL_911,
            priority=Priority.CRITICAL,
            reason_codes=[],
            explanation_keys=[],
            safety_net_keys=[],
        )
        assert rule_evaluator.evaluate(rule, sample_context) is False

    def test_evaluate_rules_returns_matching(self, rule_evaluator, sample_context):
        """Test that evaluate_rules returns all matching rules."""
        rules = [
            DecisionRule(
                id="match1",
                label="Match 1",
                join=JoinType.ALL,
                conditions=[
                    Condition(field="symptoms.chest_pressure", operator=ConditionOperator.IS_TRUE, value=True),
                ],
                disposition=Disposition.ER_NOW,
                priority=Priority.HIGH,
                reason_codes=[],
                explanation_keys=[],
                safety_net_keys=[],
            ),
            DecisionRule(
                id="no_match",
                label="No Match",
                join=JoinType.ALL,
                conditions=[
                    Condition(field="symptoms.sweating", operator=ConditionOperator.IS_TRUE, value=True),
                ],
                disposition=Disposition.URGENT_CARE_TODAY,
                priority=Priority.MEDIUM,
                reason_codes=[],
                explanation_keys=[],
                safety_net_keys=[],
            ),
            DecisionRule(
                id="match2",
                label="Match 2",
                join=JoinType.ALL,
                conditions=[
                    Condition(field="patient.age", operator=ConditionOperator.GTE, value=50),
                ],
                disposition=Disposition.PRIMARY_CARE_24_72H,
                priority=Priority.LOW,
                reason_codes=[],
                explanation_keys=[],
                safety_net_keys=[],
            ),
        ]

        matched = rule_evaluator.evaluate_rules(rules, sample_context)
        assert len(matched) == 2
        assert matched[0].id == "match1"
        assert matched[1].id == "match2"

    def test_rule_with_context_conditions(self, rule_evaluator, sample_context):
        """Test rule with additional context conditions."""
        rule = DecisionRule(
            id="test_context",
            label="Test Context",
            join=JoinType.ALL,
            conditions=[
                Condition(field="symptoms.chest_pressure", operator=ConditionOperator.IS_TRUE, value=True),
            ],
            context_conditions=[
                Condition(field="patient.age", operator=ConditionOperator.GTE, value=50),
            ],
            context_join=JoinType.ALL,
            disposition=Disposition.ER_NOW,
            priority=Priority.HIGH,
            reason_codes=[],
            explanation_keys=[],
            safety_net_keys=[],
        )
        assert rule_evaluator.evaluate(rule, sample_context) is True

        # Now with age that doesn't match
        context_young = sample_context.copy()
        context_young["patient"] = {"age": 30, "sex": "male", "comorbidities": []}
        assert rule_evaluator.evaluate(rule, context_young) is False
