"""
Authentication schemas for SafeTriage user registration, login, and tokens.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid email address for the user")
    password: str = Field(..., min_length=6, max_length=128, description="Password (min 6 characters)")
    full_name: str = Field(..., min_length=2, max_length=150, description="Full name of user")
    role: Optional[str] = Field(default="researcher", description="User role: researcher, clinician, student, patient")


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
