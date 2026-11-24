import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from app.core.time import get_ist_now


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=get_ist_now, nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    user_age_group = Column(String(30), default="unknown")
    raw_input = Column(Text, nullable=False)
    duration = Column(String(100), default="unknown")
    severity = Column(String(50), default="unknown")
    triage_level = Column(String(20), nullable=False, index=True)
    care_recommendation = Column(Text, nullable=False)
    action_timeframe = Column(String(100), default="Immediate")
    explanation = Column(Text, nullable=False)
    limitations = Column(Text, nullable=False)
    is_emergency = Column(Boolean, default=False, index=True)
    uncertainty_flag = Column(Boolean, default=False)
    execution_mode = Column(String(50), default="rule_only")
    latency_ms = Column(Float, default=0.0)

    # Relationships with cascade delete
    symptoms = relationship(
        "StructuredSymptom",
        back_populates="assessment",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    triggered_rules = relationship(
        "RuleTrigger",
        back_populates="assessment",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    user = relationship(
        "User",
        back_populates="assessments"
    )
