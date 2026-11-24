"""
Follow-up Engine for missing critical information identification.
Generates concise, clinically relevant questions based on extracted symptoms.
"""

from typing import List, Dict, Any
from app.schemas.assessment import FollowUpQuestion


def generate_followup_questions(
    positive_symptoms: List[str],
    answered_ids: List[str]
) -> List[FollowUpQuestion]:
    """
    Generate targeted questions when critical triage qualifiers are not volunteered.
    Avoids asking questions already answered.
    """
    questions: List[FollowUpQuestion] = []

    # Chest pain risk qualifiers
    if "chest pain" in positive_symptoms:
        if "chest_radiation" not in answered_ids:
            questions.append(
                FollowUpQuestion(
                    id="chest_radiation",
                    question="Does the chest pain spread or radiate to your left arm, shoulder, neck, or jaw?",
                    relevant_symptom="chest pain",
                    critical_warning_if_yes="Radiation to arm/jaw is a high-risk sign of acute coronary syndrome."
                )
            )
        if "shortness_of_breath" not in answered_ids and "difficulty breathing" not in positive_symptoms:
            questions.append(
                FollowUpQuestion(
                    id="shortness_of_breath",
                    question="Are you experiencing shortness of breath, dizziness, or unusual cold sweating?",
                    relevant_symptom="chest pain",
                    critical_warning_if_yes="Chest discomfort accompanied by dyspnea or diaphoresis requires emergency evaluation."
                )
            )

    # Headache risk qualifiers
    if "headache" in positive_symptoms:
        if "thunderclap_onset" not in answered_ids and "thunderclap headache" not in positive_symptoms:
            questions.append(
                FollowUpQuestion(
                    id="thunderclap_onset",
                    question="Did the headache reach its maximum unbearable severity within a few seconds (like a sudden explosion)?",
                    relevant_symptom="headache",
                    critical_warning_if_yes="Instantaneous explosive headache requires immediate emergency department evaluation."
                )
            )
        if "stiff_neck" not in answered_ids and "neck stiffness" not in positive_symptoms:
            questions.append(
                FollowUpQuestion(
                    id="stiff_neck",
                    question="Do you have a stiff neck or severe pain when attempting to touch your chin to your chest?",
                    relevant_symptom="headache",
                    critical_warning_if_yes="Headache with neck stiffness is a key warning sign of meningitis."
                )
            )

    # Breathing risk qualifiers
    if "difficulty breathing" in positive_symptoms:
        if "cannot_speak_sentences" not in answered_ids:
            questions.append(
                FollowUpQuestion(
                    id="cannot_speak_sentences",
                    question="Are you unable to speak full sentences without pausing to catch your breath?",
                    relevant_symptom="difficulty breathing",
                    critical_warning_if_yes="Inability to complete sentences indicates severe respiratory compromise."
                )
            )

    # Abdominal pain qualifiers
    if "acute abdominal pain" in positive_symptoms:
        if "rlq_location" not in answered_ids:
            questions.append(
                FollowUpQuestion(
                    id="rlq_location",
                    question="Is the pain sharp and located primarily in the lower right side of your abdomen?",
                    relevant_symptom="acute abdominal pain",
                    critical_warning_if_yes="Lower right quadrant pain with tenderness strongly suggests appendicitis."
                )
            )

    # Limit to maximum 3 questions to prevent user fatigue
    return questions[:3]
