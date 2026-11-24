"""
Comprehensive catalog of clinical deterministic safety rules for SafeTriage.
Each rule includes:
- Rule ID
- Name
- Assigned Level
- Trigger Criteria Function
- Clinical Rationale
- Issuing Organization & Citation
"""

from typing import Dict, List, Callable, Any
from app.core.urgency import TriageLevel


class ClinicalRule:
    def __init__(
        self,
        rule_id: str,
        name: str,
        assigned_level: str,
        evaluator: Callable[[List[str], str, str, str, Dict[str, Any]], bool],
        rationale: str,
        source_guideline: str,
        organization: str,
        recommended_action: str
    ):
        self.rule_id = rule_id
        self.name = name
        self.assigned_level = assigned_level
        self.evaluator = evaluator
        self.rationale = rationale
        self.source_guideline = source_guideline
        self.organization = organization
        self.recommended_action = recommended_action

    def applies(
        self,
        positive_symptoms: List[str],
        severity: str,
        duration: str,
        age_group: str,
        answers: Dict[str, Any]
    ) -> bool:
        return self.evaluator(positive_symptoms, severity, duration, age_group, answers)


# Evaluator Functions
def eval_rf001(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """RF-001: Acute Coronary Syndrome Warning."""
    has_chest = "chest pain" in symptoms
    has_radiation = "pain radiating to left arm" in symptoms or answers.get("chest_radiation") == "Yes"
    has_dyspnea = "difficulty breathing" in symptoms or answers.get("shortness_of_breath") == "Yes"
    is_severe_or_crushing = severity == "severe" or has_radiation or has_dyspnea

    return has_chest and is_severe_or_crushing


def eval_rf002(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """RF-002: FAST Stroke Signs."""
    return "stroke FAST signs" in symptoms or answers.get("stroke_signs") == "Yes"


def eval_rf003(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """RF-003: Severe Respiratory Compromise / Cyanosis."""
    return (
        "cyanosis" in symptoms
        or ("difficulty breathing" in symptoms and severity == "severe")
        or answers.get("cannot_speak_sentences") == "Yes"
    )


def eval_rf004(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """RF-004: Unresponsiveness / Collapse."""
    return "loss of consciousness" in symptoms or answers.get("unresponsive") == "Yes"


def eval_rf005(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """RF-005: Severe Uncontrolled Hemorrhage."""
    return "severe uncontrolled bleeding" in symptoms


def eval_rf006(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """RF-006: Anaphylaxis Signs."""
    return "airway swelling" in symptoms or (
        "rash" in symptoms and "difficulty breathing" in symptoms
    )


def eval_rf007(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """RF-007: Thunderclap Headache (SAH suspicion)."""
    return "thunderclap headache" in symptoms


# Level 2 Urgent Rules
def eval_urg001(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """URG-001: Acute Abdomen / Appendicitis."""
    return "acute abdominal pain" in symptoms and ("vomiting" in symptoms or "fever" in symptoms or "high fever" in symptoms)


def eval_urg002(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """URG-002: Pediatric Fever in Vulnerable Age Group."""
    is_pediatric = age in ["infant", "child"]
    has_fever = "fever" in symptoms or "high fever" in symptoms
    return is_pediatric and has_fever


def eval_urg003(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """URG-003: Suspected DVT."""
    return "unilateral calf swelling" in symptoms


def eval_urg004(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """URG-004: Febrile Meningismus."""
    has_fever = "fever" in symptoms or "high fever" in symptoms
    has_stiff_neck = "neck stiffness" in symptoms
    return has_fever and has_stiff_neck


def eval_urg005(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """URG-005: Acute Glaucoma / Severe Eye Pain."""
    return "severe eye pain" in symptoms


def eval_urg006(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """URG-006: Altered Mental Status with Headache or Metabolic Disturbance."""
    return "altered mental status" in symptoms or ("headache" in symptoms and severity == "severe" and "vomiting" in symptoms)


# Level 3 Routine Rules
def eval_rou001(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """ROU-001: Subacute Respiratory Symptoms."""
    return "cough" in symptoms or "sore throat" in symptoms


def eval_rou002(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """ROU-002: Dysuria / Uncomplicated UTI."""
    return "dysuria" in symptoms


def eval_rou003(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """ROU-003: Non-traumatic Back or Joint Pain."""
    return "back pain" in symptoms or "joint pain" in symptoms or "earache" in symptoms


def eval_rou004(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """ROU-004: Uncomplicated Headache or Vomiting."""
    return ("headache" in symptoms and severity != "severe") or ("vomiting" in symptoms and severity != "severe") or "rash" in symptoms


# Level 4 Self-Care Rules
def eval_slf001(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """SLF-001: Common Cold / Viral Rhinitis."""
    return "runny nose" in symptoms and "fever" not in symptoms and "high fever" not in symptoms


def eval_slf002(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """SLF-002: Muscle Soreness (DOMS)."""
    return "muscle soreness" in symptoms


def eval_slf003(symptoms: List[str], severity: str, duration: str, age: str, answers: Dict[str, Any]) -> bool:
    """SLF-003: Minor Laceration or Mild Thirst."""
    return "minor laceration" in symptoms or "mild thirst" in symptoms or ("nausea" in symptoms and len(symptoms) == 1 and severity == "mild")


CLINICAL_RULES_CATALOG: List[ClinicalRule] = [
    # Level 1 Emergency Rules
    ClinicalRule(
        rule_id="RF-001",
        name="Acute Coronary Syndrome Warning",
        assigned_level=TriageLevel.LEVEL_1.value,
        evaluator=eval_rf001,
        rationale="Retrosternal chest pain with radiation or dyspnea indicates potential myocardial ischemia.",
        source_guideline="Cardiological Society of India (CSI) STEMI Guidelines",
        organization="Cardiological Society of India (CSI)",
        recommended_action="Call emergency medical services immediately (112 / 108). Rest quietly; do not drive."
    ),
    ClinicalRule(
        rule_id="RF-002",
        name="FAST Stroke Warning Signs",
        assigned_level=TriageLevel.LEVEL_1.value,
        evaluator=eval_rf002,
        rationale="Acute unilateral weakness or speech impairment is characteristic of acute ischemic stroke.",
        source_guideline="Indian Stroke Association (ISA) FAST Triage Protocol",
        organization="Indian Stroke Association (ISA)",
        recommended_action="Seek emergency stroke care immediately at nearest stroke-ready hospital (112 / 108)."
    ),
    ClinicalRule(
        rule_id="RF-003",
        name="Severe Respiratory Compromise",
        assigned_level=TriageLevel.LEVEL_1.value,
        evaluator=eval_rf003,
        rationale="Cyanosis or inability to complete full sentences indicates severe hypoxemia.",
        source_guideline="ICMR Emergency & Critical Care Guidelines",
        organization="Indian Council of Medical Research (ICMR)",
        recommended_action="Call emergency services immediately (112 / 108). Sit upright and use rescue inhalers if prescribed."
    ),
    ClinicalRule(
        rule_id="RF-004",
        name="Unresponsiveness / Collapse",
        assigned_level=TriageLevel.LEVEL_1.value,
        evaluator=eval_rf004,
        rationale="Sudden unresponsiveness or loss of consciousness requires urgent resuscitation assessment.",
        source_guideline="AIIMS Resuscitation & Emergency Protocols",
        organization="AIIMS New Delhi",
        recommended_action="Call emergency services immediately (112 / 108). Check breathing and prepare for CPR if indicated."
    ),
    ClinicalRule(
        rule_id="RF-005",
        name="Severe Uncontrolled Hemorrhage",
        assigned_level=TriageLevel.LEVEL_1.value,
        evaluator=eval_rf005,
        rationale="Arterial or refractory bleeding presents acute danger of hypovolemic shock.",
        source_guideline="AIIMS Trauma & Hemorrhage Management Guidelines",
        organization="AIIMS New Delhi",
        recommended_action="Apply heavy direct pressure with clean dressing. Call emergency services immediately (112 / 108)."
    ),
    ClinicalRule(
        rule_id="RF-006",
        name="Anaphylaxis Warning",
        assigned_level=TriageLevel.LEVEL_1.value,
        evaluator=eval_rf006,
        rationale="Airway angioedema with wheeze or systemic rash indicates life-threatening anaphylaxis.",
        source_guideline="ICMR Acute Anaphylaxis Emergency Guidelines",
        organization="Indian Council of Medical Research (ICMR)",
        recommended_action="Administer epinephrine autoinjector if available. Call emergency services immediately (112 / 108)."
    ),
    ClinicalRule(
        rule_id="RF-007",
        name="Thunderclap Headache",
        assigned_level=TriageLevel.LEVEL_1.value,
        evaluator=eval_rf007,
        rationale="Headache peaking instantly within seconds raises high suspicion of subarachnoid hemorrhage.",
        source_guideline="AIIMS Emergency Medicine Neurovascular Protocol",
        organization="AIIMS New Delhi",
        recommended_action="Immediate emergency department neuroimaging evaluation (call 112 / 108)."
    ),

    # Level 2 Urgent Rules
    ClinicalRule(
        rule_id="URG-001",
        name="Acute Peritoneal Abdominal Symptoms",
        assigned_level=TriageLevel.LEVEL_2.value,
        evaluator=eval_urg001,
        rationale="Localized severe abdominal pain with fever or emesis requires urgent surgical evaluation.",
        source_guideline="AIIMS Surgical Triage Guidelines for Acute Abdomen",
        organization="AIIMS New Delhi",
        recommended_action="Seek urgent medical evaluation at nearest community health centre or hospital today."
    ),
    ClinicalRule(
        rule_id="URG-002",
        name="Pediatric High Fever Warning",
        assigned_level=TriageLevel.LEVEL_2.value,
        evaluator=eval_urg002,
        rationale="Infants and children with high fever have elevated risk of rapid decompensation and dehydration.",
        source_guideline="Indian Academy of Pediatrics (IAP) Guidelines for Pediatric Fever",
        organization="Indian Academy of Pediatrics (IAP)",
        recommended_action="Have the child evaluated by a pediatrician or urgent care clinician today."
    ),
    ClinicalRule(
        rule_id="URG-003",
        name="Suspected Deep Vein Thrombosis",
        assigned_level=TriageLevel.LEVEL_2.value,
        evaluator=eval_urg003,
        rationale="Unilateral calf pain, erythema, and swelling requires urgent ultrasound to rule out DVT.",
        source_guideline="Cardiological Society of India (CSI) VTE/DVT Protocol",
        organization="Cardiological Society of India (CSI)",
        recommended_action="Seek urgent clinical examination and vascular Doppler ultrasound today."
    ),
    ClinicalRule(
        rule_id="URG-004",
        name="Febrile Meningismus",
        assigned_level=TriageLevel.LEVEL_2.value,
        evaluator=eval_urg004,
        rationale="High fever with neck stiffness raises concern for CNS infection.",
        source_guideline="ICMR Guidelines for Acute Febrile Encephalopathy & Meningitis",
        organization="Indian Council of Medical Research (ICMR)",
        recommended_action="Urgent medical evaluation today for lumbar puncture and antibiotic assessment."
    ),
    ClinicalRule(
        rule_id="URG-005",
        name="Acute Painful Ocular Emergency",
        assigned_level=TriageLevel.LEVEL_2.value,
        evaluator=eval_urg005,
        rationale="Severe eye pain with vision halos suggests acute glaucoma or keratitis.",
        source_guideline="All India Ophthalmological Society (AIOS) Emergency Guidelines",
        organization="All India Ophthalmological Society (AIOS)",
        recommended_action="Urgent ophthalmological examination today to prevent visual damage."
    ),
    ClinicalRule(
        rule_id="URG-006",
        name="Severe Headache with Altered Sensorium",
        assigned_level=TriageLevel.LEVEL_2.value,
        evaluator=eval_urg006,
        rationale="Severe headache with persistent vomiting or lethargy requires urgent neuro-evaluation.",
        source_guideline="AIIMS Clinical Neurology Guidelines",
        organization="AIIMS New Delhi",
        recommended_action="Urgent same-day clinical assessment at hospital casualty."
    ),

    # Level 3 Routine Rules
    ClinicalRule(
        rule_id="ROU-001",
        name="Subacute Respiratory Symptoms",
        assigned_level=TriageLevel.LEVEL_3.value,
        evaluator=eval_rou001,
        rationale="Persistent cough or sore throat without acute respiratory distress is appropriate for outpatient primary care.",
        source_guideline="MoHFW Standard Treatment Guidelines (STG) for Respiratory Infections",
        organization="Ministry of Health and Family Welfare (MoHFW), Govt. of India",
        recommended_action="Schedule an appointment with your primary care physician or PHC within 24 to 72 hours."
    ),
    ClinicalRule(
        rule_id="ROU-002",
        name="Uncomplicated Lower Urinary Symptoms",
        assigned_level=TriageLevel.LEVEL_3.value,
        evaluator=eval_rou002,
        rationale="Dysuria without back/flank pain or high fever is consistent with uncomplicated cystitis.",
        source_guideline="MoHFW Standard Treatment Guidelines for Urinary Tract Infections",
        organization="Ministry of Health and Family Welfare (MoHFW), Govt. of India",
        recommended_action="Visit a primary health centre or clinic for urine routine testing."
    ),
    ClinicalRule(
        rule_id="ROU-003",
        name="Subacute Musculoskeletal or Ear Pain",
        assigned_level=TriageLevel.LEVEL_3.value,
        evaluator=eval_rou003,
        rationale="Non-traumatic musculoskeletal strain or localized earache without systemic signs.",
        source_guideline="ICMR Musculoskeletal Clinical Guidelines",
        organization="Indian Council of Medical Research (ICMR)",
        recommended_action="Consult a general physician or physiotherapist within a few days."
    ),
    ClinicalRule(
        rule_id="ROU-004",
        name="Mild to Moderate Headache / Gastrointestinal Symptoms",
        assigned_level=TriageLevel.LEVEL_3.value,
        evaluator=eval_rou004,
        rationale="Standard multi-symptom complaints without red flags.",
        source_guideline="MoHFW Primary Health Centre Clinical Algorithm",
        organization="National Health Mission (NHM), Govt. of India",
        recommended_action="Consult your family doctor or dispensary if symptoms do not improve over the next 48 hours."
    ),

    # Level 4 Self-Care Rules
    ClinicalRule(
        rule_id="SLF-001",
        name="Mild Upper Respiratory Infection (Common Cold)",
        assigned_level=TriageLevel.LEVEL_4.value,
        evaluator=eval_slf001,
        rationale="Uncomplicated rhinorrhea and sneezing without fever is typically a self-limiting viral illness.",
        source_guideline="MoHFW Common Cold & Seasonal Viral Management Guidance",
        organization="Ministry of Health and Family Welfare (MoHFW), Govt. of India",
        recommended_action="Rest, maintain fluid intake, steam inhalation, and home monitoring. Monitor for worsening."
    ),
    ClinicalRule(
        rule_id="SLF-002",
        name="Delayed Onset Muscle Soreness (DOMS)",
        assigned_level=TriageLevel.LEVEL_4.value,
        evaluator=eval_slf002,
        rationale="Post-exercise muscle soreness without trauma or dark urine is benign and self-resolving.",
        source_guideline="Sports Authority of India / Sports Medicine Clinical Guidance",
        organization="Sports Authority of India",
        recommended_action="Gentle stretching, hydration, and light activity. Resolves in 2 to 4 days."
    ),
    ClinicalRule(
        rule_id="SLF-003",
        name="Minor Superficial Lesion / Mild Thirst",
        assigned_level=TriageLevel.LEVEL_4.value,
        evaluator=eval_slf003,
        rationale="Superficial skin abrasion or transient mild dehydration resolving with oral fluids.",
        source_guideline="Indian Red Cross Society First Aid Manual",
        organization="Indian Red Cross Society",
        recommended_action="Cleanse with mild soap and clean water. Stay hydrated with ORS or water."
    ),
]
