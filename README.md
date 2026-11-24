# SafeTriage: A Hybrid NLP, Rule-Based and Large Language Model Framework for Safe and Explainable Medical Symptom Triage

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Frontend-Next.js%2014%20(App%20Router)-black.svg)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38bdf8.svg)](https://tailwindcss.com/)
[![License: Academic Research](https://img.shields.io/badge/License-Academic%20Research-purple.svg)]()

> [!IMPORTANT]
> **Academic Research Prototype Notice**
> SafeTriage is an experimental software framework developed for an MCA research dissertation. It investigates clinical safety boundaries when combining deterministic decision logic, NLP entity extraction, and Large Language Models.
> **SafeTriage does NOT provide medical diagnosis, prescribe pharmaceutical medications, or replace a licensed physician.**
> If you are experiencing a life-threatening medical emergency (such as severe chest pain, stroke warning signs, or unresponsiveness), call your local emergency service immediately (**112 / 108 / 911**).

---

## 1. System Architecture Overview

SafeTriage is built around a non-negotiable safety invariant: **The Large Language Model is NEVER the sole authority for assigning clinical urgency.**

```
User Natural Language Input
            │
            ▼
   Input Validation & Sanitization
            │
            ▼
   NLP Extraction & Status Tagging
   (POSITIVE, NEGATED, HISTORICAL, THIRD_PARTY, UNCERTAIN)
            │
            ▼
   Follow-Up Risk Analysis
            │
            ▼
   Deterministic Red-Flag Safety Engine
   (Precedence: Level 1 Emergency Rules Evaluated First)
            │
            ▼
   Pluggable LLM / Local Safe Explainer
   (Template Fallback / OpenAI / Gemini with JSON Schema Validation)
            │
            ▼
   Safety Invariant Gatekeeper
   Enforces: final_level = min(rule_level, model_level)
   Model CANNOT downgrade Level 1 Emergency or Level 2 Urgent
            │
            ▼
   Structured Clinical Result & SQLite Persistence
```

### Four-Tier Urgency Framework
- **Level 1 — Emergency / Immediate Care**: Potential life-threatening presentation (AHA/ACC acute coronary syndrome, FAST stroke signs, airway angioedema, thunderclap headache).
- **Level 2 — Urgent Medical Attention**: High-acuity symptoms requiring assessment within hours (acute surgical abdomen, pediatric fever vulnerability, suspected DVT).
- **Level 3 — Routine Medical Consultation**: Subacute complaints appropriate for outpatient primary care appointment (cough > 7 days, uncomplicated dysuria, tension headache).
- **Level 4 — Self-Care Information / Monitoring**: Mild, self-limiting symptoms manageable at home (viral common cold, delayed onset muscle soreness, minor skin scrape).

---

## 2. Technology Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide React icons.
- **Backend**: Python 3.11+, FastAPI, Pydantic V2, SQLAlchemy, Scikit-learn, Pytest, HTTPX.
- **Database**: SQLite (default zero-configuration local database), PostgreSQL-compatible ORM design.
- **AI & NLP**: Rule-based NegEx negation detection, clinical synonym normalization, TF-IDF + LogisticRegression baseline, pluggable LLM interface with 100% offline local fallback.

---

## 3. Quickstart & Installation

### Prerequisites
- Python 3.11+
- Node.js v18+ (tested on Node v22.5.1 and npm 10.8.2)

### Clone / Enter Directory
```bash
cd SafeTriage
```

### Environment Configuration
Copy the template to `.env`:
```powershell
# Windows PowerShell:
Copy-Item .env.example .env

# Linux / macOS:
cp .env.example .env
```
*(The default `.env` is pre-configured for 100% offline local operation without requiring any API keys).*

---

### Step A: Backend Setup & Execution

#### Windows PowerShell:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest-asyncio

# Run automated test suite:
pytest -v

# Start FastAPI backend server:
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Linux / macOS:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest-asyncio

# Run automated test suite:
pytest -v

# Start FastAPI backend server:
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend will be active at:
- **API Base URL**: `http://127.0.0.1:8000/api/v1`
- **Interactive OpenAPI Documentation**: `http://127.0.0.1:8000/docs`
- **Health Check**: `http://127.0.0.1:8000/api/v1/health`

---

### Step B: Frontend Setup & Execution

Open a separate terminal window:

#### Windows PowerShell:
```powershell
cd frontend
npm install
npm run build
npm run start
# Alternatively, for hot-reload development:
# npm run dev
```

#### Linux / macOS:
```bash
cd frontend
npm install
npm run build
npm run start
# Alternatively, for hot-reload development:
# npm run dev
```

Open your browser to: **`http://localhost:3000`**

---

## 4. Web Application Pages

- **Page A — Landing Page (`/`)**: System overview, 3-step triage pipeline visual, research objectives, privacy and medical disclaimers.
- **Page B — Symptom Assessment (`/assess`)**: Natural language text area, age group selector (with opt-out), duration/severity pickers, preset clinical vignettes for one-click testing, dynamic follow-up risk questions, live emergency modal alert.
- **Page C — Assessment Results (`/results/[id]`)**: Distinct urgency level badges, recommended action timeframe, structured positive & negated symptoms breakdown, triggered deterministic clinical rules with rationale and guidelines, explainable decision factors, and print/save tools.
- **Page D — Research Dashboard (`/dashboard`)**: Analytics KPIs, model comparison matrix, under-triage vs over-triage safety rates, red-flag emergency sensitivity, and clinical rule coverage.
- **Page E — Research Evaluation Lab (`/evaluate`)**: Benchmark laboratory comparing **Rule-Based**, **Traditional ML**, **LLM-Only**, and **Proposed Hybrid** models on identical synthetic cases. Interactive 4x4 confusion matrix, per-class statistical tables, and CSV/JSON export.
- **Page F — Assessment History (`/history`)**: Local database records, filterable list, view detail links, single record deletion, and complete history wipe privacy control.
- **Page G — About & Evidence (`/about`)**: Complete research title, problem statement, research gap, safety invariant mathematical formulations, and documented clinical references with issuing bodies and URLs.

---

## 5. Automated Test Suite

Run all automated unit, safety invariant, API, and persistence tests:
```powershell
cd backend
.\.venv\Scripts\pytest -v
```

### Coverage Summary:
- **`test_urgency.py`**: Explicit ordinal ranking verification, min/max selection logic, safety invariant non-downgrade enforcement.
- **`test_nlp_extraction.py`**: Positive symptom extraction, NegEx-style negation ("no chest pain"), temporal historical markers ("five years ago I had pneumonia"), third-party context filtering ("my father had cardiac arrest last year"), spelling variations ("hedache", "throwin up").
- **`test_safety_engine.py`**: Level 1 emergency rules (RF-001 through RF-007), Level 2 urgent rules, Level 3 routine rules, Level 4 self-care rules, and ambiguity uncertainty states.
- **`test_safety_invariants.py`**: Adversarial test cases where patients minimize red flags or an LLM attempts to downgrade acute chest pain; verified that deterministic engine overrides model output.
- **`test_evaluator_metrics.py`**: Pure Python accuracy, 4x4 confusion matrix, under-triage and over-triage rates, and zero-division resilience.
- **`test_persistence_and_api.py`**: FastAPI endpoints, SQLite database transactions, cascade deletion, and benchmark runner API.
- **`verify_e2e_integration.py`**: Live HTTP client verification against concurrently running backend and frontend daemons.

---

## 6. Clinical References & Grounding

All deterministic rules are adapted from public clinical triage guidelines:
1. **AHA/ACC 2021 Chest Pain Guidelines** (Section 3: Initial Triage and Red Flags) — Rule `RF-001`
2. **AHA/ASA Stroke FAST Guidelines** (Face, Arm, Speech, Time) — Rule `RF-002`
3. **British Thoracic Society Emergency Oxygen Guidelines** (Severe Respiratory Distress) — Rule `RF-003`
4. **WAO Anaphylaxis Guidelines: 2020 Update** (Airway Angioedema & Shock) — Rule `RF-006`
5. **NICE NG143 Fever in under 5s** (Pediatric Risk Traffic Light System) — Rule `URG-002`
6. **WSES Guidelines for Acute Abdomen** (Acute Appendicitis / Peritoneal Signs) — Rule `URG-001`
7. **NHS Digital / NHS Pathways** (Four-tier triage schema and exclusion queries)

For complete bibliographic citations and access dates, inspect [`docs/references.md`](docs/references.md).

---

## 7. Known Research Limitations

1. **Non-Certified Medical Software**: SafeTriage is an investigational academic prototype developed for research purposes; it has not undergone formal regulatory clinical certification (FDA SaMD or EU MDR).
2. **Synthetic Evaluation Dataset**: Evaluation benchmarks are derived from a curated synthetic test corpus (32 test cases) to validate pipeline invariants; they do not represent real-world clinical trial efficacy.
3. **Absence of Vital Signs**: Triage is performed solely on patient-entered text without real-time physiological telemetry (SpO2, heart rate, blood pressure, ECG).
4. **Emergency Services Integration**: The system cannot automatically dispatch emergency vehicles or confirm local hospital bed capacity.
