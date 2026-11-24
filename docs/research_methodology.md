# SafeTriage Research Methodology & Comparative Benchmark Framework

This document outlines the comparative experimental design used to evaluate four triage approaches within the SafeTriage research framework.

---

## 1. Research Objectives & Problem Statement

### 1.1 Problem Statement
Triage in primary care and emergency access points requires balancing timeliness with patient safety. While Large Language Models exhibit high conversational fluency and semantic reasoning, their susceptibility to hallucinations, prompt sensitivity, and stochastic variation makes unconstrained LLM triage unsafe in clinical settings. Conversely, purely rule-based systems are deterministic and auditable, but struggle with colloquial patient vocabulary, indirect phrasing, and multi-symptom context.

### 1.2 Research Hypotheses
1. **Hypothesis 1 (Safety Preservation)**: Enforcing deterministic safety invariants onto LLM predictions will reduce under-triage to 0% for emergency (Level 1) cases while retaining higher conversational flexibility.
2. **Hypothesis 2 (Comparative Acuity Calibration)**: A hybrid approach demonstrates superior macro-F1 and balanced over-triage trade-offs compared to purely rule-based, traditional statistical ML, or standalone unconstrained LLM baselines.

---

## 2. Four Evaluated Architectural Approaches

### Approach A: Deterministic Rule-Based Baseline
- **Mechanism**: Parses positive symptom entities and executes predefined clinical logic trees (e.g., chest pain + radiation -> Level 1).
- **Strengths**: 100% deterministic, zero latency overhead, complete transparency, no hallucinations.
- **Limitations**: Inflexible to phrasing outside the predefined dictionary; lacks nuance for complex multi-morbidity presentations.

### Approach B: Traditional ML/NLP Baseline (Scikit-Learn)
- **Mechanism**: Word and character n-gram TF-IDF vectorization with Logistic Regression trained on labeled scenarios.
- **Reproducibility Protocol**: Trained strictly on the isolated `splits/train.json` partition (700 cases). Evaluated on the held-out `splits/test.json` partition (150 cases).
- **Out-of-Sample Isolation**: Because whole template families are assigned to single splits, test cases contain phrasing and templates never seen during training, preventing artificial inflated accuracy.
- **Research Transparency**: Synthetic dataset training is explicitly disclosed as an algorithmic pipeline benchmark. It is not presented as a clinical validation on real human patients.

### Approach C: LLM-Only Baseline
- **Mechanism**: Directly prompts an LLM with natural-language symptom text and requests a structured JSON response specifying the triage level.
- **Safety Restriction**: Strictly confined to the research evaluation laboratory for comparative benchmarking. **Never** exposed as a patient-facing clinical authority.
- **Failure Logging**: Any provider timeouts, invalid schemas, or network disconnects are recorded explicitly in the evaluation dataset rather than silently filtered.

### Approach D: Proposed SafeTriage Hybrid Model
- **Mechanism**:
  1. Natural language input parsing with multi-status entity tagging (POSITIVE, NEGATED, HISTORICAL, UNCERTAIN).
  2. Execution of the deterministic safety engine to establish a firm floor on urgency.
  3. LLM semantic normalization and conversational explanation generation.
  4. Post-processing safety invariant validation: $\text{Final Level} = \text{select\_most\_urgent}(\text{Rule Level}, \text{Model Level})$.
- **Safety Invariant**: Under no circumstance can the LLM downgrade a Level 1 (Emergency) or Level 2 (Urgent) rule finding.

---

## 3. Synthetic Benchmark Generation & Split Isolation Protocol

To evaluate triage models across diverse clinical presentations without ethical barriers or patient privacy violations, SafeTriage employs a 1,000-case synthetic clinical corpus.

### 3.1 Template Family Architecture
The dataset comprises 27 distinct clinical template families spanning all 4 triage levels:
- **Level 1 (Emergency, 261 cases)**: Acute Coronary Syndrome, FAST stroke presentations, acute respiratory distress, anaphylaxis, severe hypertensive emergencies.
- **Level 2 (Urgent, 224 cases)**: Pediatric fever with lethargy, acute appendicitis/peritonism, severe dehydration, progressive infection signs.
- **Level 3 (Routine Consultation, 222 cases)**: Persistent musculoskeletal pain, stable rash, mild chronic symptoms, uncomplicated subacute issues.
- **Level 4 (Self-Care / Monitoring, 293 cases)**: Mild upper respiratory infections, minor localized abrasions, tension headaches, self-limiting indigestion.

### 3.2 Leakage Prevention via Group Splitting
To avoid optimistic bias caused by near-duplicate text leakage:
1. Every synthetic case belongs to a designated `template_family`.
2. Splitting assigns entire template families to either `train`, `val`, or `test`.
3. Set intersection between any two splits is mathematically guaranteed to be empty:
   $$\text{Families}(\text{Train}) \cap \text{Families}(\text{Val}) = \emptyset, \quad \text{Families}(\text{Train}) \cap \text{Families}(\text{Test}) = \emptyset, \quad \text{Families}(\text{Val}) \cap \text{Families}(\text{Test}) = \emptyset$$
4. ML baseline vectorizers and classifiers are fit exclusively on `train.json` (700 cases) and benchmarked against unseen `test.json` (150 cases).

---

## 4. Experimental Reproducibility & Audit Logging

Every research evaluation run captures:
- `run_id`: Unique UUID.
- `timestamp`: UTC execution timestamp.
- `dataset_version`: Dataset hash/filename, split partition, and sample size ($N$).
- `model_type`: Model identifier and configuration hyperparameters.
- `predictions`: Full itemized record ($y_i, \hat{y}_i$, under_triaged, over_triaged, rules_triggered, latency_ms).
- `metrics`: Pure Python calculation of accuracy, precision, recall, macro-F1, under-triage rate, and confusion matrix.
- `export`: Exportable as CSV and JSON for external verification in Python, R, or SPSS.

