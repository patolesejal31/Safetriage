"""
Hybrid Service Orchestrator for SafeTriage.
Coordinates NLP extraction, deterministic safety engine, LLM explanation,
and mandatory safety invariant validation.
"""

import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.urgency import (
    TriageLevel,
    enforce_safety_invariant,
    LEVEL_METADATA,
    is_more_urgent,
)
from app.nlp.extractor import extractor
from app.triage.safety_engine import safety_engine
from app.triage.followup_engine import generate_followup_questions
from app.services.llm_provider import get_llm_provider
from app.models.assessment import Assessment
from app.models.symptom import StructuredSymptom
from app.models.rule_trigger import RuleTrigger
from app.schemas.assessment import (
    AssessmentRequest,
    AssessmentResponse,
    SymptomItem,
    RuleTriggerItem,
)


class HybridTriageService:
    def __init__(self):
        self.llm_provider = get_llm_provider()

    async def process_assessment(
        self,
        request: AssessmentRequest,
        db: Optional[Session] = None,
        user_id: Optional[str] = None
    ) -> AssessmentResponse:
        start_time = time.perf_counter()

        # 1. NLP Extraction
        extraction = extractor.extract(
            text=request.text,
            user_duration=request.duration,
            user_severity=request.severity
        )

        # 2. Safety Rule Evaluation
        safety_result = safety_engine.evaluate(
            positive_symptoms=extraction.positive_symptoms,
            negated_symptoms=extraction.negated_symptoms,
            uncertain_symptoms=extraction.uncertain_symptoms,
            unsupported_terms=extraction.unsupported_terms,
            severity=extraction.detected_severity,
            duration=extraction.detected_duration,
            age_group=request.age_group or "unknown",
            answers=request.associated_answers or {},
            has_ambiguity=extraction.has_ambiguity
        )

        # 3. LLM / Local Explanation Generation
        triggered_names = [r.rule_name for r in safety_result.triggered_rules]
        llm_output = await self.llm_provider.generate_explanation(
            raw_text=request.text,
            positive_symptoms=extraction.positive_symptoms,
            negated_symptoms=extraction.negated_symptoms,
            deterministic_level=safety_result.triage_level,
            triggered_rule_names=triggered_names
        )

        # 4. Mandatory Safety Invariant Validation Gate
        # Never allow LLM to downgrade Level 1 or Level 2
        final_level = enforce_safety_invariant(
            rule_level=safety_result.triage_level,
            model_level=llm_output.suggested_triage_level
        )

        is_emergency = (final_level == TriageLevel.LEVEL_1.value)

        # 5. Follow-up Questions (Only if not already an emergency)
        follow_up_qs = []
        if not is_emergency:
            answered_keys = list((request.associated_answers or {}).keys())
            follow_up_qs = generate_followup_questions(
                positive_symptoms=extraction.positive_symptoms,
                answered_ids=answered_keys
            )

        # Compute execution time
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        assessment_id = str(uuid.uuid4())

        # Determine explanation and recommendation
        meta = LEVEL_METADATA.get(final_level, LEVEL_METADATA[TriageLevel.LEVEL_3.value])
        care_recommendation = safety_result.care_recommendation or meta["action_header"]
        action_timeframe = safety_result.action_timeframe or meta["timeframe"]

        # Merge patient-friendly explanation with rule rationale
        final_explanation = (
            f"{llm_output.patient_friendly_explanation} "
            f"\n\n[Deterministic Safety Basis]: {safety_result.explanation}"
        )

        limitations = (
            "SafeTriage is an experimental research system and not a diagnostic medical device. "
            "It cannot replace a professional medical consultation, diagnostic tests, or clinical examination. "
            "If your symptoms worsen or you feel unsafe, seek immediate professional care."
        )

        # Prepare response schema
        symptom_items = [
            SymptomItem(
                name=m.canonical_name,
                status=m.status,
                duration=m.duration,
                severity=m.severity,
                raw_text_span=m.raw_span
            )
            for m in extraction.symptoms
        ]

        response = AssessmentResponse(
            id=assessment_id,
            created_at=datetime.utcnow(),
            triage_level=final_level,
            title=meta["title"],
            care_recommendation=care_recommendation,
            action_timeframe=action_timeframe,
            color=meta["color"],
            is_emergency=is_emergency,
            uncertainty_flag=safety_result.uncertainty_flag,
            explanation=final_explanation,
            limitations=limitations,
            symptoms=symptom_items,
            negated_symptoms=extraction.negated_symptoms,
            uncertain_symptoms=extraction.uncertain_symptoms,
            unsupported_terms=extraction.unsupported_terms,
            triggered_rules=safety_result.triggered_rules,
            follow_up_questions=follow_up_qs,
            emergency_contacts={
                "primary": settings.EMERGENCY_PHONE_PRIMARY,
                "ambulance": settings.EMERGENCY_PHONE_AMBULANCE,
                "disclaimer": settings.EMERGENCY_SERVICE_DISCLAIMER
            },
            execution_mode="hybrid" if settings.LLM_PROVIDER != "mock" else "rule_with_local_explainer",
            latency_ms=latency_ms
        )

        # 6. Database Persistence (if db session provided)
        if db is not None:
            db_assessment = Assessment(
                id=assessment_id,
                user_id=user_id,
                user_age_group=request.age_group or "unknown",
                raw_input=request.text,
                duration=extraction.detected_duration,
                severity=extraction.detected_severity,
                triage_level=final_level,
                care_recommendation=care_recommendation,
                action_timeframe=action_timeframe,
                explanation=final_explanation,
                limitations=limitations,
                is_emergency=is_emergency,
                uncertainty_flag=safety_result.uncertainty_flag,
                execution_mode=response.execution_mode,
                latency_ms=latency_ms
            )
            db.add(db_assessment)

            for sym in extraction.symptoms:
                db_sym = StructuredSymptom(
                    assessment_id=assessment_id,
                    name=sym.canonical_name,
                    status=sym.status,
                    duration=sym.duration,
                    severity=sym.severity,
                    raw_text_span=sym.raw_span
                )
                db.add(db_sym)

            for trig in safety_result.triggered_rules:
                db_trig = RuleTrigger(
                    assessment_id=assessment_id,
                    rule_id=trig.rule_id,
                    rule_name=trig.rule_name,
                    assigned_level=trig.assigned_level,
                    rationale=trig.rationale,
                    source_guideline=trig.source_guideline
                )
                db.add(db_trig)

            try:
                db.commit()
            except Exception:
                db.rollback()

        return response


hybrid_service = HybridTriageService()
