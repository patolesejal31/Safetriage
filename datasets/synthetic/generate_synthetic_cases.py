"""
SafeTriage Deterministic Synthetic Dataset Generator (India Clinical Context).
Generates exactly 1,000 unique, reproducible clinical vignettes with:
- All 4 triage levels (Level 1 Emergency, Level 2 Urgent, Level 3 Routine, Level 4 Self-Care)
- Clinical provenance grounded in Indian Health Guidelines (ICMR, AIIMS New Delhi, MoHFW, CSI, ISA, IAP)
- Template family isolation across splits (Train 700, Validation 150, Test 150) with zero leakage
- Diverse age groups, durations, severities, synonyms, negations, historical, and adversarial cases
- Seed: 42
"""

import os
import json
import csv
import random
from typing import List, Dict, Any, Tuple


def create_dataset(seed: int = 42, target_count: int = 1000) -> Tuple[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
    rng = random.Random(seed)

    FAMILIES = [
        # ==========================================
        # LEVEL 1 — EMERGENCY / IMMEDIATE CARE (INDIA)
        # ==========================================
        {
            "id": "FAM-L1-ACS-01",
            "level": "Level 1",
            "red_flags": ["acute_chest_pain_with_radiation"],
            "expected_symptoms": ["chest pain", "pain radiating to left arm"],
            "rationale": "Acute crushing retrosternal chest pain radiating to left arm/jaw meets Cardiological Society of India (CSI) STEMI criteria for suspected acute myocardial infarction.",
            "provenance": "Cardiological Society of India (CSI) STEMI Guidelines / AIIMS Emergency Medicine Protocol",
            "primary_symptoms": ["chest pain", "pain radiating to left arm"],
            "variations": [
                "Crushing retrosternal chest pain radiating down my left arm with severe shortness of breath and cold profuse sweating.",
                "Terrible squeezing pressure in center of chest that radiates into left shoulder and jaw for the past 45 minutes.",
                "Substernal chest tightness spreading down my left arm; feeling lightheaded and breaking out in cold sweat.",
                "Severe heaviness on chest like a heavy boulder sitting on me with tingling radiating into left hand and nausea.",
                "Sudden intense chest ache radiating into left arm and neck since 30 minutes, having severe trouble breathing.",
                "Unbearable crushing chest pain that shoots down my left arm whenever I try to move, feeling clammy and faint.",
                "Intense retrosternal chest pain spreading to left arm and back; rescue sublingual sorbitrate did not relieve it.",
                "Heavy central chest pain radiating to left arm, vomiting and breathless since 20 minutes ago.",
            ],
            "adversarial": [
                "Crushing chest pain radiating down my left arm for 40 minutes. I thought it was just severe gastric acidity from dinner, but the pain is unbearable.",
                "Severe pain in chest and left arm for an hour. Patient insists it is just gas and wants to sleep it off.",
                "Terrible chest tightness radiating into left jaw. I have a runny nose too so maybe it is just a seasonal cold?",
            ]
        },
        {
            "id": "FAM-L1-STROKE-02",
            "level": "Level 1",
            "red_flags": ["stroke_fast_signs"],
            "expected_symptoms": ["stroke FAST signs"],
            "rationale": "Sudden onset focal neurological deficit with unilateral arm drift or slurred speech fulfills Indian Stroke Association (ISA) FAST emergency criteria.",
            "provenance": "Indian Stroke Association (ISA) FAST Triage Protocol",
            "primary_symptoms": ["stroke FAST signs"],
            "variations": [
                "My mother suddenly cannot move her right arm and her speech is slurred and garbled since 20 minutes ago.",
                "Sudden weakness on right side of my body, right arm is limp, and words are coming out jumbled and incoherent.",
                "Noticeable facial droop on left side and cannot lift right arm; started abruptly 15 minutes ago.",
                "Patient collapsed into chair, right arm drifting down with incoherent speech and drooling from mouth corner.",
                "Sudden loss of strength in left arm and leg; unable to pronounce simple Hindi or English words clearly since 10 minutes.",
                "Wife's face is sagging on right side and she cannot hold her chai cup with her right hand.",
                "Woke up unable to speak full words properly and right arm feels completely paralyzed.",
                "Sudden difficulty speaking and severe weakness in right arm while having lunch.",
            ],
            "adversarial": [
                "Mother cannot move right arm and has slurred speech since 30 minutes. Family says she just wants to rest on the cot.",
                "Right side facial drooping and arm weakness after waking up. No fever, eating fine otherwise.",
            ]
        },
        {
            "id": "FAM-L1-RESP-03",
            "level": "Level 1",
            "red_flags": ["severe_respiratory_distress", "cyanosis"],
            "expected_symptoms": ["difficulty breathing", "cyanosis"],
            "rationale": "Severe respiratory distress with cyanosis or inability to speak in sentences indicates impending respiratory failure per ICMR guidelines.",
            "provenance": "ICMR Emergency & Critical Care Management Guidelines",
            "primary_symptoms": ["difficulty breathing", "cyanosis"],
            "variations": [
                "Severe difficulty breathing, gasping for air, blue tint on my lips, cannot speak even two full words.",
                "Struggling to breathe, lips are turning bluish, breathing very rapidly and feeling suffocated.",
                "Extreme shortness of breath, audible wheezing stridor, blue fingernails, unable to finish a sentence.",
                "Severe asthma flare-up, used rescue inhaler 5 times with zero relief, gasping and lips look purple.",
                "Sudden suffocating feeling, wheezing loudly, turning blue around mouth, unable to lie flat on bed.",
                "Heavy gasping for air, chest retractions visible, fingernails turning blue, completely breathless.",
                "Breathless at complete rest, gasping, cyanotic lips, heart pounding at 140 bpm.",
                "Severe breathing distress, choking sensation, blue discoloration of lips since 20 minutes.",
            ],
            "adversarial": [
                "Cannot breathe properly and lips look slightly blue, but I just took ginger tea hoping it clears up.",
            ]
        },
        {
            "id": "FAM-L1-UNRESP-04",
            "level": "Level 1",
            "red_flags": ["unresponsiveness_loss_of_consciousness"],
            "expected_symptoms": ["loss of consciousness"],
            "rationale": "Sudden unresponsiveness or collapse represents acute hemodynamic or neurological collapse requiring immediate CPR/resuscitation per AIIMS protocol.",
            "provenance": "AIIMS Resuscitation & Emergency Medicine Protocol",
            "primary_symptoms": ["loss of consciousness"],
            "variations": [
                "Patient is unresponsive, collapsed 5 minutes ago and will not wake up to loud calling or shaking.",
                "My husband suddenly blacked out, collapsed onto floor and remains completely unconscious.",
                "Passed out suddenly while standing in market, fell to ground, breathing shallowly and unarousable for 4 minutes.",
                "Colleague slumped over office desk, unresponsive to voice or pinch, eyes rolling back.",
                "Grandmother collapsed in veranda, unresponsive, pulse is faint, breathing irregularly.",
                "Sudden blackout and unresponsiveness after standing up, will not respond to voice.",
                "Unconscious person found on floor, unresponsive, labored breathing since 10 minutes.",
                "Fainted suddenly, hit head, completely unarousable and unresponsive to pain stimulus.",
            ],
            "adversarial": [
                "Patient collapsed and is unresponsive, but breathing slowly. Family wants to know if they can pour water on forehead.",
            ]
        },
        {
            "id": "FAM-L1-BLEED-05",
            "level": "Level 1",
            "red_flags": ["severe_uncontrolled_hemorrhage"],
            "expected_symptoms": ["severe uncontrolled bleeding"],
            "rationale": "Pulsatile or heavy arterial hemorrhage refractory to direct pressure leads to hypovolemic shock within minutes per AIIMS trauma guidelines.",
            "provenance": "AIIMS Trauma Centre Acute Hemorrhage Guidelines",
            "primary_symptoms": ["severe uncontrolled bleeding"],
            "variations": [
                "Deep wound on thigh spurting bright red blood that will not stop despite holding heavy compression.",
                "Accident with farm machinery, arm is bleeding profusely with bright red pulsating blood.",
                "Severe laceration on forearm from broken windshield, blood is gushing out rapidly soaking through four thick towels.",
                "Deep puncture wound to neck, continuous heavy arterial blood loss, feeling dizzy, pale and cold.",
                "Deep glass cut on wrist with spurting bright red blood refractory to continuous direct pressure.",
                "Post-surgical incision burst open, copious bright red bleeding pooling onto floor within 5 minutes.",
                "Motorcycle accident on highway, pulsating bright red bleeding from leg, losing consciousness from blood loss.",
                "Deep stab laceration to groin, uncontrolled rapid bleeding soaking through compression cloth.",
            ],
            "adversarial": [
                "Deep cut on thigh spurting bright red blood. Applied a cloth but it soaked through in 1 minute; waiting to see if it stops.",
            ]
        },
        {
            "id": "FAM-L1-ANAPHYLAXIS-06",
            "level": "Level 1",
            "red_flags": ["anaphylaxis"],
            "expected_symptoms": ["airway swelling", "difficulty breathing"],
            "rationale": "Acute multisystem allergic response with airway compromise and bronchospasm meets ICMR criteria for anaphylactic shock.",
            "provenance": "ICMR Acute Anaphylaxis Emergency Triage Protocol",
            "primary_symptoms": ["airway swelling", "difficulty breathing"],
            "variations": [
                "Ate peanuts 15 minutes ago, now throat is swelling shut, hives all over, wheezing loudly and feeling faint.",
                "Stung by wasp in farm 10 minutes ago, tongue swelling rapidly, cannot swallow saliva, throat tightness and wheezing.",
                "Took antibiotic injection 20 minutes ago, full body red rash, lips and tongue swollen, gasping for air.",
                "Severe allergic reaction to prawns, throat feels like closing up, hives, wheezing, vision fading.",
                "Swollen tongue and throat closing up following honeybee sting, loud stridor, lightheadedness.",
                "Sudden airway swelling and widespread hives after eating walnuts, vomiting and struggling to breathe.",
                "Throat swelling shut, unable to swallow, severe wheezing and clammy cold skin after medication.",
                "Allergic reaction, lips and uvula massive swelling, hoarse voice turning into gasping within 15 minutes.",
            ],
            "adversarial": [
                "Throat feels like swelling shut and wheezing after eating seafood, but I took an antiallergic pill and want to wait.",
            ]
        },
        {
            "id": "FAM-L1-THUNDERCLAP-07",
            "level": "Level 1",
            "red_flags": ["thunderclap_headache"],
            "expected_symptoms": ["thunderclap headache"],
            "rationale": "Sudden headache reaching peak intensity within seconds (thunderclap) is characteristic of subarachnoid hemorrhage per AIIMS neurovascular protocols.",
            "provenance": "AIIMS Emergency Medicine Neurovascular Triage Protocol",
            "primary_symptoms": ["thunderclap headache"],
            "variations": [
                "Sudden onset of the worst headache of my entire life, feels like a thunderclap inside my skull, accompanied by vomiting and neck stiffness.",
                "Explosive headache hit like a bolt of lightning peaking in 10 seconds, excruciating agony, vomited twice.",
                "Instantaneous unbearable headache, worst ever 10/10 severity, stiff neck, sensitive to light since 20 minutes.",
                "Sudden thunderclap pain in back of head while lifting heavy water bucket, unbearable agony, dizzy and threw up.",
                "Sudden explosion in head reaching peak intensity in under a minute, neck is rigid, cannot open eyes.",
                "Worst headache of my life struck without warning 30 minutes ago, throbbing agonizingly with nausea.",
                "Sudden thunderclap headache like being hit with a club on head, vomiting and stiff neck.",
                "Instantaneous 10/10 headache reaching maximum pain in 15 seconds, crying in pain, stiff neck.",
            ],
            "adversarial": [
                "Worst headache of my entire life started instantly like thunderclap, but I have a mild runny nose too so maybe it is sinus?",
            ]
        },

        # ==========================================
        # LEVEL 2 — URGENT MEDICAL ATTENTION (INDIA)
        # ==========================================
        {
            "id": "FAM-L2-APPEN-08",
            "level": "Level 2",
            "red_flags": ["acute_abdomen"],
            "expected_symptoms": ["acute abdominal pain", "fever", "vomiting"],
            "rationale": "Acute localized right lower quadrant abdominal pain with fever or emesis requires urgent surgical evaluation for acute appendicitis per AIIMS surgical guidelines.",
            "provenance": "AIIMS Surgical Triage Guidelines for Acute Abdomen",
            "primary_symptoms": ["acute abdominal pain", "vomiting"],
            "variations": [
                "Severe sharp pain in the lower right abdomen since this morning, high fever of 102F, cannot stand straight, and throwing up.",
                "Intense pain in right lower belly worsening with every step, nauseous, threw up three times, fever 101.5F.",
                "Severe abdominal pain focused on right lower quadrant for 8 hours, feverish, unable to eat or keep fluids down.",
                "Constant sharp right lower abdomen cramps, rebound tenderness, low grade fever and repeated vomiting.",
                "Lower right side stomach pain getting progressively more severe over 12 hours, high temperature, dry heaving.",
                "Severe sharp belly pain in right lower quadrant, chills, nausea, painful when riding in autorickshaw over bumps.",
                "Agonizing right lower abdomen ache for 10 hours, fever of 102F, chills, vomiting green bile.",
                "Sharp localized lower right abdomen tenderness, feverish, curled up in bed unable to walk.",
            ],
            "adversarial": [
                "Severe sharp pain in lower right abdomen with fever, but no chest pain and no breathing trouble.",
            ]
        },
        {
            "id": "FAM-L2-PED-FEVER-09",
            "level": "Level 2",
            "red_flags": ["pediatric_fever_and_dehydration"],
            "expected_symptoms": ["pediatric fever", "lethargy"],
            "rationale": "Fever in an infant under 3 months or pediatric patient with lethargy and poor feeding requires urgent clinical examination per Indian Academy of Pediatrics (IAP) guidelines.",
            "provenance": "Indian Academy of Pediatrics (IAP) Guidelines for Acute Febrile Illness",
            "primary_symptoms": ["fever"],
            "variations": [
                "My 3-month-old baby has a 102.5F fever, crying weakly, refusing to drink any milk, and has sunken soft spot on head.",
                "Two-month-old infant with 103F temperature, whimpering weakly, dry diapers for 8 hours, very lethargic.",
                "Seven-week-old newborn burning up with 101.8F fever, refusing breastfeeds, difficult to wake up.",
                "Ten-week-old infant has 102.2F fever, irritable, crying inconsolably, fontanelle appears depressed.",
                "Baby under 3 months with high temperature of 102.8F, pale mottled skin, not taking feeds for 6 hours.",
                "Four-month-old baby with 103F fever, breathing fast, whimpering, no tears when crying, very sluggish.",
                "Newborn 6 weeks old with 102.4F fever, weak suck, floppy arms, fever not coming down with paracetamol drops.",
                "Eight-week-old infant with high fever, vomiting feeds, lethargic and sleeping constantly.",
            ],
            "adversarial": [
                "Baby has 102.5F fever and crying weakly, no cough, no rash on body.",
            ]
        },
        {
            "id": "FAM-L2-DVT-10",
            "level": "Level 2",
            "red_flags": ["suspected_dvt"],
            "expected_symptoms": ["unilateral calf swelling"],
            "rationale": "Unilateral calf erythema, warmth, and swelling following prolonged travel carries high risk for deep vein thrombosis per CSI VTE guidelines.",
            "provenance": "Cardiological Society of India (CSI) Venous Thromboembolism Guidelines",
            "primary_symptoms": ["unilateral calf swelling"],
            "variations": [
                "Swollen and very red, warm calf on my left leg after an 18-hour train journey yesterday, painful to walk on.",
                "Right calf is visibly larger than left, red, warm to touch and throbbing with pain since yesterday evening.",
                "Painful swelling in left calf after a long bus road trip, tight shiny skin, tender when flexing foot.",
                "Unilateral lower leg swelling, left calf is 3cm larger, red and hot, painful when putting weight on it.",
                "One leg is swollen, tender calf, warmth and redness developed over past 24 hours after prolonged bedrest.",
                "Painful throbbing in left calf with visible redness and heat, hurts to walk, completed long interstate bus ride 2 days ago.",
                "Right calf swollen and hard like a stone, red, hot, dull aching pain worsening when standing up.",
                "Swelling localized to right calf with redness and warmth, no trauma, recent long travel 2 days ago.",
            ],
            "adversarial": [
                "Left calf is swollen and warm after long journey. No chest pain and no shortness of breath.",
            ]
        },
        {
            "id": "FAM-L2-MENING-11",
            "level": "Level 2",
            "red_flags": ["febrile_meningismus"],
            "expected_symptoms": ["high fever", "neck stiffness"],
            "rationale": "High fever accompanied by nuchal rigidity and photophobia raises urgent concern for central nervous system infection per ICMR guidelines.",
            "provenance": "ICMR Guidelines for Acute Febrile Encephalopathy & Meningitis",
            "primary_symptoms": ["high fever", "neck stiffness"],
            "variations": [
                "Persistent high fever of 103F for 4 days, stiff neck, extreme fatigue, but I have no chest pain and no breathing trouble.",
                "High temperature of 102.5F, cannot bend neck to touch chin to chest, severe headache and photophobia.",
                "Fever 103.2F, severe headache, neck feels completely locked and stiff, sensitive to room light.",
                "Burning with fever for 3 days, neck stiffness, painful when looking down, feeling very confused and drowsy.",
                "Fever of 102.8F, throbbing head, stiff neck that will not flex forward, nausea and extreme fatigue.",
                "High fever 103F, neck rigidity, room lights hurt eyes, severe dull headache since 2 days.",
                "Febrile illness with 102F, inability to touch chin to sternum due to neck stiffness, drowsy.",
                "Temperature 103.5F for 48 hours, stiff neck muscles, photophobia, headache and generalized weakness.",
            ],
            "adversarial": [
                "High fever 103F and stiff neck for 3 days. I do not have chest pain and no breathing difficulty.",
            ]
        },
        {
            "id": "FAM-L2-EYE-12",
            "level": "Level 2",
            "red_flags": ["acute_angle_closure_glaucoma"],
            "expected_symptoms": ["severe eye pain"],
            "rationale": "Severe throbbing unilateral ocular pain with visual haloes and nausea indicates acute angle-closure glaucoma per AIOS guidelines.",
            "provenance": "All India Ophthalmological Society (AIOS) Emergency Eye Guidelines",
            "primary_symptoms": ["severe eye pain"],
            "variations": [
                "I have had severe throbbing eye pain with blurred vision, seeing colored halos around lights, and nausea for 3 hours.",
                "Intense pain in right eye, eyeball feels hard and throbbing, seeing rainbow rings around light bulbs, nauseous.",
                "Excruciating right eye ache, blurred vision, cloudy cornea, seeing halos, vomiting from pain.",
                "Sudden severe pain in left eye, redness, blurred sight, colored halos around streetlights, feeling sick.",
                "Severe ocular agony, eye is bloodshot, hazy vision, throbbing temple headache and nausea.",
                "Intense right eyeball pain, cannot open eye, seeing halos around lamps, blurred vision since 4 hours.",
                "Acute red eye with severe deep pain, nausea, vomiting, seeing colored circles around light sources.",
                "Throbbing right eye pain, decreased vision, halos around ceiling lights, severe headache and queasiness.",
            ],
            "adversarial": [
                "Severe throbbing eye pain with halos, no body fever, no cough, no chest tightness.",
            ]
        },
        {
            "id": "FAM-L2-AMS-13",
            "level": "Level 2",
            "red_flags": ["altered_mental_status_with_headache"],
            "expected_symptoms": ["headache", "vomiting", "altered mental status"],
            "rationale": "Severe headache accompanied by altered mental status, persistent emesis, or lethargy warrants urgent neuro-evaluation per AIIMS guidelines.",
            "provenance": "AIIMS Clinical Neurology Triage Guidelines",
            "primary_symptoms": ["headache", "vomiting", "altered mental status"],
            "variations": [
                "My hedache is horible and im throwin up since 2 days, feeling verry drowzy.",
                "Severe throbbing headache for 2 days with repeated vomiting, disoriented and unable to stay awake.",
                "Horrible headache and throwing up since yesterday, extremely drowsy, speaking slowly and confused.",
                "Severe headache with continuous nausea and vomiting, feeling very lethargic, difficult to wake up.",
                "Patient has intense pounding headache, vomited 4 times today, disoriented to time and very sleepy.",
                "Debilitating headache for 36 hours, vomiting bile, extreme drowsiness and mild confusion.",
                "Horrible migraine-like pain, vomited multiple times, drifting into sleep constantly, acting confused.",
                "Severe headache and throwing up for 2 days, feeling heavily drowsy, family noticed confusion.",
            ],
            "adversarial": [
                "Horrible headache and throwing up for 2 days, very drowsy. No chest pain, no limb paralysis.",
            ]
        },

        # ==========================================
        # LEVEL 3 — ROUTINE MEDICAL CONSULTATION (INDIA)
        # ==========================================
        {
            "id": "FAM-L3-COUGH-14",
            "level": "Level 3",
            "red_flags": [],
            "expected_symptoms": ["cough"],
            "expected_negated": ["shortness of breath", "chest pain"],
            "rationale": "Subacute productive cough > 7 days without dyspnea, hemoptysis, or chest pain requires routine primary care review and evaluation per MoHFW guidelines.",
            "provenance": "MoHFW Standard Treatment Guidelines (STG) for Respiratory Infections (NTEP)",
            "primary_symptoms": ["cough"],
            "variations": [
                "Persistent cough with thick green phlegm for 8 days, low grade fever of 99.8F, mild fatigue, but no shortness of breath and no chest discomfort.",
                "Hacking productive cough for 9 days bringing up yellowish mucus, mild chest tickle, but breathing normally and no pain.",
                "Coughing up thick mucus for over a week, low fever, tired, no shortness of breath and no chest tightness.",
                "Wet cough lasting 10 days after viral cold, chest sounds congested, but breathing feels comfortable and no severe pain.",
                "Persistent cough for 8 days, clears throat often with yellow sputum, mild fatigue, no wheezing or chest pain.",
                "Coughing with yellow phlegm for 2 weeks, low-grade temperature 99.5F, no breathing trouble and no chest pain.",
                "Subacute productive cough for 11 days, throat clearing, eating fine, no dyspnea and no severe symptoms.",
                "Cough has lasted 8 days, coughing bouts in morning, phlegm present, no shortness of breath and no fever.",
            ],
            "adversarial": [
                "Persistent cough with green phlegm for 10 days, denies chest pain, denies shortness of breath, denies high fever.",
            ]
        },
        {
            "id": "FAM-L3-RASH-15",
            "level": "Level 3",
            "red_flags": [],
            "expected_symptoms": ["rash"],
            "expected_negated": ["fever", "trouble breathing"],
            "rationale": "Localized pruritic skin rash without mucosal compromise, fever, or respiratory symptoms is suitable for routine outpatient review per MoHFW STG.",
            "provenance": "MoHFW Standard Treatment Guidelines in Dermatology (India)",
            "primary_symptoms": ["rash"],
            "variations": [
                "I have had an itchy red rash spread across both arms for the last 5 days. It is mildly uncomfortable, but no fever, no swelling, and no trouble breathing.",
                "Red bumpy itchy rash on forearms and thighs for 4 days, bothersome itching, but no facial swelling and no fever.",
                "Dry red itchy patches on both elbows and knees for a week, scratching constantly, no fever and feeling fine.",
                "Pruritic red rash on chest and abdomen for 5 days, mildly itchy, no throat tightness, no fever, no difficulty breathing.",
                "Itchy red bumps on wrists and hands for 6 days, no fever, no swelling of lips, normal breathing.",
                "Skin rash with mild itching on both legs for 5 days, red spots, no pain, no fever, no allergic symptoms.",
                "Red itchy eczema-like flare on arms for 6 days, calamine lotion not helping, no fever and no facial swelling.",
                "Bothersome itchy rash across torso for 5 days, red blemishes, no systemic symptoms, no breathing trouble.",
            ],
            "adversarial": [
                "Itchy red rash for 5 days. I do NOT have breathing difficulty, no throat swelling, and no chest pain.",
            ]
        },
        {
            "id": "FAM-L3-UTI-16",
            "level": "Level 3",
            "red_flags": [],
            "expected_symptoms": ["dysuria"],
            "expected_negated": ["back pain", "fever"],
            "rationale": "Uncomplicated dysuria and urinary frequency without flank pain, high fever, or hematuria represents uncomplicated lower UTI per MoHFW STG.",
            "provenance": "MoHFW Standard Treatment Guidelines for Urinary Tract Infections (India)",
            "primary_symptoms": ["dysuria"],
            "variations": [
                "Burning sensation during urination for the past 3 days and having to pee much more frequently. No back pain, no fever, no blood in urine.",
                "Painful stinging when I pee for 3 days, urinating every hour, mild lower bladder pressure, but no fever and no flank ache.",
                "Dysuria and urinary urgency since 2 days, burning sensation, no backache, no chills, no fever.",
                "Stinging sensation every time I urinate for 3 days, frequent trips to washroom, no blood and no high temperature.",
                "Burning during urination and constant urge to pee for 4 days, no fever, no vomiting, no flank pain.",
                "Painful urination for 3 days, going to restroom frequently with burning feeling, normal appetite and no fever.",
                "Burning sensation when peeing and mild pelvic discomfort for 3 days, no fever, no back pain, no blood.",
                "Urinating frequently with stinging discomfort for 72 hours, no systemic illness, no nausea, no fever.",
            ],
            "adversarial": [
                "Burning sensation during urination for 3 days. Denies back pain, denies fever, denies chills.",
            ]
        },
        {
            "id": "FAM-L3-BACK-17",
            "level": "Level 3",
            "red_flags": [],
            "expected_symptoms": ["back pain"],
            "expected_negated": ["numbness", "incontinence"],
            "rationale": "Mechanical lower back pain following lifting or desk work without cauda equina signs, motor deficit, or bladder changes per ICMR guidelines.",
            "provenance": "ICMR Musculoskeletal Clinical Management Guidelines",
            "primary_symptoms": ["back pain"],
            "variations": [
                "Dull ache in my lower back for 2 weeks after moving heavy furniture. Pain is worse with bending, but no numbness, no leg weakness, and normal bowel/bladder control.",
                "Lower back stiffness and ache for 10 days after gardening, hurts when standing up, no tingling in legs and normal bladder control.",
                "Persistent dull lower back pain for 2 weeks, muscular ache, no numbness in feet, no loss of bowel or bladder control.",
                "Aching lumbar spine pain for 12 days after lifting heavy luggage, relieved by lying down, no weakness and no incontinence.",
                "Lower back strain lasting 2 weeks, stiffness in morning, no numbness in groin area, bowel and bladder completely normal.",
                "Dull aching low back pain for 14 days, tight muscles, no shooting pain down legs, no weakness and no numbness.",
                "Backache across lower lumbar region for 2 weeks, worse after long scooter commute, no bowel or bladder changes, no leg tingling.",
                "Mechanical lower back pain for 10 days, uncomfortable when twisting, no leg numbness, no fever, normal urination.",
            ],
            "adversarial": [
                "Lower back pain for 2 weeks. Denies numbness, denies leg weakness, denies chest pain.",
            ]
        },
        {
            "id": "FAM-L3-MIGRAINE-18",
            "level": "Level 3",
            "red_flags": [],
            "expected_symptoms": ["headache", "nausea"],
            "expected_negated": [],
            "rationale": "Uncomplicated recurrent migraine headache with photophobia and nausea without thunderclap onset or focal neurological signs.",
            "provenance": "AIIMS Headache Clinic Clinical Protocol",
            "primary_symptoms": ["headache", "nausea"],
            "variations": [
                "Throbbing headache on one side of my head for 6 hours, sensitive to light and mild nausea. I have had these migraines before.",
                "Pounding headache on right temple for 8 hours, bright light bothers eyes, mild nausea, typical migraine pattern.",
                "Moderate throbbing headache since this morning, nausea, sensitive to loud sounds and bright sunlight, had similar episodes in past.",
                "One-sided head pounding for 6 hours, queasy stomach, resting in dark quiet bedroom, no sudden explosion and no stiff neck.",
                "Throbbing migraine headache on left temple for 7 hours, mild nausea, light sensitivity, gradual onset.",
                "Pounding headache on right side for 6 hours, feels like past migraines, slight nausea, no fever and no weakness.",
                "Familiar throbbing headache on left side since morning, mild nausea, photophobia, no thunderclap onset.",
                "Recurrent migraine headache for 8 hours, moderate throbbing, mild nausea, no neck rigidity and no speech issues.",
            ],
            "adversarial": [
                "Throbbing headache on one side of head for 6 hours. No sudden explosion, no stiff neck, no chest pain.",
            ]
        },
        {
            "id": "FAM-L3-MULTI-19",
            "level": "Level 3",
            "red_flags": [],
            "expected_symptoms": ["headache", "vomiting"],
            "expected_negated": [],
            "rationale": "Subacute headache followed by single or mild vomiting without fever, sudden thunderclap onset, or neurological deficit per MoHFW guidelines.",
            "provenance": "MoHFW Primary Health Centre Clinical Triage Guidelines",
            "primary_symptoms": ["headache", "vomiting"],
            "variations": [
                "I have had a mild headache since yesterday, and today I started vomiting.",
                "Mild headache began yesterday afternoon, and I threw up once this morning, feeling somewhat nauseous.",
                "Moderate headache for 24 hours followed by an episode of vomiting today, resting in bed, no fever.",
                "Head ache since yesterday and threw up breakfast today, feeling queasy, no stiff neck and no confusion.",
                "Had a dull headache since yesterday and started vomiting today, no fever, no blurred vision.",
                "Mild head pounding since yesterday, threw up earlier today, resting with fluids, no severe red flags.",
                "Headache started yesterday and today I vomited once, feeling tired and queasy, no neck stiffness.",
                "Mild headache for 1 day, threw up once today, drinking water slowly, no sudden severe pain.",
            ],
            "adversarial": [
                "Mild headache since yesterday and started vomiting today. No chest pain, no shortness of breath, no weakness.",
            ]
        },

        # ==========================================
        # LEVEL 4 — SELF-CARE / MONITORING (INDIA)
        # ==========================================
        {
            "id": "FAM-L4-COLD-20",
            "level": "Level 4",
            "red_flags": [],
            "expected_symptoms": ["runny nose", "sneezing"],
            "expected_negated": ["fever", "sore throat"],
            "rationale": "Acute mild upper respiratory viral prodrome with rhinorrhea and sneezing without fever or dyspnea; supportive home care indicated per MoHFW guidelines.",
            "provenance": "MoHFW Common Cold & Seasonal Viral Management Guidelines",
            "primary_symptoms": ["runny nose", "sneezing"],
            "variations": [
                "Mild runny nose, sneezing, and clear nasal discharge for 2 days. Feeling slightly tired but no fever, no sore throat, eating and drinking fine.",
                "Sniffles and occasional sneezing since yesterday, clear mucus, no fever, no body aches, normal appetite.",
                "Mild runny nose and sneezing for 2 days, slight tiredness, drinking plenty of warm water, no fever and no cough.",
                "Stuffy nose and frequent sneezing for 48 hours, clear drainage, no temperature, eating normally.",
                "Mild cold symptoms for 2 days, sneezing, clear runny nose, feeling a little run down but no fever.",
                "Runny nose and sneezing for 3 days, clear discharge, no fever, no difficulty breathing, taking steam inhalation at home.",
                "Slight nasal drip and sneezing since yesterday, drinking herbal ginger tea, no sore throat, no fever, active during day.",
                "Mild sneezing and runny nose for 2 days, no chills, no fever, no chest pain, sleeping well.",
            ],
            "adversarial": [
                "Mild runny nose and sneezing for 2 days. I do not have a fever and do not have breathing trouble.",
            ]
        },
        {
            "id": "FAM-L4-DOMS-21",
            "level": "Level 4",
            "red_flags": [],
            "expected_symptoms": ["muscle soreness"],
            "expected_negated": [],
            "rationale": "Delayed onset muscle soreness (DOMS) after unaccustomed physical exertion; benign self-resolving physiology.",
            "provenance": "Sports Authority of India Clinical Sports Medicine Protocol",
            "primary_symptoms": ["muscle soreness"],
            "variations": [
                "Mild muscle soreness in my thighs and calves today after playing cricket yesterday after not exercising for months.",
                "Sore quadriceps and calves today after lifting weights yesterday, stiff when standing up, normal clear urine color.",
                "Mild generalized muscle ache after helping a relative shift house yesterday, full mobility, drinking water.",
                "Calves and thighs are stiff and sore 24 hours after workout at gym, no swelling, no trauma, resolving with rest.",
                "Mild muscle soreness in arms and shoulders after first day back at badminton, full range of motion, no bruising.",
                "Leg muscles feel sore and tight today following long walk over weekend, normal urine, resting at home.",
                "Muscles aching pleasantly in hamstrings after morning yoga session yesterday, mild stiffness, stretching helps.",
                "Sore shoulder muscles today after swimming laps yesterday, mild ache, no joint swelling, no fever.",
            ],
            "adversarial": [
                "Mild muscle soreness in thighs after running. No chest pain, no shortness of breath, no dizziness.",
            ]
        },
        {
            "id": "FAM-L4-CUT-22",
            "level": "Level 4",
            "red_flags": [],
            "expected_symptoms": ["minor laceration"],
            "expected_negated": [],
            "rationale": "Superficial minor skin abrasion or cut with bleeding arrested immediately; first-aid cleansing and clean dressing indicated.",
            "provenance": "Indian Red Cross Society First Aid Manual",
            "primary_symptoms": ["minor laceration"],
            "variations": [
                "Small superficial paper cut on index finger, washed it with soap and water, tiny drop of blood stopped immediately, minor stinging.",
                "Tiny superficial scratch on forearm from rose thorn, washed with clean water, stopped bleeding right away, minor sting.",
                "Minor paper cut on thumb, bleeding halted in 30 seconds, clean band-aid applied, no swelling.",
                "Superficial small scrape on knuckle, barely bled, cleaned with antiseptic liquid, no redness or infection.",
                "Tiny surface scratch on finger from cardboard box, washed thoroughly, no bleeding, minor irritation.",
                "Minor superficial nick on finger while chopping vegetables, bled one drop then stopped, clean bandage placed.",
                "Small surface scrape on knee from rug, minor redness, washed with soap, bleeding stopped completely.",
                "Tiny paper cut on pointer finger, minor stinging when washing hands, no foreign body, clean and dry.",
            ],
            "adversarial": [
                "Small superficial paper cut on finger. Denies bleeding, denies fever, denies infection.",
            ]
        },
        {
            "id": "FAM-L4-THIRST-23",
            "level": "Level 4",
            "red_flags": [],
            "expected_symptoms": ["mild thirst"],
            "expected_negated": [],
            "rationale": "Transient mild thirst and dry mouth responding promptly to oral hydration without systemic or metabolic red flags.",
            "provenance": "National Oral Rehydration Programme (MoHFW, Govt. of India)",
            "primary_symptoms": ["mild thirst"],
            "variations": [
                "Mild dry mouth and mild thirst after working in the garden on a warm afternoon. Drank two glasses of water and feeling much better.",
                "Slightly thirsty and dry lips after walking in the afternoon sun for an hour, drank a glass of nimbu pani, feeling refreshed.",
                "Mild thirst after yard work today, drank water and rested, no dizziness, no fever, feeling normal.",
                "Dry mouth and thirsty after sitting in air conditioning for long hours, drank two cups of water and symptom completely resolved.",
                "Mild thirst after afternoon market walk, had a glass of coconut water, no nausea, no headache, feeling well.",
                "Feeling slightly thirsty after morning walk, rehydrated with water, normal energy levels.",
                "Mild dry throat and thirst after cleaning house, drank water, throat feels fine now, no fever.",
                "Thirsty after mild exercise in warm weather, drank water, feeling completely back to normal.",
            ],
            "adversarial": [
                "Mild dry mouth and thirst after working outside. Denies chest pain, denies shortness of breath, denies confusion.",
            ]
        },
        {
            "id": "FAM-L4-NEG-CHEST-24",
            "level": "Level 4",
            "red_flags": [],
            "expected_symptoms": ["nausea"],
            "expected_negated": ["chest pain", "difficulty breathing"],
            "rationale": "Adversarial test for negation: explicit denial of chest pain and dyspnea must not trigger Level 1 emergency; mild isolated nausea after food is self-limiting.",
            "provenance": "Synthetic adversarial case for negation extraction (India)",
            "primary_symptoms": ["nausea"],
            "variations": [
                "I do NOT have any chest pain, and I do not have difficulty breathing. Just feeling slightly nauseous after eating leftover street food 2 hours ago.",
                "No chest pain and no shortness of breath whatsoever. Just a tiny bit of nausea after spicy oily dinner.",
                "I definitely do not have chest pain and am not short of breath. Only mild queasiness after heavy lunch.",
                "Zero chest discomfort and no trouble breathing. Feeling slightly sick to my stomach after rich samosa.",
                "I deny chest pain and deny shortness of breath. Just mild stomach upset 2 hours after dinner.",
                "Negative for chest pain and negative for breathing problems. Just slight nausea after eating sour curd.",
                "Without chest pain and without breathlessness. Feeling slightly queasy after eating too fast.",
                "I do not have chest pain or breathing issues. Just a little nausea after drinking cold milk.",
            ],
            "adversarial": [
                "I do NOT have any chest pain, and I do not have difficulty breathing. No vomiting, no fever, just mild nausea.",
            ]
        },
        {
            "id": "FAM-L4-HISTORICAL-25",
            "level": "Level 4",
            "red_flags": [],
            "expected_symptoms": ["sore throat"],
            "expected_negated": [],
            "rationale": "Temporal filtering test: historical pneumonia resolved years ago must not trigger acute respiratory triage; acute symptom is isolated mild throat tickle.",
            "provenance": "Synthetic test case for temporal and historical mention filtering (India)",
            "primary_symptoms": ["sore throat"],
            "variations": [
                "Five years ago I had pneumonia. Currently, I just have a mild scratchy throat since this morning.",
                "I had pneumonia back in 2018 that resolved completely. Right now I only have a minor scratchy throat for a few hours.",
                "History of pneumonia 4 years ago. Today I just have a slight throat tickle, drinking warm water.",
                "Years ago I was treated for pneumonia. Currently only have a mild throat irritation since waking up.",
                "Had pneumonia as a child. Present symptoms are only a very mild scratchy throat, eating normally.",
                "Resolved pneumonia three years ago. Currently I just feel a mild scratchy sensation in throat.",
                "Previously had pneumonia in the past. Today only experiencing a slight throat tickle, no fever.",
                "Past history of pneumonia 6 years ago. Right now just a minor scratchy throat, no breathing trouble.",
            ],
            "adversarial": [
                "Five years ago I had pneumonia. Currently I do not have breathing trouble, just a mild scratchy throat.",
            ]
        },
        {
            "id": "FAM-L4-THIRDPARTY-26",
            "level": "Level 4",
            "red_flags": [],
            "expected_symptoms": ["runny nose", "sneezing"],
            "expected_negated": [],
            "rationale": "Third-party discrimination: family member's past cardiac history must not escalate patient's personal mild common cold.",
            "provenance": "Synthetic test case for third-party context discrimination (India)",
            "primary_symptoms": ["runny nose", "sneezing"],
            "variations": [
                "My father had a heart attack last year so I am worried, but I personally only have a mild runny nose and sneezing.",
                "My mother had cardiac issues two years ago, but for myself I just have a clear runny nose and sniffles for 2 days.",
                "Worried because my grandfather had heart disease, but my only personal symptom is a mild runny nose and sneezing.",
                "Family history of heart attack in my father, but I personally only have a slight runny nose and sneezing today.",
                "My uncle suffered a heart attack last summer, but I only have a mild runny nose and occasional sneeze.",
                "My brother had cardiac issues previously, but I personally just have mild sniffles and sneezing for 2 days.",
                "Worried due to father's cardiac stent last year, though I only have a minor runny nose, no chest pain.",
                "My grandfather passed away from heart attack, but my current symptom is just a mild runny nose and sneezing.",
            ],
            "adversarial": [
                "My father had a cardiac arrest last year, but I personally do not have chest pain, only a mild runny nose.",
            ]
        },
        {
            "id": "FAM-L4-UNCERTAIN-27",
            "level": "Level 4",
            "red_flags": [],
            "expected_symptoms": ["dizziness"],
            "expected_negated": ["chest pain", "weakness"],
            "rationale": "Uncertain, resolved mention with explicit denial of neurological and cardiac warning signs; self-care and monitoring.",
            "provenance": "Synthetic test case for uncertain mention and denial verification (India)",
            "primary_symptoms": ["dizziness"],
            "variations": [
                "Maybe I felt slightly dizzy yesterday or maybe it was just being tired, not sure. No chest pain, no weakness, no fainting.",
                "Not sure if I felt a little dizzy yesterday afternoon or just stood up fast. Feeling completely fine today, no chest pain.",
                "Perhaps I felt slightly off balance yesterday for 5 seconds after not eating lunch. No weakness, no fainting, normal today.",
                "Might have been slightly dizzy yesterday, or maybe just sleepy. No chest pain, no shortness of breath, fully recovered.",
                "Felt kind of weird and dizzy for a moment yesterday in the heat, not sure. Completely resolved now, no chest pain, no weakness.",
                "Maybe slight dizziness yesterday after looking at computer screen, gone now. No chest discomfort, no fainting.",
                "Not certain if I felt dizzy yesterday or just dehydrated. Drank water and feel 100% fine now, no weakness.",
                "Perhaps momentary dizziness yesterday after skipping breakfast. Denies chest pain, denies fainting, completely normal today.",
            ],
            "adversarial": [
                "Maybe I felt slightly dizzy yesterday, not sure. I do NOT have chest pain, no weakness, no fainting.",
            ]
        }
    ]

    # Split assignment by COMPLETE TEMPLATE FAMILY:
    FAMILY_SPLIT_MAP = {
        # Level 1 (5 Train, 1 Val, 1 Test)
        "FAM-L1-ACS-01": "train",
        "FAM-L1-STROKE-02": "train",
        "FAM-L1-RESP-03": "train",
        "FAM-L1-UNRESP-04": "train",
        "FAM-L1-BLEED-05": "train",
        "FAM-L1-ANAPHYLAXIS-06": "val",
        "FAM-L1-THUNDERCLAP-07": "test",

        # Level 2 (4 Train, 1 Val, 1 Test)
        "FAM-L2-APPEN-08": "train",
        "FAM-L2-PED-FEVER-09": "train",
        "FAM-L2-DVT-10": "train",
        "FAM-L2-MENING-11": "train",
        "FAM-L2-EYE-12": "val",
        "FAM-L2-AMS-13": "test",

        # Level 3 (4 Train, 1 Val, 1 Test)
        "FAM-L3-COUGH-14": "train",
        "FAM-L3-RASH-15": "train",
        "FAM-L3-UTI-16": "train",
        "FAM-L3-BACK-17": "train",
        "FAM-L3-MIGRAINE-18": "val",
        "FAM-L3-MULTI-19": "test",

        # Level 4 (5 Train, 1 Val, 1 Test)
        "FAM-L4-COLD-20": "train",
        "FAM-L4-DOMS-21": "train",
        "FAM-L4-CUT-22": "train",
        "FAM-L4-THIRST-23": "train",
        "FAM-L4-NEG-CHEST-24": "train",
        "FAM-L4-HISTORICAL-25": "train",
        "FAM-L4-THIRDPARTY-26": "val",
        "FAM-L4-UNCERTAIN-27": "test",
    }

    # Verify zero family overlap constraint
    train_fams = {f for f, s in FAMILY_SPLIT_MAP.items() if s == "train"}
    val_fams = {f for f, s in FAMILY_SPLIT_MAP.items() if s == "val"}
    test_fams = {f for f, s in FAMILY_SPLIT_MAP.items() if s == "test"}

    assert train_fams.isdisjoint(val_fams), "Train and Val families overlap!"
    assert train_fams.isdisjoint(test_fams), "Train and Test families overlap!"
    assert val_fams.isdisjoint(test_fams), "Val and Test families overlap!"

    # Lexical variation components for diverse generation
    AGE_GROUPS = ["adult", "adult", "adult", "elderly", "child", "infant", "unknown"]
    SEVERITIES = ["mild", "moderate", "severe", "unknown"]
    DURATIONS = [
        "15 minutes", "30 minutes", "1 hour", "past 45 minutes",
        "since yesterday", "24 hours", "2 days", "3 days", "5 days",
        "1 week", "2 weeks", "unknown"
    ]

    INTROS = [
        "", "Namaste doctor, ", "Please advise, ", "I am writing because ",
        "For context: ", "Starting earlier today, ", "Currently, ", "Notice: "
    ]
    OUTROS = [
        "", " What should I do?", " Should I seek medical attention?",
        " Looking for guidance.", " Please help me understand.", " Waiting for advice."
    ]

    # Pre-calculated distribution target per split to reach exactly target_count (1,000)
    SPLIT_TARGETS = {
        "train": 700,
        "val": 150,
        "test": 150
    }

    cases_by_split: Dict[str, List[Dict[str, Any]]] = {"train": [], "val": [], "test": []}
    all_cases: List[Dict[str, Any]] = []
    seen_texts = set()

    case_counter = 1

    # Generate cases by split according to targets
    for split_name, target in SPLIT_TARGETS.items():
        split_families = [f for f in FAMILIES if FAMILY_SPLIT_MAP[f["id"]] == split_name]
        family_cycle = 0

        while len(cases_by_split[split_name]) < target:
            fam = split_families[family_cycle % len(split_families)]
            family_cycle += 1

            # Pick base text
            all_pool = fam["variations"] + fam.get("adversarial", [])
            base_text = rng.choice(all_pool)

            # Slot filling & perturbation to ensure uniqueness
            intro = rng.choice(INTROS)
            outro = rng.choice(OUTROS)
            
            # Select age group appropriate for family
            if "PED" in fam["id"]:
                age = rng.choice(["infant", "child"])
            elif "STROKE" in fam["id"] or "DVT" in fam["id"]:
                age = rng.choice(["elderly", "adult"])
            else:
                age = rng.choice(AGE_GROUPS)

            # Select severity appropriate for level
            if fam["level"] == "Level 1":
                sev = rng.choice(["severe", "severe", "moderate"])
                dur = rng.choice(["10 minutes", "20 minutes", "45 minutes", "1 hour", "2 hours", "unknown"])
            elif fam["level"] == "Level 2":
                sev = rng.choice(["severe", "moderate", "moderate"])
                dur = rng.choice(["3 hours", "8 hours", "1 day", "2 days", "3 days", "unknown"])
            elif fam["level"] == "Level 3":
                sev = rng.choice(["moderate", "mild", "unknown"])
                dur = rng.choice(["3 days", "5 days", "1 week", "2 weeks", "unknown"])
            else:
                sev = rng.choice(["mild", "mild", "unknown"])
                dur = rng.choice(["1 hour", "2 days", "3 days", "yesterday", "unknown"])

            # Formulate final text
            full_text = f"{intro}{base_text}{outro}".strip()

            # Prevent text duplicates
            if full_text in seen_texts:
                full_text = f"{full_text} (Duration: {dur}, Severity: {sev})"

            if full_text in seen_texts:
                continue

            seen_texts.add(full_text)

            case_id = f"SYNTH-{case_counter:04d}"
            case_counter += 1

            case_obj = {
                "case_id": case_id,
                "template_family_id": fam["id"],
                "split": split_name,
                "text": full_text,
                "age_group": age,
                "duration": dur,
                "severity": sev,
                "reference_triage_category": fam["level"],
                "expected_red_flags": fam.get("red_flags", []),
                "expected_symptoms": fam.get("expected_symptoms", fam.get("primary_symptoms", [])),
                "expected_negated": fam.get("expected_negated", []),
                "rationale": fam["rationale"],
                "provenance": f"{fam['provenance']} | Template: {fam['id']}",
                "is_synthetic": True
            }

            cases_by_split[split_name].append(case_obj)
            all_cases.append(case_obj)

    # Sort all cases by ID
    all_cases.sort(key=lambda c: c["case_id"])
    assert len(all_cases) == target_count, f"Generated {len(all_cases)} cases, expected {target_count}"
    assert len(seen_texts) == target_count, "Detected duplicate texts!"

    return all_cases, cases_by_split


def save_dataset(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    splits_dir = os.path.join(output_dir, "splits")
    os.makedirs(splits_dir, exist_ok=True)

    all_cases, cases_by_split = create_dataset(seed=42, target_count=1000)

    # 1. Save Full 1,000 cases JSON
    full_json_path = os.path.join(output_dir, "synthetic_cases_1000.json")
    with open(full_json_path, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2)

    # 2. Also update/replace default synthetic_cases.json with full 1,000 cases for immediate seamless integration
    default_json_path = os.path.join(output_dir, "synthetic_cases.json")
    with open(default_json_path, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2)

    # 3. Save Full 1,000 cases CSV
    full_csv_path = os.path.join(output_dir, "synthetic_cases_1000.csv")
    with open(full_csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "case_id", "template_family_id", "split", "text", "age_group",
            "duration", "severity", "reference_triage_category", "rationale",
            "provenance", "is_synthetic"
        ])
        for c in all_cases:
            writer.writerow([
                c["case_id"], c["template_family_id"], c["split"], c["text"],
                c["age_group"], c["duration"], c["severity"],
                c["reference_triage_category"], c["rationale"],
                c["provenance"], c["is_synthetic"]
            ])

    # Default CSV
    default_csv_path = os.path.join(output_dir, "synthetic_cases.csv")
    with open(default_csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "case_id", "template_family_id", "split", "text", "age_group",
            "duration", "severity", "reference_triage_category", "rationale",
            "provenance", "is_synthetic"
        ])
        for c in all_cases:
            writer.writerow([
                c["case_id"], c["template_family_id"], c["split"], c["text"],
                c["age_group"], c["duration"], c["severity"],
                c["reference_triage_category"], c["rationale"],
                c["provenance"], c["is_synthetic"]
            ])

    # 4. Save individual split files
    for split_name in ["train", "val", "test"]:
        split_path = os.path.join(splits_dir, f"{split_name}.json")
        with open(split_path, "w", encoding="utf-8") as f:
            json.dump(cases_by_split[split_name], f, indent=2)

    # Print summary statistics
    print(f"Generated exactly {len(all_cases)} synthetic clinical cases (India context).")
    print("Split breakdown:")
    for split_name in ["train", "val", "test"]:
        cases = cases_by_split[split_name]
        counts = {}
        for c in cases:
            cat = c["reference_triage_category"]
            counts[cat] = counts.get(cat, 0) + 1
        print(f"  - {split_name.upper():<5}: {len(cases)} cases -> {counts}")

    total_counts = {}
    for c in all_cases:
        cat = c["reference_triage_category"]
        total_counts[cat] = total_counts.get(cat, 0) + 1
    print(f"Overall Class Distribution: {total_counts}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    save_dataset(out_dir)
