from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.database import get_db
from app.models.assessment import Assessment
from app.models.user import User
from app.api.deps import get_optional_current_user
from app.schemas.assessment import (
    AssessmentRequest,
    AssessmentResponse,
    AssessmentHistoryResponse,
    AssessmentListItem,
)
from app.services.hybrid_service import hybrid_service

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.post("", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    request: AssessmentRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Submit natural-language symptoms and optional context.
    Executes NLP extraction, deterministic safety engine, LLM explanation, and safety invariants.
    """
    try:
        user_id = current_user.id if current_user else None
        response = await hybrid_service.process_assessment(request, db=db, user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error evaluating symptom assessment: {str(e)}"
        )


@router.get("", response_model=AssessmentHistoryResponse)
def list_assessments(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Retrieve history of symptom assessments (privacy-conscious, no personal identifiers)."""
    total = db.query(Assessment).count()
    records = (
        db.query(Assessment)
        .order_by(desc(Assessment.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )

    items = [
        AssessmentListItem(
            id=r.id,
            created_at=r.created_at,
            user_age_group=r.user_age_group,
            triage_level=r.triage_level,
            symptom_summary=r.raw_input[:100] + ("..." if len(r.raw_input) > 100 else ""),
            is_emergency=r.is_emergency,
            execution_mode=r.execution_mode
        )
        for r in records
    ]

    return AssessmentHistoryResponse(total=total, items=items)


@router.get("/{assessment_id}")
def get_assessment(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve full details of an assessment by ID."""
    record = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    return {
        "id": record.id,
        "created_at": record.created_at,
        "user_age_group": record.user_age_group,
        "raw_input": record.raw_input,
        "duration": record.duration,
        "severity": record.severity,
        "triage_level": record.triage_level,
        "care_recommendation": record.care_recommendation,
        "action_timeframe": record.action_timeframe,
        "explanation": record.explanation,
        "limitations": record.limitations,
        "is_emergency": record.is_emergency,
        "uncertainty_flag": record.uncertainty_flag,
        "execution_mode": record.execution_mode,
        "latency_ms": record.latency_ms,
        "symptoms": [
            {
                "name": s.name,
                "status": s.status,
                "duration": s.duration,
                "severity": s.severity,
                "raw_text_span": s.raw_text_span,
            }
            for s in record.symptoms
        ],
        "triggered_rules": [
            {
                "rule_id": r.rule_id,
                "rule_name": r.rule_name,
                "assigned_level": r.assigned_level,
                "rationale": r.rationale,
                "source_guideline": r.source_guideline,
            }
            for r in record.triggered_rules
        ],
    }


@router.delete("/{assessment_id}", status_code=status.HTTP_200_OK)
def delete_assessment(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Delete an individual assessment record."""
    record = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    db.delete(record)
    db.commit()
    return {"status": "success", "message": f"Assessment {assessment_id} deleted."}


@router.delete("", status_code=status.HTTP_200_OK)
def clear_all_assessments(
    db: Session = Depends(get_db)
):
    """Privacy control: Clear entire assessment history."""
    from app.models.symptom import StructuredSymptom
    from app.models.rule_trigger import RuleTrigger
    db.query(StructuredSymptom).delete(synchronize_session=False)
    db.query(RuleTrigger).delete(synchronize_session=False)
    num_deleted = db.query(Assessment).delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "message": f"All {num_deleted} assessment records deleted."}
