import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "SafeTriage: AI-Based Medical Symptom Triage System"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000

    # Database: SQLite default, PostgreSQL compatible
    DATABASE_URL: str = "sqlite:///./safetriage.db"

    # CORS origins
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Security & JWT Authentication
    SECRET_KEY: str = "safetriage-mca-research-secure-jwt-secret-key-32bytes-ist-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Regional Timezone Configuration (India)
    TIMEZONE_NAME: str = "Asia/Kolkata"
    TIMEZONE_OFFSET: str = "UTC+05:30"

    # Emergency phone configuration (defaulting to India 112 / 108; easily configurable for 911 / 999)
    EMERGENCY_PHONE_PRIMARY: str = "112"
    EMERGENCY_PHONE_AMBULANCE: str = "108"
    EMERGENCY_SERVICE_DISCLAIMER: str = (
        "SafeTriage is an informational research prototype. "
        "It does not dispatch emergency services or guarantee hospital capacity."
    )

    # Pluggable LLM settings (default to local mock for zero-key local operation)
    LLM_PROVIDER: str = "mock"  # "mock", "openai", "gemini"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TIMEOUT_SECONDS: int = 10

    # Privacy and security
    MAX_INPUT_LENGTH: int = 2000
    MIN_INPUT_LENGTH: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
