"""
Patient-related data models.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class PatientContext(BaseModel):
    """Patient demographic and medical context."""
    age: int = Field(..., ge=18, description="Patient age, must be 18 or older")
    sex: str = Field(..., pattern="^(male|female|other)$", description="Patient sex")
    comorbidities: list[str] = Field(
        default_factory=list,
        description="List of comorbidities (e.g., 'diabetes', 'hypertension')"
    )
    medications: list[str] = Field(
        default_factory=list,
        description="List of current medications"
    )


class SymptomInput(BaseModel):
    """Symptom information from user input."""
    chief_complaint: str = Field(
        ...,
        min_length=1,
        description="Primary complaint (e.g., 'chest_pain')"
    )
    symptoms: dict[str, Any] = Field(
        default_factory=dict,
        description="Symptom flags (e.g., {'chest_pressure': True})"
    )
    duration_hours: Optional[float] = Field(
        None,
        ge=0,
        description="How long symptoms have been present"
    )
    severity: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Symptom severity on 1-10 scale"
    )


class LabInput(BaseModel):
    """Lab test result input."""
    test_code: str = Field(..., min_length=1, description="Lab test code (e.g., 'troponin')")
    value: float = Field(..., description="Numeric test result value")
    unit: str = Field(..., min_length=1, description="Unit of measurement")
    reference_low: Optional[float] = Field(None, description="Lab's reference range lower bound")
    reference_high: Optional[float] = Field(None, description="Lab's reference range upper bound")
    lab_flag: Optional[str] = Field(
        None,
        description="Lab-provided flag (e.g., 'H', 'L', 'HH', 'LL')"
    )
