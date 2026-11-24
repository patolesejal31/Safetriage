from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.assessments import router as assessments_router
from app.api.v1.research import router as research_router
from app.api.v1.health import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(assessments_router)
api_router.include_router(research_router)
api_router.include_router(health_router)
