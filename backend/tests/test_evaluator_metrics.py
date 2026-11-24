import pytest
from app.research.evaluator import calculate_evaluation_metrics
from app.core.urgency import TriageLevel


def test_perfect_evaluation_metrics():
    predictions = [
        {"ground_truth_level": "Level 1", "predicted_level": "Level 1", "error": None},
        {"ground_truth_level": "Level 2", "predicted_level": "Level 2", "error": None},
        {"ground_truth_level": "Level 3", "predicted_level": "Level 3", "error": None},
        {"ground_truth_level": "Level 4", "predicted_level": "Level 4", "error": None},
    ]
    report = calculate_evaluation_metrics(predictions)
    assert report.accuracy == 1.0
    assert report.under_triage_rate_overall == 0.0
    assert report.over_triage_rate_overall == 0.0
    assert report.red_flag_sensitivity == 1.0
    assert report.macro_f1 == 1.0


def test_under_triage_calculation():
    """Ground truth Level 1 (Emergency), Predicted Level 4 (Self-Care) -> Severe Under-triage."""
    predictions = [
        {"ground_truth_level": "Level 1", "predicted_level": "Level 4", "error": None},
        {"ground_truth_level": "Level 2", "predicted_level": "Level 2", "error": None},
    ]
    report = calculate_evaluation_metrics(predictions)
    assert report.accuracy == 0.5
    assert report.under_triage_rate_overall == 0.5
    assert report.red_flag_sensitivity == 0.0  # Missed Level 1 emergency


def test_over_triage_calculation():
    """Ground truth Level 4 (Self-Care), Predicted Level 2 (Urgent) -> Over-triage."""
    predictions = [
        {"ground_truth_level": "Level 4", "predicted_level": "Level 2", "error": None},
        {"ground_truth_level": "Level 3", "predicted_level": "Level 3", "error": None},
    ]
    report = calculate_evaluation_metrics(predictions)
    assert report.accuracy == 0.5
    assert report.over_triage_rate_overall == 0.5
    assert report.under_triage_rate_overall == 0.0


def test_empty_and_failed_predictions_resilience():
    """Calculations must gracefully handle empty lists and failed predictions without throwing ZeroDivisionError."""
    empty_report = calculate_evaluation_metrics([])
    assert empty_report.accuracy == 0.0

    predictions_with_error = [
        {"ground_truth_level": "Level 1", "predicted_level": "Level 1", "error": "Provider timeout"},
    ]
    report = calculate_evaluation_metrics(predictions_with_error)
    assert report.failed_predictions == 1
    assert report.accuracy == 0.0
