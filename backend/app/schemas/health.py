from typing import Dict, Any
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    database: str
    llm_provider: str
    llm_configured: bool
    ml_baseline_ready: bool
    rules_loaded: int
    emergency_contacts: Dict[str, Any]
