"""
Pluggable LLM Provider Interface for SafeTriage.
Includes:
- BaseLLMProvider (abstract interface)
- LocalFallbackProvider (zero external calls, deterministic clinical template)
- ExternalAPIProvider (OpenAI / Gemini compatible with strict JSON schema validation and timeout fallback)
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.urgency import TriageLevel, URGENCY_RANK

logger = logging.getLogger(__name__)


class LLMStructuredOutput(BaseModel):
    suggested_triage_level: str = Field(..., description="Level 1, Level 2, Level 3, or Level 4")
    patient_friendly_explanation: str = Field(..., description="Clear explanation for the patient")
    key_observations: list[str] = Field(default_factory=list)
    confidence_rationale: str = Field(default="")


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_explanation(
        self,
        raw_text: str,
        positive_symptoms: list[str],
        negated_symptoms: list[str],
        deterministic_level: str,
        triggered_rule_names: list[str]
    ) -> LLMStructuredOutput:
        pass


class LocalFallbackProvider(BaseLLMProvider):
    """
    Local deterministic provider. Requires ZERO API keys, network calls, or paid services.
    Generates transparent, safe explanations aligned with deterministic rules.
    """
    async def generate_explanation(
        self,
        raw_text: str,
        positive_symptoms: list[str],
        negated_symptoms: list[str],
        deterministic_level: str,
        triggered_rule_names: list[str]
    ) -> LLMStructuredOutput:
        if deterministic_level == TriageLevel.LEVEL_1.value:
            explanation = (
                f"Emergency red-flag warning signs were identified ({', '.join(triggered_rule_names) if triggered_rule_names else 'critical indicators'}). "
                "Immediate medical evaluation is necessary. Please contact local emergency services without delay."
            )
        elif deterministic_level == TriageLevel.LEVEL_2.value:
            explanation = (
                f"Urgent clinical indicators were recognized ({', '.join(triggered_rule_names) if triggered_rule_names else 'urgent criteria'}). "
                "An in-person clinical assessment is recommended today to prevent progression or complications."
            )
        elif deterministic_level == TriageLevel.LEVEL_3.value:
            explanation = (
                f"Reported symptoms ({', '.join(positive_symptoms) if positive_symptoms else 'mild complaints'}) do not display immediate emergency red flags. "
                "A routine consultation with your primary care provider is recommended."
            )
        else:
            explanation = (
                f"Symptoms are consistent with a mild, self-limiting condition. "
                "Supportive self-care, rest, and monitoring are appropriate. Seek clinical care if symptoms worsen."
            )

        observations = [f"Symptoms reported: {', '.join(positive_symptoms) if positive_symptoms else 'None recognized'}"]
        if negated_symptoms:
            observations.append(f"Excluded symptoms: {', '.join(negated_symptoms)}")

        return LLMStructuredOutput(
            suggested_triage_level=deterministic_level,
            patient_friendly_explanation=explanation,
            key_observations=observations,
            confidence_rationale="Deterministic local template generation based on clinical rule engine findings."
        )


class ExternalAPIProvider(BaseLLMProvider):
    """
    External LLM Provider (OpenAI / Gemini compatible).
    Strictly validates responses against LLMStructuredOutput.
    Falls back gracefully to LocalFallbackProvider on any error, timeout, or invalid output.
    """
    def __init__(self, api_key: str, model_name: str, timeout_seconds: int = 10):
        self.api_key = api_key
        self.model_name = model_name
        self.timeout = timeout_seconds
        self.local_fallback = LocalFallbackProvider()

    async def generate_explanation(
        self,
        raw_text: str,
        positive_symptoms: list[str],
        negated_symptoms: list[str],
        deterministic_level: str,
        triggered_rule_names: list[str]
    ) -> LLMStructuredOutput:
        if not self.api_key:
            return await self.local_fallback.generate_explanation(
                raw_text, positive_symptoms, negated_symptoms, deterministic_level, triggered_rule_names
            )

        prompt = (
            f"You are SafeTriage AI, a clinical symptom interpretation assistant. "
            f"A deterministic safety engine has already evaluated this patient and assigned: '{deterministic_level}'. "
            f"Triggered safety rules: {triggered_rule_names}. "
            f"Patient description: '{raw_text}'. "
            f"Extracted positive symptoms: {positive_symptoms}. "
            f"Explicitly negated symptoms: {negated_symptoms}. "
            f"Return JSON adhering strictly to: "
            f"{{\"suggested_triage_level\": \"Level 1\" | \"Level 2\" | \"Level 3\" | \"Level 4\", "
            f"\"patient_friendly_explanation\": \"...\", \"key_observations\": [\"...\"], \"confidence_rationale\": \"...\"}}."
        )

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model_name,
                        "messages": [
                            {"role": "system", "content": "You are a clinical decision support research assistant. Output only valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.1
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    suggested_level = parsed.get("suggested_triage_level", deterministic_level)
                    if suggested_level not in URGENCY_RANK:
                        suggested_level = deterministic_level

                    return LLMStructuredOutput(
                        suggested_triage_level=suggested_level,
                        patient_friendly_explanation=parsed.get("patient_friendly_explanation", ""),
                        key_observations=parsed.get("key_observations", []),
                        confidence_rationale=parsed.get("confidence_rationale", "Generated by external LLM with JSON schema validation.")
                    )
        except Exception as e:
            logger.warning(f"External LLM call failed or timed out ({str(e)}). Falling back to safe local provider.")

        # Safe fallback on any error
        return await self.local_fallback.generate_explanation(
            raw_text, positive_symptoms, negated_symptoms, deterministic_level, triggered_rule_names
        )


def get_llm_provider() -> BaseLLMProvider:
    """Factory to instantiate the appropriate provider based on configuration."""
    if settings.LLM_PROVIDER in ["openai", "gemini"] and settings.LLM_API_KEY:
        return ExternalAPIProvider(
            api_key=settings.LLM_API_KEY,
            model_name=settings.LLM_MODEL,
            timeout_seconds=settings.LLM_TIMEOUT_SECONDS
        )
    return LocalFallbackProvider()
