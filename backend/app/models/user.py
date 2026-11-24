"""
User Model for SafeTriage Authentication and Role-based Access.
"""

import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.models.database import Base
from app.core.time import get_ist_now


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="researcher", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=get_ist_now, nullable=False)

    # Optional relationship with assessments
    assessments = relationship(
        "Assessment",
        back_populates="user",
        lazy="selectin"
    )
