"""
Automated Dataset Validation Suite for SafeTriage 1,000-Case Synthetic Dataset.
Validates:
- Exactly 1,000 unique cases
- Zero duplicate case IDs
- Zero duplicate symptom texts
- Mandatory fields completeness
- Valid ordinal triage labels (Levels 1 to 4)
- Strict template family isolation across splits (zero leakage between Train, Val, Test)
- All 4 classes represented across all splits
- Safety critical annotations (red-flag triggers)
- CSV format schema parity
"""

import os
import json
import csv
import pytest
from app.core.urgency import URGENCY_RANK


def get_dataset_dir():
    # Candidate directory locations
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "synthetic")),
        os.path.abspath(os.path.join("..", "datasets", "synthetic")),
        os.path.abspath(os.path.join("datasets", "synthetic")),
    ]
    for c in candidates:
        if os.path.exists(os.path.join(c, "synthetic_cases_1000.json")):
            return c
    raise FileNotFoundError("Could not find synthetic dataset directory.")


@pytest.fixture(scope="module")
def full_dataset():
    d_dir = get_dataset_dir()
    json_path = os.path.join(d_dir, "synthetic_cases_1000.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def split_datasets():
    d_dir = get_dataset_dir()
    splits = {}
    for s in ["train", "val", "test"]:
        p = os.path.join(d_dir, "splits", f"{s}.json")
        with open(p, "r", encoding="utf-8") as f:
            splits[s] = json.load(f)
    return splits


def test_exact_dataset_size(full_dataset):
    """Requirement: Exactly 1,000 records."""
    assert len(full_dataset) == 1000, f"Expected exactly 1,000 records, got {len(full_dataset)}"


def test_unique_case_ids(full_dataset):
    """Requirement: Zero duplicate case IDs."""
    ids = [c["case_id"] for c in full_dataset]
    assert len(ids) == len(set(ids)), "Duplicate case IDs detected!"
    # Verify format
    assert all(c["case_id"].startswith("SYNTH-") for c in full_dataset)


def test_unique_symptom_texts(full_dataset):
    """Requirement: Zero duplicate symptom texts."""
    texts = [c["text"].strip().lower() for c in full_dataset]
    assert len(texts) == len(set(texts)), f"Duplicate texts detected: {len(texts) - len(set(texts))} duplicates found"


def test_mandatory_fields_presence(full_dataset):
    """Requirement: All cases must have valid required fields."""
    required_keys = [
        "case_id",
        "template_family_id",
        "split",
        "text",
        "age_group",
        "duration",
        "severity",
        "reference_triage_category",
        "rationale",
        "provenance",
        "is_synthetic"
    ]
    for case in full_dataset:
        for k in required_keys:
            assert k in case, f"Case {case.get('case_id')} missing field '{k}'"
            if isinstance(case[k], str):
                assert len(case[k].strip()) > 0, f"Case {case['case_id']} field '{k}' is empty!"
        assert case["is_synthetic"] is True


def test_valid_triage_labels(full_dataset):
    """Requirement: Labels must strictly belong to {'Level 1', 'Level 2', 'Level 3', 'Level 4'}."""
    valid_labels = set(URGENCY_RANK.keys())
    for case in full_dataset:
        lbl = case["reference_triage_category"]
        assert lbl in valid_labels, f"Invalid label '{lbl}' in case {case['case_id']}"


def test_split_family_isolation(split_datasets):
    """
    Requirement: Assign complete template families to individual splits.
    No family may cross train, validation, and test splits.
    """
    train_cases = split_datasets["train"]
    val_cases = split_datasets["val"]
    test_cases = split_datasets["test"]

    train_fams = {c["template_family_id"] for c in train_cases}
    val_fams = {c["template_family_id"] for c in val_cases}
    test_fams = {c["template_family_id"] for c in test_cases}

    assert train_fams.isdisjoint(val_fams), f"Train and Val share families: {train_fams.intersection(val_fams)}"
    assert train_fams.isdisjoint(test_fams), f"Train and Test share families: {train_fams.intersection(test_fams)}"
    assert val_fams.isdisjoint(test_fams), f"Val and Test share families: {val_fams.intersection(test_fams)}"


def test_split_sizes_and_sum(split_datasets, full_dataset):
    """Check split count summing to 1000."""
    total_split_cases = len(split_datasets["train"]) + len(split_datasets["val"]) + len(split_datasets["test"])
    assert total_split_cases == 1000
    assert len(split_datasets["train"]) == 700
    assert len(split_datasets["val"]) == 150
    assert len(split_datasets["test"]) == 150


def test_all_classes_in_all_splits(split_datasets):
    """Verify all 4 triage levels are present in every split."""
    for split_name, cases in split_datasets.items():
        classes_present = {c["reference_triage_category"] for c in cases}
        assert classes_present == {"Level 1", "Level 2", "Level 3", "Level 4"}, (
            f"Split '{split_name}' missing classes: {set(URGENCY_RANK.keys()) - classes_present}"
        )


def test_safety_critical_cases_annotations(full_dataset):
    """Verify Level 1 cases contain expected red flags or clinical urgency metadata."""
    level_1_cases = [c for c in full_dataset if c["reference_triage_category"] == "Level 1"]
    assert len(level_1_cases) >= 200, f"Expected >= 200 Level 1 cases, found {len(level_1_cases)}"
    for c in level_1_cases:
        assert len(c["expected_red_flags"]) > 0 or len(c["expected_symptoms"]) > 0


def test_csv_file_parity():
    """Verify CSV dataset exists and has identical 1,000 rows."""
    d_dir = get_dataset_dir()
    csv_path = os.path.join(d_dir, "synthetic_cases_1000.csv")
    assert os.path.exists(csv_path), "synthetic_cases_1000.csv not found"

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 1000, f"CSV has {len(reader)} rows, expected 1000"
