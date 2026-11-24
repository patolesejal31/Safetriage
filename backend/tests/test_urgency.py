import pytest
from app.core.urgency import (
    TriageLevel,
    URGENCY_RANK,
    get_urgency_rank,
    is_more_urgent,
    is_less_urgent,
    is_equally_urgent,
    select_most_urgent,
    select_least_urgent,
    enforce_safety_invariant,
)


def test_urgency_ranking_order():
    """Verify explicit ordering: Level 1 (rank 1) is most urgent, Level 4 (rank 4) is least urgent."""
    assert get_urgency_rank(TriageLevel.LEVEL_1.value) == 1
    assert get_urgency_rank(TriageLevel.LEVEL_2.value) == 2
    assert get_urgency_rank(TriageLevel.LEVEL_3.value) == 3
    assert get_urgency_rank(TriageLevel.LEVEL_4.value) == 4

    assert is_more_urgent(TriageLevel.LEVEL_1.value, TriageLevel.LEVEL_2.value)
    assert is_more_urgent(TriageLevel.LEVEL_2.value, TriageLevel.LEVEL_3.value)
    assert is_more_urgent(TriageLevel.LEVEL_3.value, TriageLevel.LEVEL_4.value)
    assert is_more_urgent(TriageLevel.LEVEL_1.value, TriageLevel.LEVEL_4.value)

    assert is_less_urgent(TriageLevel.LEVEL_4.value, TriageLevel.LEVEL_1.value)
    assert is_equally_urgent(TriageLevel.LEVEL_2.value, TriageLevel.LEVEL_2.value)


def test_select_most_and_least_urgent():
    levels = [TriageLevel.LEVEL_4.value, TriageLevel.LEVEL_2.value, TriageLevel.LEVEL_3.value]
    assert select_most_urgent(levels) == TriageLevel.LEVEL_2.value
    assert select_least_urgent(levels) == TriageLevel.LEVEL_4.value

    levels_with_emergency = [TriageLevel.LEVEL_4.value, TriageLevel.LEVEL_1.value, TriageLevel.LEVEL_3.value]
    assert select_most_urgent(levels_with_emergency) == TriageLevel.LEVEL_1.value


def test_enforce_safety_invariant_downgrade_prevention():
    """Adversarial test: A model recommending Level 4 or Level 3 must NEVER downgrade Level 1 or Level 2."""
    # LLM recommends Level 4 (Self-care), but Rule Engine found Level 1 (Emergency)
    final = enforce_safety_invariant(
        rule_level=TriageLevel.LEVEL_1.value,
        model_level=TriageLevel.LEVEL_4.value
    )
    assert final == TriageLevel.LEVEL_1.value, "Safety invariant failed: Emergency was downgraded!"

    # LLM recommends Level 3 (Routine), but Rule Engine found Level 2 (Urgent)
    final_l2 = enforce_safety_invariant(
        rule_level=TriageLevel.LEVEL_2.value,
        model_level=TriageLevel.LEVEL_3.value
    )
    assert final_l2 == TriageLevel.LEVEL_2.value, "Safety invariant failed: Urgent level was downgraded!"


def test_enforce_safety_invariant_escalation_allowed():
    """If model notices a higher urgency than rule, conservative escalation is permitted."""
    final = enforce_safety_invariant(
        rule_level=TriageLevel.LEVEL_3.value,
        model_level=TriageLevel.LEVEL_2.value
    )
    assert final == TriageLevel.LEVEL_2.value


def test_enforce_safety_invariant_invalid_model_output():
    """If model returns an invalid string or None, rule level must be preserved."""
    assert enforce_safety_invariant(TriageLevel.LEVEL_2.value, None) == TriageLevel.LEVEL_2.value
    assert enforce_safety_invariant(TriageLevel.LEVEL_1.value, "InvalidCategory") == TriageLevel.LEVEL_1.value
    assert enforce_safety_invariant(TriageLevel.LEVEL_3.value, "") == TriageLevel.LEVEL_3.value
