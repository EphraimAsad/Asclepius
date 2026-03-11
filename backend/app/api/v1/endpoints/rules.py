"""
Rules validation endpoint.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.engine import RulebookLoader
from app.config import settings

router = APIRouter()


class ValidationResult(BaseModel):
    """Result of rulebook validation."""
    valid: bool
    issues: list[str]
    stats: dict[str, int] | None = None


@router.post("/validate", response_model=ValidationResult)
async def validate_rulebook():
    """
    Validate the compiled rulebook.

    Checks:
    - JSON syntax validity
    - JSON Schema compliance
    - Pydantic model validation
    - Reference integrity (all keys exist in catalogs)

    Returns validation status and any issues found.
    """
    loader = RulebookLoader(
        rulebook_path=settings.rulebook_path,
        schema_path=settings.schema_path,
    )

    issues = loader.validate_only()

    if issues:
        return ValidationResult(
            valid=False,
            issues=issues,
            stats=None,
        )

    # If valid, load and return stats
    try:
        rulebook = loader.load()
        stats = {
            "global_emergency_rules": len(rulebook.global_emergency_rules),
            "risk_modifiers": len(rulebook.risk_modifiers),
            "triage_pathways": len(rulebook.triage_pathways),
            "lab_tests": len(rulebook.lab_tests),
            "symptom_lab_escalation_rules": len(rulebook.symptom_lab_escalation_rules),
            "explanation_catalog_entries": len(rulebook.explanation_catalog),
            "safety_net_catalog_entries": len(rulebook.safety_net_catalog),
            "reason_codes": len(rulebook.reason_codes),
        }
        return ValidationResult(
            valid=True,
            issues=[],
            stats=stats,
        )
    except Exception as e:
        return ValidationResult(
            valid=False,
            issues=[str(e)],
            stats=None,
        )
