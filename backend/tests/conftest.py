"""
Pytest configuration and fixtures.
"""

import pytest
from app.models.enums import ConditionOperator, JoinType, Disposition, Priority
from app.models.rules import Condition, DecisionRule
from app.engine import ConditionEvaluator, RuleEvaluator


@pytest.fixture
def condition_evaluator():
    """Provide a ConditionEvaluator instance."""
    return ConditionEvaluator()


@pytest.fixture
def rule_evaluator(condition_evaluator):
    """Provide a RuleEvaluator instance."""
    return RuleEvaluator(condition_evaluator)


@pytest.fixture
def sample_context():
    """Provide a sample evaluation context."""
    return {
        "patient": {
            "age": 55,
            "sex": "male",
            "comorbidities": ["diabetes", "hypertension"],
            "medications": ["metformin", "lisinopril"],
        },
        "symptoms": {
            "chest_pressure": True,
            "shortness_of_breath": True,
            "sweating": False,
        },
        "chief_complaint": "chest_pain",
        "duration_hours": 2.5,
        "severity": 7,
        "derived": {
            "lab_status": {
                "troponin": "HIGH",
            }
        },
    }


@pytest.fixture
def sample_rule():
    """Provide a sample decision rule."""
    return DecisionRule(
        id="test_rule",
        label="Test Rule",
        join=JoinType.ALL,
        conditions=[
            Condition(
                field="symptoms.chest_pressure",
                operator=ConditionOperator.IS_TRUE,
                value=True
            ),
            Condition(
                field="symptoms.shortness_of_breath",
                operator=ConditionOperator.IS_TRUE,
                value=True
            ),
        ],
        disposition=Disposition.ER_NOW,
        priority=Priority.HIGH,
        reason_codes=["TEST_REASON"],
        explanation_keys=["test_explanation"],
        safety_net_keys=["test_safety"],
    )
