# SafeTriage Dataset Schema Specification

This document defines the schema requirements for datasets utilized in the SafeTriage Research Evaluation Laboratory.

---

## 1. CSV Dataset Format Specification

When uploading custom evaluation datasets via the web laboratory, CSV files must conform to the following columns:

| Column Name | Data Type | Required | Permitted Values / Description |
| :--- | :--- | :--- | :--- |
| `case_id` | String | Yes | Unique identifier for the scenario (e.g., `SYNTH-001`, `CASE-104`). |
| `text` | String | Yes | Natural language description of symptoms (10 - 2000 characters). |
| `reference_triage_category` | String | Yes | Reference ground-truth category: `Level 1`, `Level 2`, `Level 3`, or `Level 4`. |
| `age_group` | String | Optional | `infant`, `child`, `adult`, `elderly`, or `unknown`. Defaults to `unknown`. |
| `duration` | String | Optional | Symptom duration volunteered by user (e.g. `2 days`, `1 hour`). |
| `severity` | String | Optional | Subjective severity: `mild`, `moderate`, `severe`, or `unknown`. |
| `rationale` | String | Optional | Explanatory note justifying reference triage category. |
| `provenance` | String | Optional | Source guideline citation or synthetic origin statement. |

### Sample CSV Row
```csv
case_id,text,age_group,duration,severity,reference_triage_category,rationale,provenance
SYNTH-001,"Crushing chest pain radiating down my left arm with severe shortness of breath.",adult,past 45 minutes,severe,Level 1,"Acute coronary syndrome presentation","Synthetic vignette based on AHA/ACC 2021"
```

---

## 2. JSON Dataset Format Specification

JSON datasets must consist of an array of objects matching the following schema:

```json
[
  {
    "case_id": "SYNTH-001",
    "text": "Crushing chest pain radiating down my left arm with severe shortness of breath and sweating.",
    "age_group": "adult",
    "duration": "past 45 minutes",
    "severity": "severe",
    "reference_triage_category": "Level 1",
    "expected_red_flags": ["acute_chest_pain_with_radiation", "respiratory_distress"],
    "expected_symptoms": ["chest pain", "pain radiating to left arm", "shortness of breath", "sweating"],
    "expected_negated": [],
    "rationale": "Classic presentation of acute coronary syndrome.",
    "provenance": "Synthetic clinical vignette based on AHA/ACC 2021 Chest Pain Guidelines"
  }
]
```

---

## 3. Bundled Synthetic Research Corpus (1,000 Cases — India Context)

SafeTriage includes a 1,000-case synthetic benchmark corpus generated deterministically (`seed=42`) via `datasets/synthetic/generate_synthetic_cases.py`, customized for the Indian clinical and epidemiological setting.

### 3.1 Corpus Metrics & Partitions
- **Total Unique Vignettes**: Exactly 1,000 records (`SYNTH-0001` through `SYNTH-1000`).
- **Clinical Setting**: Indian healthcare context, clinical terminology, and guidelines (ICMR, AIIMS New Delhi, MoHFW STG, CSI, ISA, IAP).
- **Template Families**: 27 distinct clinical template families.
- **Partitioning Strategy**: Template-family group splitting ensures zero overlap between splits.
  - `splits/train.json`: 700 cases (70%) — ML baseline training
  - `splits/val.json`: 150 cases (15%) — Model tuning and threshold selection
  - `splits/test.json`: 150 cases (15%) — Held-out evaluation (unseen template families)
- **Timezone**: System timestamps represent Indian Standard Time (IST, UTC+05:30).

### 3.2 Triage Class Distribution
- **Level 1 (Emergency)**: 261 cases (26.1%)
- **Level 2 (Urgent)**: 224 cases (22.4%)
- **Level 3 (Routine Consultation)**: 222 cases (22.2%)
- **Level 4 (Self-Care / Monitoring)**: 293 cases (29.3%)

### 3.3 Clinical Phenomenon Coverage (India)
The 1,000-case corpus systematically incorporates:
1. **Linguistic Complexity & Local Phrasing**: Negation phrases (*"no chest pain"*), colloquial symptom descriptions, historical timelines, third-party descriptions, and typographical variations.
2. **Indian Red Flag Invariants**: Acute Coronary Syndrome / STEMI (CSI Guidelines), FAST stroke signs (Indian Stroke Association), pediatric high fever with lethargy (IAP Guidelines), acute peritonitis (AIIMS Surgery), acute anaphylaxis, and hypertensive crises.
3. **Safety Distractors**: Mixed red-flag emergencies paired with benign secondary symptoms (e.g., mild gastric acidity or minor scratch paired with crushing chest pain and left arm radiation) to evaluate deterministic non-downgrade safety overrides.

---

## 4. Dataset Validation Invariants
The backend validation pipeline executes these checks on upload and generation:
1. Header row contains mandatory columns: `case_id`, `text`, `reference_triage_category`.
2. Every `reference_triage_category` is strictly one of `{"Level 1", "Level 2", "Level 3", "Level 4"}`.
3. No duplicate `case_id` values exist.
4. Total rows between 1 and 1,000 for local benchmark stability.
5. Template-family isolation across train, validation, and test splits (zero intersection).

