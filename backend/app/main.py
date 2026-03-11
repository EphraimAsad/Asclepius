"""
Asclepius Backend - FastAPI Application

A rules-first medical triage and lab interpretation API.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.router import router as api_v1_router
from app.engine import RulebookLoader, TriageEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Loads and validates the rulebook at startup.
    The application will fail to start if the rulebook is invalid.
    """
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")

    # Load and validate rulebook
    try:
        loader = RulebookLoader(
            rulebook_path=settings.rulebook_path,
            schema_path=settings.schema_path,
        )
        rulebook = loader.load()
        app.state.rulebook = rulebook
        app.state.triage_engine = TriageEngine(rulebook)

        print("Rulebook loaded successfully:")
        print(f"  - Global emergency rules: {len(rulebook.global_emergency_rules)}")
        print(f"  - Risk modifiers: {len(rulebook.risk_modifiers)}")
        print(f"  - Triage pathways: {len(rulebook.triage_pathways)}")
        print(f"  - Lab tests: {len(rulebook.lab_tests)}")
        print(f"  - Symptom-lab escalation rules: {len(rulebook.symptom_lab_escalation_rules)}")

    except FileNotFoundError as e:
        print(f"ERROR: Rulebook not found: {e}")
        print("Run 'python scripts/compile_rules.py' to compile the rulebook.")
        raise

    except Exception as e:
        print(f"ERROR: Failed to load rulebook: {e}")
        raise

    yield

    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    description=(
        "A rules-first medical triage and lab interpretation API. "
        "This tool provides educational information and care navigation "
        "guidance only. It is NOT for diagnosis or treatment."
    ),
    version=settings.app_version,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Rules-first medical triage API",
        "disclaimer": (
            "This tool is for educational purposes only. "
            "It is NOT for medical diagnosis or treatment."
        ),
        "docs_url": "/docs",
    }
