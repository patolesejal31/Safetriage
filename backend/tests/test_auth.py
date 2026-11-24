"""
Unit and integration tests for User Authentication (Registration, Login, Me, Token Validation).
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, get_db

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_register_user_success():
    payload = {
        "email": "dr.sharma@aiims.edu.in",
        "password": "SecurePassword123!",
        "full_name": "Dr. Rajesh Sharma",
        "role": "clinician"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "dr.sharma@aiims.edu.in"
    assert data["user"]["full_name"] == "Dr. Rajesh Sharma"
    assert data["user"]["role"] == "clinician"


def test_register_duplicate_email_fails():
    payload = {
        "email": "dr.sharma@aiims.edu.in",
        "password": "AnotherPassword456!",
        "full_name": "Duplicate User",
        "role": "researcher"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_success():
    payload = {
        "email": "dr.sharma@aiims.edu.in",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "dr.sharma@aiims.edu.in"


def test_login_invalid_password_fails():
    payload = {
        "email": "dr.sharma@aiims.edu.in",
        "password": "WrongPassword999"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_get_current_user_profile():
    # Login first
    login_res = client.post("/api/v1/auth/login", json={
        "email": "dr.sharma@aiims.edu.in",
        "password": "SecurePassword123!"
    })
    token = login_res.json()["access_token"]

    # Call /me with header
    res_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    me_data = res_me.json()
    assert me_data["email"] == "dr.sharma@aiims.edu.in"
    assert me_data["full_name"] == "Dr. Rajesh Sharma"


def test_get_current_user_unauthorized():
    res_me = client.get("/api/v1/auth/me")
    assert res_me.status_code == 401
