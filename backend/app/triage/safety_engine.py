"""
Deterministic Red-Flag Safety Engine for SafeTriage.
Enforces Level 1 emergency priority, conservative triage assignment,
and explicit uncertainty handling.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from app.core.urgency import (
    TriageLevel,
    URGENCY_RANK,
    select_most_urgent,
    LEVEL_METADATA,
    is_more_urgent,
)
from app.triage.rules_catalog import CLINICAL_RULES_CATALOG, ClinicalRule
from app.schemas.assessment import RuleTriggerItem


@dataclass
class SafetyAssessmentResult:
    triage_level: str
    is_emergency: bool
    uncertainty_flag: bool
    triggered_rules: List[RuleTriggerItem] = field(default_factory=list)
    care_recommendation: str = ""
    action_timeframe: str = ""
    explanation: str = ""
    limitations: str = ""


class DeterministicSafetyEngine:
    def __init__(self, rules: Optional[List[ClinicalRule]] = None):
        self.rules = rules or CLINICAL_RULES_CATALOG

    def evaluate(
        self,
        positive_symptoms: List[str],
        negated_symptoms: List[str],
        uncertain_symptoms: List[str],
        unsupported_terms: List[str],
        severity: str = "unknown",
        duration: str = "unknown",
        age_group: str = "unknown",
        answers: Optional[Dict[str, Any]] = None,
        has_ambiguity: bool = False
    ) -> SafetyAssessmentResult:
        answers = answers or {}
        triggered_rules_list: List[ClinicalRule] = []

        # 1. Evaluate rules in order of priority: Level 1 -> Level 2 -> Level 3 -> Level 4
        # We group rules by level to maintain priority
        rules_by_level = {
            TriageLevel.LEVEL_1.value: [r for r in self.rules if r.assigned_level == TriageLevel.LEVEL_1.value],
            TriageLevel.LEVEL_2.value: [r for r in self.rules if r.assigned_level == TriageLevel.LEVEL_2.value],
            TriageLevel.LEVEL_3.value: [r for r in self.rules if r.assigned_level == TriageLevel.LEVEL_3.value],
            TriageLevel.LEVEL_4.value: [r for r in self.rules if r.assigned_level == TriageLevel.LEVEL_4.value],
        }

        # Check Level 1 Emergency rules first
        for rule in rules_by_level[TriageLevel.LEVEL_1.value]:
            if rule.applies(positive_symptoms, severity, duration, age_group, answers):
                triggered_rules_list.append(rule)

        # Check Level 2 Urgent rules
        for rule in rules_by_level[TriageLevel.LEVEL_2.value]:
            if rule.applies(positive_symptoms, severity, duration, age_group, answers):
                triggered_rules_list.append(rule)

        # Check Level 3 and 4
        for level_key in [TriageLevel.LEVEL_3.value, TriageLevel.LEVEL_4.value]:
            for rule in rules_by_level[level_key]:
                if rule.applies(positive_symptoms, severity, duration, age_group, answers):
                    triggered_rules_list.append(rule)

        # Convert to schema items
        schema_triggers = [
            RuleTriggerItem(
                rule_id=r.rule_id,
                rule_name=r.name,
                assigned_level=r.assigned_level,
                rationale=r.rationale,
                source_guideline=f"{r.organization} ({r.source_guideline})"
            )
            for r in triggered_rules_list
        ]

        # Case A: Emergency rules triggered
        level_1_triggers = [r for r in triggered_rules_list if r.assigned_level == TriageLevel.LEVEL_1.value]
        if level_1_triggers:
            primary_rule = level_1_triggers[0]
            explanation = (
                f"Emergency warning signs were identified by deterministic clinical rule '{primary_rule.name}' "
                f"({primary_rule.rule_id}). Rationale: {primary_rule.rationale} "
                f"Reference guideline: {primary_rule.source_guideline}."
            )
            return SafetyAssessmentResult(
                triage_level=TriageLevel.LEVEL_1.value,
                is_emergency=True,
                uncertainty_flag=False,
                triggered_rules=schema_triggers,
                care_recommendation=primary_rule.recommended_action,
                action_timeframe=LEVEL_METADATA[TriageLevel.LEVEL_1.value]["timeframe"],
                explanation=explanation,
                limitations="SafeTriage is a research prototype. It does not dispatch emergency services. Please contact local emergency services directly."
            )

        # Case B: Other rules triggered (Level 2, 3, or 4)
        if triggered_rules_list:
            assigned_level = select_most_urgent([r.assigned_level for r in triggered_rules_list])
            is_emergency = (assigned_level == TriageLevel.LEVEL_1.value)
            primary_rule = next(r for r in triggered_rules_list if r.assigned_level == assigned_level)

            explanation = (
                f"Triage recommendation assigned by clinical rule '{primary_rule.name}' ({primary_rule.rule_id}). "
                f"Clinical rationale: {primary_rule.rationale}. Guideline source: {primary_rule.source_guideline}."
            )
            return SafetyAssessmentResult(
                triage_level=assigned_level,
                is_emergency=is_emergency,
                uncertainty_flag=False,
                triggered_rules=schema_triggers,
                care_recommendation=primary_rule.recommended_action,
                action_timeframe=LEVEL_METADATA[assigned_level]["timeframe"],
                explanation=explanation,
                limitations="Rule-based prototype assessment. Clinical consultation is necessary to obtain an accurate diagnostic workup."
            )

        # Case C: Ambiguous or unsupported symptom description (Uncertainty State)
        if has_ambiguity or unsupported_terms or not positive_symptoms:
            explanation = (
                "The symptom description is ambiguous or contains terms not matched in the clinical lexicon. "
                "Per research safety protocols, lack of detected keywords is NEVER treated as proof of safety. "
                "An in-person professional consultation is recommended."
            )
            return SafetyAssessmentResult(
                triage_level=TriageLevel.LEVEL_3.value,
                is_emergency=False,
                uncertainty_flag=True,
                triggered_rules=[],
                care_recommendation="Consult a healthcare professional for an in-person medical evaluation to clarify symptoms.",
                action_timeframe="Within 24 to 48 hours",
                explanation=explanation,
                limitations="Uncertainty state: System could not reliably map inputs to known clinical pathways."
            )

        # Case D: Positive symptoms volunteered but no specific rule matched -> default conservatively to Level 3
        explanation = (
            f"Detected symptoms ({', '.join(positive_symptoms)}) did not trigger acute emergency red-flags. "
            "Conservative clinical baseline requires routine outpatient evaluation."
        )
        return SafetyAssessmentResult(
            triage_level=TriageLevel.LEVEL_3.value,
            is_emergency=False,
            uncertainty_flag=False,
            triggered_rules=[],
            care_recommendation="Schedule a routine medical consultation if symptoms persist or cause discomfort.",
            action_timeframe=LEVEL_METADATA[TriageLevel.LEVEL_3.value]["timeframe"],
            explanation=explanation,
            limitations="Preliminary triage estimate. Worsening symptoms warrant immediate reassessment."
        )


safety_engine = DeterministicSafetyEngine()
