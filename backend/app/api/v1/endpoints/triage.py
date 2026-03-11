"""
Triage evaluation endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.models.request import TriageRequest
from app.models.response import TriageResult
from app.engine import TriageEngine

router = APIRouter()


def get_triage_engine() -> TriageEngine:
    """
    Dependency to get the triage engine.

    The engine is initialized at app startup and stored in app.state.
    """
    from app.main import app
    if not hasattr(app.state, "triage_engine"):
        raise HTTPException(
            status_code=503,
            detail="Triage engine not initialized"
        )
    return app.state.triage_engine


@router.post("/evaluate", response_model=TriageResult)
async def evaluate_triage(
    request: TriageRequest,
    engine: TriageEngine = Depends(get_triage_engine)
):
    """
    Evaluate symptoms and return triage disposition.

    This endpoint evaluates the provided patient information, symptoms,
    and optional lab results against the rules engine to determine the
    recommended level of care.

    The evaluation follows a deterministic 8-step process:
    1. Derive lab statuses from results
    2. Run global emergency rules (highest priority)
    3. Evaluate triage pathway rules
    4. Apply risk modifiers
    5. Run lab urgency rules
    6. Apply symptom-lab escalation rules
    7. Select highest urgency disposition
    8. Assemble structured output

    **Important**: This is NOT a medical diagnosis. This tool provides
    educational information and care navigation guidance only.
    """
    # Validate age (must be 18+)
    if request.patient.age < 18:
        raise HTTPException(
            status_code=400,
            detail="This tool is for adults 18 and older only"
        )

    try:
        result = engine.evaluate(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation error: {str(e)}"
        )
