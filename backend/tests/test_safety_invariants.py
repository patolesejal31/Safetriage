import pytest
from app.core.urgency import TriageLevel, enforce_safety_invariant
from app.services.hybrid_service import HybridTriageService
from app.schemas.assessment import AssessmentRequest


@pytest.mark.asyncio
async def test_adversarial_llm_downgrade_attempt():
    """
    Adversarial test: Even if user text minimizes symptoms and an LLM were to output Level 4,
    the deterministic safety engine detects acute chest pain, and the invariant gate MUST enforce Level 1.
    """
    service = HybridTriageService()
    # Case with severe chest pain but patient minimizing it
    req = AssessmentRequest(
        text="Severe crushing pain in center of chest for 15 minutes. Patient insists it is just indigestion and wants to sleep.",
        severity="severe"
    )
    res = await service.process_assessment(req)

    assert res.triage_level == TriageLevel.LEVEL_1.value, "Adversarial failure: Emergency downgraded!"
    assert res.is_emergency is True
    assert any(r.rule_id == "RF-001" for r in res.triggered_rules)


@pytest.mark.asyncio
async def test_emergency_in_long_sentence():
    """Emergency symptom ('cannot move her right arm and her speech is slurred') embedded in longer natural language."""
    service = HybridTriageService()
    req = AssessmentRequest(
        text="We were having lunch and my mother suddenly cannot move her right arm and her speech is slurred and garbled since 20 minutes ago.",
        age_group="elderly"
    )
    res = await service.process_assessment(req)
    assert res.triage_level == TriageLevel.LEVEL_1.value
    assert res.is_emergency is True


@pytest.mark.asyncio
async def test_negated_emergency_does_not_trigger_level_1():
    """An explicitly denied emergency symptom ('do NOT have any chest pain') must NOT trigger Level 1."""
    service = HybridTriageService()
    req = AssessmentRequest(
        text="I do NOT have any chest pain, and I do not have difficulty breathing. Just feeling slightly nauseous after eating leftover food.",
        severity="mild"
    )
    res = await service.process_assessment(req)
    assert res.triage_level != TriageLevel.LEVEL_1.value
    assert res.is_emergency is False
