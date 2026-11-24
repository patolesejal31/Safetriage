from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SymptomItem(BaseModel):
    name: str = Field(..., description="Standardized symptom name")
    status: str = Field(default="POSITIVE", description="POSITIVE, NEGATED, HISTORICAL, THIRD_PARTY, UNCERTAIN, UNSUPPORTED")
    duration: Optional[str] = Field(default="unknown")
    severity: Optional[str] = Field(default="unknown")
    raw_text_span: Optional[str] = Field(default="")


class RuleTriggerItem(BaseModel):
    rule_id: str
    rule_name: str
    assigned_level: str
    rationale: str
    source_guideline: str


class FollowUpQuestion(BaseModel):
    id: str
    question: str
    relevant_symptom: str
    options: List[str] = ["Yes", "No", "Uncertain"]
    critical_warning_if_yes: Optional[str] = None


class AssessmentRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=2000, description="Natural language description of symptoms")
    age_group: Optional[str] = Field(default="unknown", description="infant, child, adult, elderly, unknown")
    duration: Optional[str] = Field(default="unknown", description="Subjective duration")
    severity: Optional[str] = Field(default="unknown", description="mild, moderate, severe, unknown")
    associated_answers: Optional[dict] = Field(default_factory=dict, description="Answers to follow-up questions")


class AssessmentResponse(BaseModel):
    id: str
    created_at: datetime
    triage_level: str
    title: str
    care_recommendation: str
    action_timeframe: str
    color: str
    is_emergency: bool
    uncertainty_flag: bool
    explanation: str
    limitations: str
    symptoms: List[SymptomItem]
    negated_symptoms: List[str]
    uncertain_symptoms: List[str]
    unsupported_terms: List[str]
    triggered_rules: List[RuleTriggerItem]
    follow_up_questions: List[FollowUpQuestion]
    emergency_contacts: dict
    execution_mode: str
    latency_ms: float


class AssessmentListItem(BaseModel):
    id: str
    created_at: datetime
    user_age_group: str
    triage_level: str
    symptom_summary: str
    is_emergency: bool
    execution_mode: str


class AssessmentHistoryResponse(BaseModel):
    total: int
    items: List[AssessmentListItem]
