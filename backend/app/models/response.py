"""
API response models.
"""

from typing import Optional
from pydantic import BaseModel, Field

from .enums import Disposition, Priority, LabStatus


class MatchedRule(BaseModel):
    """Information about a matched rule."""
    rule_id: str
    label: str
    disposition: Disposition
    priority: Priority
    reason_codes: list[str]


class TriageResult(BaseModel):
    """Result of triage evaluation."""
    disposition: Disposition = Field(..., description="Recommended level of care")
    priority: Priority = Field(..., description="Urgency priority")
    matched_rule_ids: list[str] = Field(
        default_factory=list,
        description="IDs of all rules that matched (for audit)"
    )
    matched_rules: list[MatchedRule] = Field(
        default_factory=list,
        description="Details of matched rules"
    )
    reason_codes: list[str] = Field(
        default_factory=list,
        description="Reason codes explaining the disposition"
    )
    explanation: str = Field(..., description="Human-readable explanation")
    safety_warnings: list[str] = Field(
        default_factory=list,
        description="Safety-net warnings for the patient"
    )
    derived_lab_statuses: dict[str, LabStatus] = Field(
        default_factory=dict,
        description="Lab status derived from inputs"
    )
    risk_modifiers_applied: list[str] = Field(
        default_factory=list,
        description="Risk modifier IDs that were applied"
    )
    follow_up_questions: list[str] = Field(
        default_factory=list,
        description="Questions patient should be prepared to answer when seeking care"
    )
    llm_enhanced: bool = Field(
        default=False,
        description="Whether the explanation was enhanced by LLM"
    )
    disclaimer: str = Field(
        default="This is not a medical diagnosis. This tool provides educational "
        "information and care navigation guidance only. Always consult with a "
        "healthcare professional for medical advice, diagnosis, or treatment.",
        description="Legal disclaimer"
    )


class LabStatusResult(BaseModel):
    """Status result for a single lab test."""
    test_code: str
    status: LabStatus
    interpretation_title: str
    interpretation_body: str


class LabInterpretResult(BaseModel):
    """Result of lab interpretation."""
    lab_statuses: list[LabStatusResult] = Field(default_factory=list)
    overall_disposition: Optional[Disposition] = Field(
        None,
        description="If labs alone warrant action, the recommended disposition"
    )
    reason_codes: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(
        default_factory=list,
        description="Questions patient should be prepared to answer when seeking care"
    )
    llm_enhanced: bool = Field(
        default=False,
        description="Whether the interpretation was enhanced by LLM"
    )
    disclaimer: str = Field(
        default="This is not a medical diagnosis. Lab interpretation is for "
        "educational purposes only. Always consult with a healthcare "
        "professional to understand your lab results.",
        description="Legal disclaimer"
    )
