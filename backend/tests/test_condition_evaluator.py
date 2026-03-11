"""
Tests for the condition evaluator.
"""

import pytest
from app.models.enums import ConditionOperator
from app.models.rules import Condition
from app.engine import ConditionEvaluator


class TestConditionEvaluator:
    """Tests for ConditionEvaluator."""

    def test_eq_operator(self, condition_evaluator):
        """Test equality operator."""
        condition = Condition(
            field="patient.age",
            operator=ConditionOperator.EQ,
            value=45
        )
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 45}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 44}}) is False

    def test_neq_operator(self, condition_evaluator):
        """Test not equal operator."""
        condition = Condition(
            field="patient.sex",
            operator=ConditionOperator.NEQ,
            value="female"
        )
        assert condition_evaluator.evaluate(condition, {"patient": {"sex": "male"}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"sex": "female"}}) is False

    def test_gt_operator(self, condition_evaluator):
        """Test greater than operator."""
        condition = Condition(
            field="patient.age",
            operator=ConditionOperator.GT,
            value=65
        )
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 70}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 65}}) is False
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 60}}) is False

    def test_gte_operator(self, condition_evaluator):
        """Test greater than or equal operator."""
        condition = Condition(
            field="patient.age",
            operator=ConditionOperator.GTE,
            value=65
        )
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 70}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 65}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 60}}) is False

    def test_lt_operator(self, condition_evaluator):
        """Test less than operator."""
        condition = Condition(
            field="severity",
            operator=ConditionOperator.LT,
            value=5
        )
        assert condition_evaluator.evaluate(condition, {"severity": 3}) is True
        assert condition_evaluator.evaluate(condition, {"severity": 5}) is False

    def test_lte_operator(self, condition_evaluator):
        """Test less than or equal operator."""
        condition = Condition(
            field="severity",
            operator=ConditionOperator.LTE,
            value=5
        )
        assert condition_evaluator.evaluate(condition, {"severity": 3}) is True
        assert condition_evaluator.evaluate(condition, {"severity": 5}) is True
        assert condition_evaluator.evaluate(condition, {"severity": 7}) is False

    def test_in_operator(self, condition_evaluator):
        """Test 'in' operator."""
        condition = Condition(
            field="derived.lab_status.troponin",
            operator=ConditionOperator.IN,
            value=["HIGH", "CRITICAL_HIGH"]
        )
        context = {"derived": {"lab_status": {"troponin": "HIGH"}}}
        assert condition_evaluator.evaluate(condition, context) is True

        context = {"derived": {"lab_status": {"troponin": "NORMAL"}}}
        assert condition_evaluator.evaluate(condition, context) is False

    def test_not_in_operator(self, condition_evaluator):
        """Test 'not_in' operator."""
        condition = Condition(
            field="patient.sex",
            operator=ConditionOperator.NOT_IN,
            value=["unknown", "unspecified"]
        )
        assert condition_evaluator.evaluate(condition, {"patient": {"sex": "male"}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"sex": "unknown"}}) is False

    def test_contains_operator_list(self, condition_evaluator):
        """Test 'contains' operator with list."""
        condition = Condition(
            field="patient.comorbidities",
            operator=ConditionOperator.CONTAINS,
            value="diabetes"
        )
        context = {"patient": {"comorbidities": ["diabetes", "hypertension"]}}
        assert condition_evaluator.evaluate(condition, context) is True

        context = {"patient": {"comorbidities": ["hypertension"]}}
        assert condition_evaluator.evaluate(condition, context) is False

    def test_contains_operator_string(self, condition_evaluator):
        """Test 'contains' operator with string."""
        condition = Condition(
            field="chief_complaint",
            operator=ConditionOperator.CONTAINS,
            value="pain"
        )
        assert condition_evaluator.evaluate(condition, {"chief_complaint": "chest_pain"}) is True
        assert condition_evaluator.evaluate(condition, {"chief_complaint": "headache"}) is False

    def test_exists_operator(self, condition_evaluator):
        """Test 'exists' operator."""
        condition = Condition(
            field="symptoms.chest_pressure",
            operator=ConditionOperator.EXISTS,
            value=None
        )
        context = {"symptoms": {"chest_pressure": True}}
        assert condition_evaluator.evaluate(condition, context) is True

        context = {"symptoms": {}}
        assert condition_evaluator.evaluate(condition, context) is False

    def test_not_exists_operator(self, condition_evaluator):
        """Test 'not_exists' operator."""
        condition = Condition(
            field="symptoms.fainting",
            operator=ConditionOperator.NOT_EXISTS,
            value=None
        )
        context = {"symptoms": {}}
        assert condition_evaluator.evaluate(condition, context) is True

        context = {"symptoms": {"fainting": True}}
        assert condition_evaluator.evaluate(condition, context) is False

    def test_between_operator(self, condition_evaluator):
        """Test 'between' operator."""
        condition = Condition(
            field="patient.age",
            operator=ConditionOperator.BETWEEN,
            value_min=40,
            value_max=60
        )
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 50}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 40}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 60}}) is True
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 39}}) is False
        assert condition_evaluator.evaluate(condition, {"patient": {"age": 61}}) is False

    def test_is_true_operator(self, condition_evaluator):
        """Test 'is_true' operator."""
        condition = Condition(
            field="symptoms.chest_pressure",
            operator=ConditionOperator.IS_TRUE,
            value=True
        )
        context = {"symptoms": {"chest_pressure": True}}
        assert condition_evaluator.evaluate(condition, context) is True

        context = {"symptoms": {"chest_pressure": False}}
        assert condition_evaluator.evaluate(condition, context) is False

    def test_is_false_operator(self, condition_evaluator):
        """Test 'is_false' operator."""
        condition = Condition(
            field="symptoms.sweating",
            operator=ConditionOperator.IS_FALSE,
            value=False
        )
        context = {"symptoms": {"sweating": False}}
        assert condition_evaluator.evaluate(condition, context) is True

        context = {"symptoms": {"sweating": True}}
        assert condition_evaluator.evaluate(condition, context) is False

    def test_dotted_field_resolution(self, condition_evaluator):
        """Test resolution of deeply nested fields."""
        condition = Condition(
            field="derived.lab_status.troponin",
            operator=ConditionOperator.EQ,
            value="HIGH"
        )
        context = {"derived": {"lab_status": {"troponin": "HIGH"}}}
        assert condition_evaluator.evaluate(condition, context) is True

    def test_missing_field_returns_none(self, condition_evaluator):
        """Test that missing fields don't raise errors."""
        condition = Condition(
            field="nonexistent.field",
            operator=ConditionOperator.EQ,
            value="something"
        )
        assert condition_evaluator.evaluate(condition, {}) is False

    def test_null_value_handling(self, condition_evaluator):
        """Test handling of None values."""
        condition = Condition(
            field="patient.age",
            operator=ConditionOperator.GT,
            value=18
        )
        context = {"patient": {"age": None}}
        assert condition_evaluator.evaluate(condition, context) is False
