# SafeTriage Deterministic Safety Engine & Rules Catalog

This document provides a comprehensive specification of the deterministic safety rules implemented in SafeTriage, their clinical rationale, trigger thresholds, and safety invariants.

---

## 1. Safety Architecture & Invariant Guarantees

The deterministic safety engine is an independent, pure-logic module that does not rely on external networks, stochastic models, or LLM providers.

### Fundamental Safety Invariants
1. **Emergency Precedence**: Level 1 rules take absolute precedence over any lower-urgency findings.
2. **Deterministic Non-Downgrade Guarantee**: If the deterministic safety engine classifies a case as Level 1 (Emergency) or Level 2 (Urgent), no downstream LLM explanation, ML baseline score, or user self-assessment can downgrade that triage urgency.
3. **Absence of Evidence is Not Evidence of Safety**: The absence of detected red-flag keywords does not certify that a patient is healthy. When user input is ambiguous or critical fields are missing, the engine returns an explicit `UNCERTAINTY` flag advising professional clinical evaluation.
4. **Instant Emergency Cutoff**: If a Level 1 red flag is detected in the input, the evaluation workflow halts further questioning and immediately surfaces emergency contact advice (e.g., call 112 / 108 / 911 immediately).

---

## 2. Complete Rules Catalog

### 2.1 Level 1 — Emergency / Immediate Care

#### Rule ID: `RF-001` — Acute Coronary Syndrome Warning
- **Trigger Symptoms**: Retrosternal or crushing chest pain PLUS (radiation to left arm, neck, or jaw OR shortness of breath OR diaphoresis/sweating).
- **Exclusion**: Explicitly negated mentions (e.g. "no chest pain").
- **Assigned Urgency**: `Level 1`
- **Clinical Rationale**: Acute coronary syndrome / myocardial infarction is time-critical. Early emergency transport and revascularization significantly reduces mortality.
- **Guideline Source**: AHA/ACC 2021 Chest Pain Guidelines.
- **Action Recommendation**: Call local emergency medical services immediately (112 / 108 / 911). Do not attempt to drive yourself.

#### Rule ID: `RF-002` — Acute Stroke Signs (FAST)
- **Trigger Symptoms**: Sudden unilateral arm/leg weakness, facial droop, or sudden slurred/incoherent speech.
- **Assigned Urgency**: `Level 1`
- **Clinical Rationale**: Acute ischemic stroke requires urgent thrombolysis or endovascular thrombectomy within narrow therapeutic time windows (typically <4.5 hours).
- **Guideline Source**: AHA/ASA Stroke FAST Assessment Guidelines.
- **Action Recommendation**: Seek emergency medical evaluation immediately. Note the exact time symptoms started.

#### Rule ID: `RF-003` — Severe Respiratory Compromise
- **Trigger Symptoms**: Severe dyspnea, central cyanosis (blue lips/face), inability to complete sentences, gasping, or refractory asthma attack.
- **Assigned Urgency**: `Level 1`
- **Clinical Rationale**: Hypoxemic respiratory failure is immediately life-threatening.
- **Guideline Source**: British Thoracic Society Emergency Oxygen Guidelines.
- **Action Recommendation**: Call emergency services immediately. Remain seated upright and use prescribed rescue inhalers if available.

#### Rule ID: `RF-004` — Unresponsiveness / Collapse
- **Trigger Symptoms**: Loss of consciousness, collapse without waking, unresponsiveness.
- **Assigned Urgency**: `Level 1`
- **Clinical Rationale**: Sudden collapse without rapid full recovery suggests cardiac arrest, severe intracranial event, or profound syncope.
- **Guideline Source**: ERC / AHA Basic and Advanced Life Support Guidelines.
- **Action Recommendation**: Call emergency services immediately; assess breathing and initiate CPR if pulse/breathing absent.

#### Rule ID: `RF-005` — Severe Uncontrolled Hemorrhage
- **Trigger Symptoms**: Spurting or pulsating bright red blood, continuous heavy bleeding refractory to direct pressure.
- **Assigned Urgency**: `Level 1`
- **Clinical Rationale**: Major arterial hemorrhage can result in hypovolemic shock and exsanguination within minutes.
- **Guideline Source**: ATLS Hemorrhage Control Guidelines.
- **Action Recommendation**: Apply firm, continuous direct pressure with a clean cloth. Call emergency services immediately.

#### Rule ID: `RF-006` — Anaphylaxis Signs
- **Trigger Symptoms**: Acute facial or airway angioedema (swollen tongue, throat tightness) combined with wheezing, urticaria, or feeling faint after allergen exposure.
- **Assigned Urgency**: `Level 1`
- **Clinical Rationale**: Anaphylaxis can lead to fatal upper airway obstruction or vasodilatory shock rapidly.
- **Guideline Source**: World Allergy Organization (WAO) Anaphylaxis Guidelines.
- **Action Recommendation**: Administer epinephrine autoinjector (EpiPen) if available. Call emergency services immediately.

#### Rule ID: `RF-007` — Thunderclap Headache
- **Trigger Symptoms**: Headache with instantaneous onset ("worst headache of life", peaking in seconds), accompanied by neck stiffness or vomiting.
- **Assigned Urgency**: `Level 1`
- **Clinical Rationale**: High clinical sensitivity for aneurysmal subarachnoid hemorrhage (SAH).
- **Guideline Source**: NICE NG232 Head Injury & Neurological Assessment.
- **Action Recommendation**: Immediate emergency department assessment for non-contrast head CT and lumbar puncture.

---

### 2.2 Level 2 — Urgent Medical Attention (Within Hours)

#### Rule ID: `URG-001` — Acute Abdomen / Peritoneal Signs
- **Trigger Symptoms**: Severe, sharp, or localized abdominal pain (especially right lower quadrant) accompanied by fever or vomiting.
- **Assigned Urgency**: `Level 2`
- **Clinical Rationale**: High suspicion of acute surgical abdomen (appendicitis, cholecystitis, diverticulitis, bowel perforation).
- **Guideline Source**: World Society of Emergency Surgery (WSES) Acute Abdomen Guidelines.

#### Rule ID: `URG-002` — Pediatric High Fever in Vulnerable Age Group
- **Trigger Symptoms**: Age under 3 months with fever >= 38°C (100.4°F), or infant with fever, weak cry, sunken fontanelle, or refusal to feed.
- **Assigned Urgency**: `Level 2`
- **Clinical Rationale**: Neonatal and young infant immune immaturity carries elevated risk for invasive bacterial infection and rapid dehydration.
- **Guideline Source**: NICE NG143 Fever in Under 5s.

#### Rule ID: `URG-003` — Suspected Deep Vein Thrombosis (DVT)
- **Trigger Symptoms**: Unilateral calf or lower leg swelling with erythema, warmth, and localized tenderness (especially post-travel or immobility).
- **Assigned Urgency**: `Level 2`
- **Clinical Rationale**: Risk of pulmonary embolism if untreated; urgent duplex ultrasound indicated.
- **Guideline Source**: Wells DVT Criteria & NICE VTE Guidelines.

#### Rule ID: `URG-004` — Febrile Meningismus
- **Trigger Symptoms**: High persistent fever (>102°F) accompanied by neck stiffness, photophobia, or altered alertness, without focal stroke signs.
- **Assigned Urgency**: `Level 2`
- **Clinical Rationale**: Potential bacterial or viral meningitis requiring urgent CSF analysis and antimicrobial therapy.
- **Guideline Source**: Infectious Diseases Society of America (IDSA) Meningitis Guidelines.

#### Rule ID: `URG-005` — Acute Red Eye with Vision Disturbance
- **Trigger Symptoms**: Intense ocular pain, decreased vision, or rainbow halos around lights.
- **Assigned Urgency**: `Level 2`
- **Clinical Rationale**: Potential acute angle-closure glaucoma or severe keratitis; risks permanent vision loss within hours.
- **Guideline Source**: Royal College of Ophthalmologists Emergency Eye Guidance.

---

### 2.3 Level 3 — Routine Medical Consultation (Within Days)

#### Rule ID: `ROU-001` — Subacute Upper/Lower Respiratory Symptoms
- **Trigger Symptoms**: Productive cough, low-grade fever (<101°F), nasal congestion lasting >7 days without shortness of breath or chest pain.
- **Assigned Urgency**: `Level 3`
- **Clinical Rationale**: Uncomplicated bronchitis, sinusitis, or resolving viral illness suitable for primary care consultation.

#### Rule ID: `ROU-002` — Uncomplicated Dysuria
- **Trigger Symptoms**: Burning on urination, urinary frequency without flank/back pain, high fever, or hematuria.
- **Assigned Urgency**: `Level 3`
- **Clinical Rationale**: Uncomplicated cystitis requiring primary care urine dipstick and targeted outpatient antibiotics.

#### Rule ID: `ROU-003` — Subacute Mechanical Musculoskeletal Strain
- **Trigger Symptoms**: Non-traumatic or posture-related back/neck pain lasting days to weeks without neurological deficits (no numbness, foot drop, or incontinence).
- **Assigned Urgency**: `Level 3`
- **Clinical Rationale**: Conservative outpatient physical therapy and clinical follow-up.

---

### 2.4 Level 4 — Self-Care Information & Monitoring

#### Rule ID: `SLF-001` — Acute Mild Upper Respiratory Symptoms (Common Cold)
- **Trigger Symptoms**: Mild runny nose, sneezing, mild throat tickle, duration <4 days, no fever, eating and drinking normally.
- **Assigned Urgency**: `Level 4`
- **Clinical Rationale**: Self-limiting viral rhinovirus syndrome; supportive care (rest, hydration) is clinically indicated.
- **Guideline Source**: CDC Common Cold Management.

#### Rule ID: `SLF-002` — Delayed Onset Muscle Soreness (DOMS)
- **Trigger Symptoms**: Diffuse mild muscle ache following unaccustomed physical activity, full range of motion, normal dark urine color.
- **Assigned Urgency**: `Level 4`
- **Clinical Rationale**: Benign physiological response to eccentric exercise; resolves spontaneously.

#### Rule ID: `SLF-003` — Minor Superficial Skin Laceration / Abrasion
- **Trigger Symptoms**: Minor surface scratch or paper cut, bleeding stopped spontaneously, no foreign body, tetanus up to date.
- **Assigned Urgency**: `Level 4`
- **Clinical Rationale**: First-aid cleansing and clean dressing.
