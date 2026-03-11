"""
API request models.
"""

from typing import Optional
from pydantic import BaseModel, Field

from .patient import PatientContext, SymptomInput, LabInput


class TriageRequest(BaseModel):
    """Request for triage evaluation."""
    patient: PatientContext
    symptoms: SymptomInput
    labs: list[LabInput] = Field(default_factory=list)
    session_id: str = Field(..., min_length=1, description="Session ID for audit tracking")


class LabInterpretRequest(BaseModel):
    """Request for lab result interpretation."""
    patient: PatientContext
    labs: list[LabInput] = Field(..., min_length=1)
    symptoms: Optional[SymptomInput] = Field(
        None,
        description="Optional symptoms for context"
    )
    session_id: str = Field(..., min_length=1, description="Session ID for audit tracking")
