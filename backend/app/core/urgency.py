"""
Explicit urgency ranking module for SafeTriage.

Urgency scale:
- Level 1: Emergency / Immediate Care (Highest urgency)
- Level 2: Urgent Medical Attention
- Level 3: Routine Medical Consultation
- Level 4: Self-Care Information / Monitoring (Lowest urgency)

Strict ordering:
Level 1 is strictly more urgent than Level 2, 3, and 4.
Smaller rank integer = higher medical urgency.
"""

from typing import Dict, List, Optional
from enum import Enum


class TriageLevel(str, Enum):
    LEVEL_1 = "Level 1"
    LEVEL_2 = "Level 2"
    LEVEL_3 = "Level 3"
    LEVEL_4 = "Level 4"


# Explicit ordinal ranking dictionary
# Rank 1 = most urgent, Rank 4 = least urgent
URGENCY_RANK: Dict[str, int] = {
    TriageLevel.LEVEL_1.value: 1,
    TriageLevel.LEVEL_2.value: 2,
    TriageLevel.LEVEL_3.value: 3,
    TriageLevel.LEVEL_4.value: 4,
}

# Display metadata for each level
LEVEL_METADATA = {
    TriageLevel.LEVEL_1.value: {
        "title": "Emergency / Immediate Care",
        "description": "Life-threatening symptoms requiring immediate emergency evaluation and intervention.",
        "timeframe": "Immediate (Minutes)",
        "color": "red",
        "action_header": "Seek Emergency Medical Care Immediately",
    },
    TriageLevel.LEVEL_2.value: {
        "title": "Urgent Medical Attention",
        "description": "Severe or high-risk symptoms requiring clinical assessment within hours.",
        "timeframe": "Within hours (Same Day)",
        "color": "amber",
        "action_header": "Consult Urgent Care / Emergency Dept Today",
    },
    TriageLevel.LEVEL_3.value: {
        "title": "Routine Medical Consultation",
        "description": "Subacute or mild symptoms appropriate for scheduled outpatient primary care.",
        "timeframe": "Within 24 - 72 hours",
        "color": "blue",
        "action_header": "Schedule Primary Care Appointment",
    },
    TriageLevel.LEVEL_4.value: {
        "title": "Self-Care Information / Monitoring",
        "description": "Mild, self-limiting symptoms manageable with supportive self-care and monitoring.",
        "timeframe": "Monitor 3 - 5 days",
        "color": "emerald",
        "action_header": "Follow Self-Care Guidelines & Monitor for Red Flags",
    },
}


def get_urgency_rank(level: str) -> int:
    """Return explicit rank: 1 (Emergency) to 4 (Self-Care). Raises ValueError if unrecognized."""
    if level not in URGENCY_RANK:
        raise ValueError(f"Unrecognized triage level '{level}'. Must be one of {list(URGENCY_RANK.keys())}")
    return URGENCY_RANK[level]


def is_more_urgent(level_a: str, level_b: str) -> bool:
    """Return True if level_a is strictly more urgent than level_b."""
    return get_urgency_rank(level_a) < get_urgency_rank(level_b)


def is_less_urgent(level_a: str, level_b: str) -> bool:
    """Return True if level_a is strictly less urgent than level_b."""
    return get_urgency_rank(level_a) > get_urgency_rank(level_b)


def is_equally_urgent(level_a: str, level_b: str) -> bool:
    """Return True if level_a and level_b have the same urgency rank."""
    return get_urgency_rank(level_a) == get_urgency_rank(level_b)


def select_most_urgent(levels: List[str]) -> str:
    """
    Select the category representing the highest medical urgency among the inputs.
    Never uses ambiguous min/max without the explicit URGENCY_RANK key function.
    """
    if not levels:
        raise ValueError("Cannot select most urgent from an empty list.")
    return min(levels, key=get_urgency_rank)


def select_least_urgent(levels: List[str]) -> str:
    """Select the category representing the lowest medical urgency among the inputs."""
    if not levels:
        raise ValueError("Cannot select least urgent from an empty list.")
    return max(levels, key=get_urgency_rank)


def enforce_safety_invariant(rule_level: str, model_level: Optional[str]) -> str:
    """
    Enforce the fundamental safety invariant:
    An LLM or ML model output can NEVER downgrade a triage level assigned by deterministic safety rules.

    If a model suggests a MORE urgent level (e.g. noticing a subtle nuance), escalation is allowed.
    If a model suggests a LESS urgent level, the rule level stands firm.
    """
    if not model_level:
        return rule_level

    # If model is invalid or unrecognized, always preserve rule_level
    if model_level not in URGENCY_RANK:
        return rule_level

    # If rule is Level 1 or Level 2, NEVER allow downgrade
    if rule_level in [TriageLevel.LEVEL_1.value, TriageLevel.LEVEL_2.value]:
        if is_less_urgent(model_level, rule_level):
            return rule_level

    # In all cases, take the most conservative / urgent category
    return select_most_urgent([rule_level, model_level])
