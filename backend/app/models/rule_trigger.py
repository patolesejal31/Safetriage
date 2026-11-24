from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class RuleTrigger(Base):
    __tablename__ = "rule_triggers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_id = Column(String(50), nullable=False)
    rule_name = Column(String(150), nullable=False)
    assigned_level = Column(String(20), nullable=False)
    rationale = Column(Text, nullable=False)
    source_guideline = Column(String(255), nullable=False)

    assessment = relationship("Assessment", back_populates="triggered_rules")
