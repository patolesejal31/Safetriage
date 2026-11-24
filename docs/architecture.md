# SafeTriage System Architecture

SafeTriage is an architectural framework designed to integrate Natural Language Processing, deterministic medical safety rules, and Large Language Models (LLMs) into an auditable, fail-safe clinical triage pipeline.

---

## 1. High-Level Pipeline Architecture

```
User Symptom Description (Natural Language)
                     │
                     ▼
          [1. Input Validation]
      - Length check (1 - 2000 chars)
      - Non-medical query detection
      - Safe content sanitization
                     │
                     ▼
      [2. NLP Symptom Extractor & Tagging]
      - Tokenization and boundary parsing
      - NegEx-style negation detection (POSITIVE vs NEGATED)
      - Temporal parsing (HISTORICAL vs ACUTE)
      - Third-party distinction (SELF vs FAMILY)
      - Uncertainty classification (UNCERTAIN vs DEFINITE)
      - Synonym normalization (e.g. emesis -> vomiting)
                     │
                     ▼
   [3. Structured Clinical Representation]
      - Positive symptoms list
      - Negated symptoms list
      - Duration and Severity attributes
      - Unrecognized / Ambiguous tokens list
                     │
                     ▼
   [4. Follow-up Question Evaluator]
      - Check for missing critical risk factors
      - (e.g. chest pain -> check radiation / dyspnea)
                     │
                     ▼
  [5. Deterministic Red-Flag Safety Engine]
      - Precedence: Level 1 Emergency Rules evaluated first
      - Evaluates Level 2 Urgent Rules
      - Missing information checks (Uncertainty State)
      - Generates Baseline Deterministic Triage Level
                     │
                     ▼
    [6. Optional LLM / Local Fallback Explainer]
      - Strict JSON schema structured output
      - Plain-language explanation for patient
      - Pluggable provider (Local template fallback / OpenAI / Gemini)
      - Provider timeout / error handler
                     │
                     ▼
    [7. Safety Invariant Validator (Gatekeeper)]
      - Invariant: LLM cannot downgrade deterministic urgency
      - final_level = select_most_urgent([rule_level, model_level])
      - If Level 1 or 2 rule triggered, enforce rule level
                     │
                     ▼
     [8. Structured Response & Audit Logger]
      - SQLite / PostgreSQL assessment persistence
      - Audit trail of triggered rules and model contributions
      - Red-flag emergency modal trigger (if Level 1)
```

---

## 2. Core Safety Invariants

### Invariant 1: The LLM is Never the Sole Authority
The deterministic rule engine runs independently. If an LLM is offline, unconfigured, or invalid, the triage process completes using the rule engine and deterministic explainer without interruption.

### Invariant 2: Explicit Urgency Ranking Function
Urgency comparison is strictly defined by an unambiguous ordinal mapping:
$$\text{Level 1} (1) < \text{Level 2} (2) < \text{Level 3} (3) < \text{Level 4} (4)$$
where smaller numerical rank indicates strictly higher clinical urgency.

### Invariant 3: Absolute Non-Downgrade
```python
def enforce_safety_invariants(rule_level: str, model_level: Optional[str]) -> str:
    if not model_level:
        return rule_level
    # Select most urgent (lowest rank number)
    return select_most_urgent([rule_level, model_level])
```
An LLM can escalate a low-urgency case if it uncovers nuanced clinical context, but it can **never** downgrade a case flagged as urgent or emergency by the rule engine.

---

## 3. Component Breakdown

- **Backend (`FastAPI`)**:
  - `core/urgency.py`: Definitive urgency ranking functions and comparison logic.
  - `nlp/extractor.py`: Multi-status symptom tagger (POSITIVE, NEGATED, HISTORICAL, THIRD_PARTY, UNCERTAIN, UNSUPPORTED).
  - `triage/safety_engine.py`: Deterministic rule evaluator with clinical citations.
  - `triage/followup_engine.py`: Identifies missing critical risk information.
  - `services/llm_provider.py`: Pluggable adapter interface with zero-dependency local fallback.
  - `services/hybrid_service.py`: Pipeline orchestrator enforcing invariant gates.
  - `research/evaluator.py`: Pure Python evaluation metrics engine.
- **Frontend (`Next.js App Router`)**:
  - Medical UI with Tailwind CSS, Lucide React, accessible badges, responsive layouts.
  - Direct communication with FastAPI REST endpoints.
  - Interactive research laboratory with dynamic confusion matrices.
