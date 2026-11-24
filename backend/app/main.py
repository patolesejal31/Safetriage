from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
import app.models  # Ensure all SQLAlchemy models (User, Assessment, etc.) are registered with Base.metadata
from app.models.database import Base, engine
from app.api.v1.router import api_router
from app.services.ml_baseline import initialize_ml_baseline


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    # Initialize ML Baseline on synthetic dataset
    initialize_ml_baseline()
    yield
    # Shutdown logic if needed


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "SafeTriage: A Hybrid NLP, Rule-Based and Large Language Model Framework "
        "for Safe and Explainable Medical Symptom Triage. Research and educational prototype."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "api_docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
        "disclaimer": (
            "SafeTriage is a research prototype developed for an MCA research project. "
            "It does not provide medical diagnosis, prescribe treatments, or replace a doctor."
        )
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import logging, traceback
    logging.error(f"Unhandled exception on {request.method} {request.url}: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred during processing.",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG
    )
