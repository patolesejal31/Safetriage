import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from app.core.time import get_ist_now


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=get_ist_now, nullable=False, index=True)
    dataset_name = Column(String(150), nullable=False)
    dataset_version = Column(String(50), default="1.0.0")
    model_type = Column(String(50), nullable=False, index=True)
    num_cases = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)
    macro_f1 = Column(Float, nullable=False)
    weighted_f1 = Column(Float, nullable=False)
    under_triage_rate = Column(Float, nullable=False)
    over_triage_rate = Column(Float, nullable=False)
    red_flag_sensitivity = Column(Float, nullable=False)
    metrics_json = Column(Text, nullable=False)
    duration_ms = Column(Float, default=0.0)

    predictions = relationship(
        "EvaluationPrediction",
        back_populates="run",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class EvaluationPrediction(Base):
    __tablename__ = "evaluation_predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(36), ForeignKey("evaluation_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    case_id = Column(String(50), nullable=False)
    input_text = Column(Text, nullable=False)
    ground_truth_level = Column(String(20), nullable=False)
    predicted_level = Column(String(20), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    under_triaged = Column(Boolean, nullable=False)
    over_triaged = Column(Boolean, nullable=False)
    triggered_rules_json = Column(Text, default="[]")
    latency_ms = Column(Float, default=0.0)
    error = Column(String(255), nullable=True)

    run = relationship("EvaluationRun", back_populates="predictions")
