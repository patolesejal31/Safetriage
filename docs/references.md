# SafeTriage Clinical References & Evidence Base (India Framework)

> [!IMPORTANT]
> **Research and Educational Prototype Notice (India Context)**
> SafeTriage is an experimental academic prototype developed for an MCA research project. It is **not** a certified medical device, diagnostic system, or clinically validated triage protocol. The clinical sources referenced below served as conceptual guides to model rule structures and red-flag warning thresholds based on Indian national guidelines and healthcare practice. Prototype rules must not be interpreted as validated medical advice.

---

## 1. Primary Clinical Guidance Sources (India)

### Cardiological Society of India (CSI)
- **Guideline**: Cardiological Society of India (CSI) Guidelines for the Management of Acute Myocardial Infarction / STEMI
- **Issuing Organization**: Cardiological Society of India (CSI)
- **Relevant Section**: Initial Emergency Triage & 'Red Flag' Warning Signs (retrosternal crushing pain, radiation to left arm/jaw, diaphoresis, dyspnea, presyncope).
- **Prototype Adaptation**: Direct deterministic mapping to **Level 1 (Emergency)**. Acute chest pain with radiation or dyspnea triggers immediate Level 1 red-flag alerts without delay or downgrade. Emergency contact: **112 / 108**.

---

### Indian Stroke Association (ISA)
- **Guideline**: Indian Stroke Association Clinical Practice Guidelines (FAST Triage Protocol)
- **Issuing Organization**: Indian Stroke Association (ISA)
- **Relevant Section**: Face drooping, Arm weakness, Speech difficulty, Time to reach nearest stroke-ready hospital.
- **Prototype Adaptation**: Mapped directly to **Level 1 (Emergency)**. Any acute unilateral motor weakness, facial asymmetry, or sudden slurred speech triggers immediate emergency guidance.

---

### Indian Council of Medical Research (ICMR)
- **Guideline 1**: ICMR Guidelines for Emergency and Critical Care Management (Acute Respiratory Failure)
- **Guideline 2**: ICMR Guidelines for Acute Anaphylaxis Emergency Triage
- **Guideline 3**: ICMR Guidelines for Acute Febrile Illness and Central Nervous System Infections (Encephalopathy & Meningitis)
- **Issuing Organization**: Indian Council of Medical Research (ICMR), Department of Health Research, Govt. of India
- **Relevant Section**: Danger signs in acute respiratory distress (cyanosis, inability to complete full sentences), anaphylactic airway angioedema, and nuchal rigidity with high fever.
- **Prototype Adaptation**: Life-threatening respiratory failure and anaphylaxis mapped to **Level 1 (Emergency)**; febrile meningismus mapped to **Level 2 (Urgent Medical Attention)**.

---

### All India Institute of Medical Sciences (AIIMS New Delhi)
- **Guideline 1**: AIIMS Resuscitation & Emergency Medicine Protocols
- **Guideline 2**: AIIMS Trauma Centre Guidelines for Severe Hemorrhage Management
- **Guideline 3**: AIIMS Emergency Medicine Protocol for Acute Thunderclap Headache and Neurovascular Emergencies
- **Guideline 4**: AIIMS Surgical Triage Guidelines for Acute Abdomen (Suspected Appendicitis/Peritonitis)
- **Issuing Organization**: All India Institute of Medical Sciences (AIIMS New Delhi)
- **Prototype Adaptation**: Acute trauma bleeding and sudden collapse mapped to **Level 1 (Emergency)**; acute abdomen mapped to **Level 2 (Urgent Medical Attention)**.

---

### Indian Academy of Pediatrics (IAP)
- **Guideline**: IAP Guidelines for the Management of Acute Febrile Illness in Pediatric Patients
- **Issuing Organization**: Indian Academy of Pediatrics (IAP)
- **Relevant Section**: Danger signs in infants (< 3 months with high fever >= 38°C / 100.4°F, lethargy, poor feeding, sunken fontanelle).
- **Prototype Adaptation**: Mapped to **Level 2 (Urgent Medical Attention)**.

---

### Ministry of Health and Family Welfare (MoHFW, Govt. of India)
- **Guideline 1**: Standard Treatment Guidelines (STG) for Primary, Secondary, and Tertiary Healthcare
- **Guideline 2**: National Vector Borne Disease Control Programme (NVBDCP) Triage Protocols (Dengue & Malaria warning signs)
- **Guideline 3**: National Tuberculosis Elimination Program (NTEP) Cough Screening Protocol (> 2 weeks cough)
- **Guideline 4**: National Oral Rehydration Therapy & Diarrhea Control Guidelines
- **Issuing Organization**: Ministry of Health and Family Welfare, Government of India
- **Prototype Adaptation**: Informs the 4-level triage schema, routine primary care pathways (Level 3), and home self-care hydration/monitoring guidance (Level 4).

---

## 2. Prototype Algorithmic Rule Catalog Summary

| Rule ID | Clinical Red Flag | Published Source | Prototype Assigned Urgency |
| :--- | :--- | :--- | :--- |
| **RF-001** | Acute chest pain with left arm/jaw radiation | CSI STEMI Guidelines | **Level 1 — Emergency** |
| **RF-002** | FAST stroke symptoms (slurred speech, arm drift) | Indian Stroke Association (ISA) | **Level 1 — Emergency** |
| **RF-003** | Severe dyspnea / cyanosis / speech compromise | ICMR Critical Care Guidelines | **Level 1 — Emergency** |
| **RF-004** | Complete loss of consciousness / collapse | AIIMS Resuscitation Protocols | **Level 1 — Emergency** |
| **RF-005** | Severe uncontrolled pulsatile hemorrhage | AIIMS Trauma Centre Guidelines | **Level 1 — Emergency** |
| **RF-006** | Acute airway angioedema with wheeze | ICMR Anaphylaxis Guidelines | **Level 1 — Emergency** |
| **RF-007** | Thunderclap headache (peak < 1 minute) | AIIMS Neurovascular Protocol | **Level 1 — Emergency** |
| **URG-001** | Acute abdomen / RLQ peritonism with fever | AIIMS Acute Abdomen Protocol | **Level 2 — Urgent** |
| **URG-002** | Pediatric fever (< 3 mo) with lethargy/dehydration | IAP Pediatric Fever Guidelines | **Level 2 — Urgent** |
| **URG-003** | Unilateral swollen painful calf post-travel | CSI Venous Thromboembolism | **Level 2 — Urgent** |
| **URG-004** | High fever (> 102°F) with nuchal rigidity | ICMR Encephalopathy Guidelines | **Level 2 — Urgent** |
| **URG-005** | Sudden painful red eye with visual halo | AIOS Emergency Eye Guidelines | **Level 2 — Urgent** |
| **URG-006** | Severe headache with altered sensorium | AIIMS Neurology Guidelines | **Level 2 — Urgent** |
| **ROU-001** | Persistent subacute cough without dyspnea | MoHFW STG / NTEP Guidelines | **Level 3 — Routine** |
| **ROU-002** | Uncomplicated dysuria without fever/back pain | MoHFW STG for UTI | **Level 3 — Routine** |
| **ROU-003** | Subacute musculoskeletal or lumbar strain | ICMR Musculoskeletal STG | **Level 3 — Routine** |
| **ROU-004** | Subacute headache or gastrointestinal discomfort | MoHFW PHC Clinical Algorithm | **Level 3 — Routine** |
| **SLF-001** | Mild common cold without fever | MoHFW Common Cold Guidelines | **Level 4 — Self-Care** |
| **SLF-002** | Post-exercise muscle soreness (DOMS) | Sports Authority of India Guidelines | **Level 4 — Self-Care** |
| **SLF-003** | Minor superficial scratch / transient thirst | Indian Red Cross / ORS Guidelines | **Level 4 — Self-Care** |
