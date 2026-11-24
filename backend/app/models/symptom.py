from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class StructuredSymptom(Base):
    __tablename__ = "structured_symptoms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False, default="POSITIVE")  # POSITIVE, NEGATED, HISTORICAL, THIRD_PARTY, UNCERTAIN, UNSUPPORTED
    duration = Column(String(100), default="unknown")
    severity = Column(String(50), default="unknown")
    raw_text_span = Column(String(255), default="")

    assessment = relationship("Assessment", back_populates="symptoms")
