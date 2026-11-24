import pytest
from app.triage.safety_engine import DeterministicSafetyEngine
from app.core.urgency import TriageLevel


@pytest.fixture
def engine():
    return DeterministicSafetyEngine()


def test_level_1_chest_pain_emergency(engine):
    """Acute chest pain with radiation or severe dyspnea must trigger Level 1 emergency."""
    res = engine.evaluate(
        positive_symptoms=["chest pain", "pain radiating to left arm"],
        negated_symptoms=[],
        uncertain_symptoms=[],
        unsupported_terms=[],
        severity="severe"
    )
    assert res.triage_level == TriageLevel.LEVEL_1.value
    assert res.is_emergency is True
    assert any(r.rule_id == "RF-001" for r in res.triggered_rules)


def test_level_1_stroke_signs(engine):
    """Acute stroke signs must trigger Level 1 emergency immediately."""
    res = engine.evaluate(
        positive_symptoms=["stroke FAST signs"],
        negated_symptoms=[],
        uncertain_symptoms=[],
        unsupported_terms=[]
    )
    assert res.triage_level == TriageLevel.LEVEL_1.value
    assert res.is_emergency is True
    assert any(r.rule_id == "RF-002" for r in res.triggered_rules)


def test_level_1_respiratory_failure(engine):
    """Cyanosis or severe dyspnea must trigger Level 1 emergency."""
    res = engine.evaluate(
        positive_symptoms=["cyanosis", "difficulty breathing"],
        negated_symptoms=[],
        uncertain_symptoms=[],
        unsupported_terms=[],
        severity="severe"
    )
    assert res.triage_level == TriageLevel.LEVEL_1.value
    assert res.is_emergency is True


def test_level_2_acute_abdomen(engine):
    """Severe RLQ abdominal pain with fever or vomiting -> Level 2 Urgent."""
    res = engine.evaluate(
        positive_symptoms=["acute abdominal pain", "vomiting"],
        negated_symptoms=[],
        uncertain_symptoms=[],
        unsupported_terms=[],
        severity="severe"
    )
    assert res.triage_level == TriageLevel.LEVEL_2.value
    assert res.is_emergency is False
    assert any(r.rule_id == "URG-001" for r in res.triggered_rules)


def test_level_2_pediatric_fever(engine):
    """Fever in an infant must trigger Level 2 urgent."""
    res = engine.evaluate(
        positive_symptoms=["fever"],
        negated_symptoms=[],
        uncertain_symptoms=[],
        unsupported_terms=[],
        age_group="infant"
    )
    assert res.triage_level == TriageLevel.LEVEL_2.value
    assert any(r.rule_id == "URG-002" for r in res.triggered_rules)


def test_level_3_routine_cough_and_headache(engine):
    """Subacute cough and headache without red-flags -> Level 3 Routine."""
    res = engine.evaluate(
        positive_symptoms=["cough"],
        negated_symptoms=["shortness of breath", "chest pain"],
        uncertain_symptoms=[],
        unsupported_terms=[],
        severity="moderate"
    )
    assert res.triage_level == TriageLevel.LEVEL_3.value
    assert res.is_emergency is False


def test_level_4_self_care_cold(engine):
    """Runny nose without fever -> Level 4 Self-Care."""
    res = engine.evaluate(
        positive_symptoms=["runny nose"],
        negated_symptoms=["fever"],
        uncertain_symptoms=[],
        unsupported_terms=[],
        severity="mild"
    )
    assert res.triage_level == TriageLevel.LEVEL_4.value
    assert res.is_emergency is False


def test_uncertainty_state_on_ambiguity(engine):
    """Missing recognized symptoms with ambiguity must return uncertainty flag and conservative Level 3."""
    res = engine.evaluate(
        positive_symptoms=[],
        negated_symptoms=[],
        uncertain_symptoms=[],
        unsupported_terms=["weird", "strange"],
        has_ambiguity=True
    )
    assert res.uncertainty_flag is True
    assert res.triage_level == TriageLevel.LEVEL_3.value
    assert "Ambiguous" in res.explanation or "ambiguous" in res.explanation
