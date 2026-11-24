"""
Research Evaluation Metrics Engine for SafeTriage.
Calculates clinical triage metrics in pure Python:
- Accuracy
- Confusion Matrix (4x4)
- Per-class Precision, Recall, and F1
- Macro F1 and Weighted F1
- Under-triage Rate (Overall and Eligible-denominator)
- Over-triage Rate (Overall and Eligible-denominator)
- Red-Flag Emergency Sensitivity
"""

from typing import List, Dict, Any, Tuple
from app.core.urgency import (
    TriageLevel,
    URGENCY_RANK,
    is_less_urgent,
    is_more_urgent,
)
from app.schemas.evaluation import MetricReportSchema, ClassMetricSchema

CLASSES = [
    TriageLevel.LEVEL_1.value,
    TriageLevel.LEVEL_2.value,
    TriageLevel.LEVEL_3.value,
    TriageLevel.LEVEL_4.value,
]


def calculate_evaluation_metrics(
    predictions: List[Dict[str, Any]],
    duration_ms: float = 0.0
) -> MetricReportSchema:
    total = len(predictions)
    if total == 0:
        return MetricReportSchema(
            accuracy=0.0,
            macro_f1=0.0,
            weighted_f1=0.0,
            under_triage_rate_overall=0.0,
            under_triage_rate_eligible=0.0,
            over_triage_rate_overall=0.0,
            over_triage_rate_eligible=0.0,
            red_flag_sensitivity=0.0,
            confusion_matrix=[[0]*4 for _ in range(4)],
            classes=CLASSES,
            per_class_metrics={c: ClassMetricSchema(precision=0.0, recall=0.0, f1_score=0.0, support=0) for c in CLASSES},
            total_evaluated=0,
            failed_predictions=0,
            duration_ms=duration_ms
        )

    # Initialize 4x4 confusion matrix
    # Row: Ground Truth (True), Column: Prediction
    class_indices = {c: i for i, c in enumerate(CLASSES)}
    cm = [[0] * 4 for _ in range(4)]

    correct_count = 0
    failed_count = 0
    under_triage_overall_count = 0
    over_triage_overall_count = 0

    eligible_under_triage_total = 0
    eligible_under_triage_count = 0

    eligible_over_triage_total = 0
    eligible_over_triage_count = 0

    level_1_total = 0
    level_1_correct = 0

    for item in predictions:
        true_level = item.get("ground_truth_level")
        pred_level = item.get("predicted_level")
        err = item.get("error")

        if err or pred_level not in class_indices or true_level not in class_indices:
            failed_count += 1
            continue

        true_idx = class_indices[true_level]
        pred_idx = class_indices[pred_level]
        cm[true_idx][pred_idx] += 1

        if pred_level == true_level:
            correct_count += 1

        # Under-triage: predicted is less urgent than true
        if is_less_urgent(pred_level, true_level):
            under_triage_overall_count += 1
            if true_level != TriageLevel.LEVEL_4.value:
                eligible_under_triage_count += 1

        if true_level != TriageLevel.LEVEL_4.value:
            eligible_under_triage_total += 1

        # Over-triage: predicted is more urgent than true
        if is_more_urgent(pred_level, true_level):
            over_triage_overall_count += 1
            if true_level != TriageLevel.LEVEL_1.value:
                eligible_over_triage_count += 1

        if true_level != TriageLevel.LEVEL_1.value:
            eligible_over_triage_total += 1

        # Level 1 emergency sensitivity
        if true_level == TriageLevel.LEVEL_1.value:
            level_1_total += 1
            if pred_level == TriageLevel.LEVEL_1.value:
                level_1_correct += 1

    accuracy = round(correct_count / total, 4) if total > 0 else 0.0

    under_triage_overall = round(under_triage_overall_count / total, 4) if total > 0 else 0.0
    under_triage_eligible = (
        round(eligible_under_triage_count / eligible_under_triage_total, 4)
        if eligible_under_triage_total > 0
        else 0.0
    )

    over_triage_overall = round(over_triage_overall_count / total, 4) if total > 0 else 0.0
    over_triage_eligible = (
        round(eligible_over_triage_count / eligible_over_triage_total, 4)
        if eligible_over_triage_total > 0
        else 0.0
    )

    red_flag_sensitivity = round(level_1_correct / level_1_total, 4) if level_1_total > 0 else 1.0

    # Per-class metrics
    per_class_metrics: Dict[str, ClassMetricSchema] = {}
    f1_list = []
    support_list = []

    for c in CLASSES:
        idx = class_indices[c]
        tp = cm[idx][idx]
        fp = sum(cm[r][idx] for r in range(4) if r != idx)
        fn = sum(cm[idx][col] for col in range(4) if col != idx)
        support = sum(cm[idx])

        precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0
        recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0.0
        f1 = round(2 * precision * recall / (precision + recall), 4) if (precision + recall) > 0 else 0.0

        per_class_metrics[c] = ClassMetricSchema(
            precision=precision,
            recall=recall,
            f1_score=f1,
            support=support
        )
        f1_list.append(f1)
        support_list.append(support)

    macro_f1 = round(sum(f1_list) / len(f1_list), 4) if f1_list else 0.0
    total_support = sum(support_list)
    weighted_f1 = (
        round(sum(f1 * sup for f1, sup in zip(f1_list, support_list)) / total_support, 4)
        if total_support > 0
        else 0.0
    )

    return MetricReportSchema(
        accuracy=accuracy,
        macro_f1=macro_f1,
        weighted_f1=weighted_f1,
        under_triage_rate_overall=under_triage_overall,
        under_triage_rate_eligible=under_triage_eligible,
        over_triage_rate_overall=over_triage_overall,
        over_triage_rate_eligible=over_triage_eligible,
        red_flag_sensitivity=red_flag_sensitivity,
        confusion_matrix=cm,
        classes=CLASSES,
        per_class_metrics=per_class_metrics,
        total_evaluated=total,
        failed_predictions=failed_count,
        duration_ms=round(duration_ms, 2)
    )
