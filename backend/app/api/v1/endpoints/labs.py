"""
Lab interpretation endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.models.request import LabInterpretRequest
from app.models.response import LabInterpretResult, LabStatusResult
from app.models.enums import LabStatus
from app.engine import LabStatusDeriver, RulebookLoader
from app.models.rules import Rulebook

router = APIRouter()


def get_rulebook() -> Rulebook:
    """Get the loaded rulebook from app state."""
    from app.main import app
    if not hasattr(app.state, "rulebook"):
        raise HTTPException(
            status_code=503,
            detail="Rulebook not initialized"
        )
    return app.state.rulebook


@router.post("/interpret", response_model=LabInterpretResult)
async def interpret_labs(
    request: LabInterpretRequest,
    rulebook: Rulebook = Depends(get_rulebook)
):
    """
    Interpret lab results and provide explanations.

    This endpoint analyzes provided lab results against reference ranges
    and lab test definitions to determine status (normal, high, low, etc.)
    and provide educational explanations.

    **Important**: This is NOT a medical diagnosis. Lab interpretation
    is for educational purposes only. Always consult with a healthcare
    professional to understand your lab results.
    """
    # Validate age
    if request.patient.age < 18:
        raise HTTPException(
            status_code=400,
            detail="This tool is for adults 18 and older only"
        )

    deriver = LabStatusDeriver()
    lab_statuses = deriver.derive_all_statuses(request.labs, rulebook.lab_tests)

    # Build lookup for lab tests
    test_lookup = {test.test_code: test for test in rulebook.lab_tests}

    results = []
    safety_warnings = []
    reason_codes = []

    for lab in request.labs:
        test_code = lab.test_code
        status = lab_statuses.get(test_code, LabStatus.NORMAL)

        # Get interpretation text
        if test_code in test_lookup:
            lab_test = test_lookup[test_code]
            interp = lab_test.interpretation

            # Select the right interpretation key based on status
            interp_key = None
            match status:
                case LabStatus.CRITICAL_LOW:
                    interp_key = interp.critical_low_key
                case LabStatus.LOW:
                    interp_key = interp.low_key
                case LabStatus.NORMAL:
                    interp_key = interp.normal_key
                case LabStatus.HIGH:
                    interp_key = interp.high_key
                case LabStatus.CRITICAL_HIGH:
                    interp_key = interp.critical_high_key

            # Look up explanation
            if interp_key and interp_key in rulebook.explanation_catalog:
                entry = rulebook.explanation_catalog[interp_key]
                results.append(LabStatusResult(
                    test_code=test_code,
                    status=status,
                    interpretation_title=entry.title,
                    interpretation_body=entry.body,
                ))
            else:
                results.append(LabStatusResult(
                    test_code=test_code,
                    status=status,
                    interpretation_title=f"{lab_test.display_name} - {status.value}",
                    interpretation_body=f"Your {lab_test.display_name} level is {status.value.lower().replace('_', ' ')}.",
                ))

            # Check for critical values and add warnings
            if status in [LabStatus.CRITICAL_HIGH, LabStatus.CRITICAL_LOW]:
                safety_warnings.append(
                    f"Your {lab_test.display_name} level is critically abnormal. "
                    "Please consult a healthcare provider promptly."
                )
                reason_codes.append(f"CRITICAL_{test_code.upper()}")

    return LabInterpretResult(
        lab_statuses=results,
        reason_codes=reason_codes,
        safety_warnings=safety_warnings,
    )
