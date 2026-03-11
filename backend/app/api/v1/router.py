"""
API v1 router aggregating all endpoints.
"""

from fastapi import APIRouter

from .endpoints import health, triage, labs, rules

router = APIRouter()

router.include_router(health.router, tags=["Health"])
router.include_router(triage.router, prefix="/triage", tags=["Triage"])
router.include_router(labs.router, prefix="/labs", tags=["Labs"])
router.include_router(rules.router, prefix="/rules", tags=["Rules"])
