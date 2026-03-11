"""
Enumerations for the Asclepius triage system.
"""

from enum import Enum


class Disposition(str, Enum):
    """Care disposition levels, ordered from most to least urgent."""
    CALL_911 = "CALL_911"
    ER_NOW = "ER_NOW"
    URGENT_CARE_TODAY = "URGENT_CARE_TODAY"
    PRIMARY_CARE_24_72H = "PRIMARY_CARE_24_72H"
    SELF_CARE = "SELF_CARE"

    @classmethod
    def urgency_order(cls) -> list["Disposition"]:
        """Return dispositions in order of urgency (highest first)."""
        return [
            cls.CALL_911,
            cls.ER_NOW,
            cls.URGENT_CARE_TODAY,
            cls.PRIMARY_CARE_24_72H,
            cls.SELF_CARE,
        ]

    def is_more_urgent_than(self, other: "Disposition") -> bool:
        """Check if this disposition is more urgent than another."""
        order = self.urgency_order()
        return order.index(self) < order.index(other)


class Priority(str, Enum):
    """Rule priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LabStatus(str, Enum):
    """Lab result status categories."""
    CRITICAL_LOW = "CRITICAL_LOW"
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL_HIGH = "CRITICAL_HIGH"


class ConditionOperator(str, Enum):
    """Operators for condition evaluation."""
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    EXISTS = "exists"
    NOT_EXISTS = "not_exists"
    BETWEEN = "between"
    IS_TRUE = "is_true"
    IS_FALSE = "is_false"


class RiskModifierEffect(str, Enum):
    """Types of effects risk modifiers can apply."""
    ESCALATE_DISPOSITION_BY_ONE_LEVEL = "escalate_disposition_by_one_level"
    FORCE_MINIMUM_DISPOSITION = "force_minimum_disposition"
    APPEND_REASON_CODE = "append_reason_code"
    APPEND_EXPLANATION_KEY = "append_explanation_key"


class JoinType(str, Enum):
    """How to combine multiple conditions."""
    ALL = "all"
    ANY = "any"
