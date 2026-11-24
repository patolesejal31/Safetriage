from fastapi import APIRouter
from app.core.config import settings
from app.triage.rules_catalog import CLINICAL_RULES_CATALOG
from app.services.ml_baseline import ml_baseline
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Verify backend health, runtime status, and subsystem readiness."""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        database=settings.DATABASE_URL.split(":///")[0],
        llm_provider=settings.LLM_PROVIDER,
        llm_configured=bool(settings.LLM_API_KEY) or settings.LLM_PROVIDER == "mock",
        ml_baseline_ready=ml_baseline.is_trained,
        rules_loaded=len(CLINICAL_RULES_CATALOG),
        emergency_contacts={
            "primary": settings.EMERGENCY_PHONE_PRIMARY,
            "ambulance": settings.EMERGENCY_PHONE_AMBULANCE,
            "disclaimer": settings.EMERGENCY_SERVICE_DISCLAIMER
        }
    )
