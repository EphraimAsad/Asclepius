"""
Triage evaluation endpoint.
"""

import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException

from app.models.request import TriageRequest
from app.models.response import TriageResult
from app.engine import TriageEngine

if TYPE_CHECKING:
    from app.llm import LLMProvider

router = APIRouter()
logger = logging.getLogger(__name__)


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


def get_llm_provider() -> "LLMProvider | None":
    """Dependency to get the LLM provider (optional)."""
    from app.main import app
    return getattr(app.state, "llm_provider", None)


@router.post("/evaluate", response_model=TriageResult)
async def evaluate_triage(
    request: TriageRequest,
    engine: TriageEngine = Depends(get_triage_engine),
    llm_provider: "LLMProvider | None" = Depends(get_llm_provider)
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

    Optionally, if LLM is enabled, the explanation will be enhanced
    and follow-up questions will be generated.

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
        # Step 1-8: Run deterministic rules engine
        result = engine.evaluate(request)

        # Step 9 (optional): Enhance explanation with LLM
        if llm_provider is not None:
            try:
                # Get matched rules for enhancement context
                matched_rules = []
                pathway = engine._select_pathway(request.symptoms.chief_complaint)
                if pathway:
                    for rule in pathway.rules:
                        if rule.id in result.matched_rule_ids:
                            matched_rules.append(rule)

                # Enhance the explanation
                enhanced_explanation, follow_up_questions, was_enhanced = (
                    await engine.explanation_generator.enhance_explanation(
                        explanation=result.explanation,
                        disposition=result.disposition.value,
                        matched_rules=matched_rules,
                        chief_complaint=request.symptoms.chief_complaint,
                        symptoms=request.symptoms.symptoms,
                        patient_age=request.patient.age,
                        patient_sex=request.patient.sex,
                        reason_codes=result.reason_codes,
                        llm_provider=llm_provider,
                    )
                )

                if was_enhanced:
                    result.explanation = enhanced_explanation
                    result.follow_up_questions = follow_up_questions
                    result.llm_enhanced = True

            except Exception as e:
                # Log but don't fail - LLM enhancement is optional
                logger.warning(f"LLM enhancement failed: {e}")

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation error: {str(e)}"
        )
