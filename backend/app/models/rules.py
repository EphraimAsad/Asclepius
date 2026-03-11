"""
Rule-related data models matching the rulebook JSON schema.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field

from .enums import Disposition, Priority, ConditionOperator, JoinType, RiskModifierEffect


class Condition(BaseModel):
    """A single condition to evaluate."""
    field: str = Field(..., min_length=1, description="Dotted path to field (e.g., 'symptoms.chest_pressure')")
    operator: ConditionOperator
    value: Optional[Any] = Field(None, description="Value to compare against")
    value_min: Optional[float | int | str] = Field(None, description="Min value for 'between' operator")
    value_max: Optional[float | int | str] = Field(None, description="Max value for 'between' operator")


class DecisionRule(BaseModel):
    """A rule that evaluates conditions and produces a disposition."""
    id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    join: JoinType = Field(..., description="How to combine conditions ('all' or 'any')")
    conditions: list[Condition] = Field(..., min_length=1)
    required_context: Optional[list[Condition]] = Field(None)
    context_conditions: Optional[list[Condition]] = Field(None)
    context_join: Optional[JoinType] = Field(None)
    disposition: Disposition
    priority: Priority
    reason_codes: list[str] = Field(default_factory=list)
    explanation_keys: list[str] = Field(default_factory=list)
    safety_net_keys: list[str] = Field(default_factory=list)


class RiskModifierEffectModel(BaseModel):
    """Effect to apply when a risk modifier matches."""
    type: RiskModifierEffect
    max_disposition: Optional[Disposition] = None
    minimum_disposition: Optional[Disposition] = None
    reason_code: Optional[str] = None
    explanation_key: Optional[str] = None


class RiskModifier(BaseModel):
    """A modifier that can escalate disposition based on risk factors."""
    id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    join: JoinType
    conditions: list[Condition] = Field(..., min_length=1)
    effect: RiskModifierEffectModel
    reason_codes: list[str] = Field(default_factory=list)


class TriagePathway(BaseModel):
    """A symptom pathway with associated rules."""
    pathway_id: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)
    chief_complaint_aliases: list[str] = Field(default_factory=list)
    intake_fields: list[str] = Field(default_factory=list)
    rules: list[DecisionRule] = Field(default_factory=list)


class StatusThreshold(BaseModel):
    """Threshold configuration for lab status determination."""
    use_reference_low: Optional[bool] = None
    use_reference_high: Optional[bool] = None
    absolute_threshold_by_unit: Optional[dict[str, float | int]] = None
    multiplier_of_reference_high: Optional[float | int] = None
    multiplier_of_reference_low: Optional[float | int] = None


class StatusLogic(BaseModel):
    """Logic for determining lab status."""
    method: str = Field(..., description="Method for status determination")
    critical_low: Optional[StatusThreshold] = None
    low: Optional[StatusThreshold] = None
    high: Optional[StatusThreshold] = None
    critical_high: Optional[StatusThreshold] = None


class LabInterpretation(BaseModel):
    """Interpretation keys for each lab status."""
    critical_low_key: Optional[str] = None
    low_key: Optional[str] = None
    normal_key: Optional[str] = None
    high_key: Optional[str] = None
    critical_high_key: Optional[str] = None


class LabTest(BaseModel):
    """Definition of a lab test with interpretation rules."""
    test_code: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    description_key: str = Field(..., min_length=1)
    units: list[str] = Field(default_factory=list)
    range_strategy: str
    status_logic: StatusLogic
    interpretation: LabInterpretation
    urgency_rules: list[DecisionRule] = Field(default_factory=list)


class CatalogEntry(BaseModel):
    """An explanation catalog entry."""
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class EngineMetadata(BaseModel):
    """Metadata about the rules engine."""
    name: str
    jurisdiction: str
    intended_use: str
    not_for: list[str]


class Rulebook(BaseModel):
    """The complete compiled rulebook."""
    schema_version: str
    engine_metadata: EngineMetadata
    global_emergency_rules: list[DecisionRule] = Field(default_factory=list)
    risk_modifiers: list[RiskModifier] = Field(default_factory=list)
    triage_pathways: list[TriagePathway] = Field(default_factory=list)
    lab_tests: list[LabTest] = Field(default_factory=list)
    symptom_lab_escalation_rules: list[DecisionRule] = Field(default_factory=list)
    explanation_catalog: dict[str, CatalogEntry] = Field(default_factory=dict)
    safety_net_catalog: dict[str, str] = Field(default_factory=dict)
    reason_codes: dict[str, str] = Field(default_factory=dict)
