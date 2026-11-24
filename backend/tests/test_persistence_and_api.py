import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import (
    Base,
    get_db,
    Assessment,
    StructuredSymptom,
    RuleTrigger,
    EvaluationRun,
    EvaluationPrediction,
)

# In-memory SQLite with StaticPool so all sessions share the same in-memory database
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


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["rules_loaded"] > 10


def test_submit_assessment_and_persist():
    payload = {
        "text": "I have had a mild headache since yesterday, and today I started vomiting.",
        "duration": "yesterday",
        "severity": "moderate"
    }
    response = client.post("/api/v1/assessments", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["triage_level"] in ["Level 1", "Level 2", "Level 3", "Level 4"]
    assert len(data["symptoms"]) >= 1

    assessment_id = data["id"]

    # Verify retrieval
    get_res = client.get(f"/api/v1/assessments/{assessment_id}")
    assert get_res.status_code == 200
    retrieved = get_res.json()
    assert retrieved["id"] == assessment_id
    assert len(retrieved["symptoms"]) >= 1


def test_list_and_delete_assessment():
    # Submit a case
    payload = {"text": "Small superficial paper cut on index finger with minor stinging.", "severity": "mild"}
    create_res = client.post("/api/v1/assessments", json=payload)
    item_id = create_res.json()["id"]

    # Verify present in list
    list_res = client.get("/api/v1/assessments")
    assert list_res.status_code == 200
    assert any(item["id"] == item_id for item in list_res.json()["items"])

    # Delete
    del_res = client.delete(f"/api/v1/assessments/{item_id}")
    assert del_res.status_code == 200

    # Verify 404 after deletion
    get_after_del = client.get(f"/api/v1/assessments/{item_id}")
    assert get_after_del.status_code == 404


def test_clear_all_assessments():
    client.post("/api/v1/assessments", json={"text": "Temporary cough test", "severity": "mild"})
    clear_res = client.delete("/api/v1/assessments")
    assert clear_res.status_code == 200

    list_res = client.get("/api/v1/assessments")
    assert list_res.json()["total"] == 0


def test_research_evaluate_endpoint():
    payload = {
        "model_types": ["rule_based"],
        "dataset_name": "synthetic_bundled",
        "split": "test"
    }
    response = client.post("/api/v1/research/evaluate", json=payload)
    assert response.status_code == 200
    runs = response.json()
    assert len(runs) == 1
    assert runs[0]["model_type"] == "rule_based"
    assert runs[0]["metrics"]["total_evaluated"] == 150
    assert runs[0]["metrics"]["accuracy"] > 0.5


def test_research_dataset_stats_endpoint():
    response = client.get("/api/v1/research/dataset-stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_cases"] == 1000
    assert data["splits"]["train"] == 700
    assert data["splits"]["val"] == 150
    assert data["splits"]["test"] == 150
    assert data["template_families_count"] == 27
    assert data["is_synthetic"] is True


def test_synthetic_cases_by_split_endpoint():
    res_test = client.get("/api/v1/research/synthetic-cases?split=test")
    assert res_test.status_code == 200
    assert len(res_test.json()) == 150

    res_val = client.get("/api/v1/research/synthetic-cases?split=val")
    assert res_val.status_code == 200
    assert len(res_val.json()) == 150

    res_train = client.get("/api/v1/research/synthetic-cases?split=train")
    assert res_train.status_code == 200
    assert len(res_train.json()) == 700

    res_all = client.get("/api/v1/research/synthetic-cases?split=all")
    assert res_all.status_code == 200
    assert len(res_all.json()) == 1000

