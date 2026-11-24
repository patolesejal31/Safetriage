"""
Symptom Lexicon and Clinical Vocabulary for SafeTriage.
Contains curated canonical symptoms, common synonyms, colloquial expressions,
negation markers, historical markers, and third-party markers.
"""

from typing import Dict, List, Set

# Canonical symptoms mapped to synonyms and colloquial variations
SYMPTOM_SYNONYMS: Dict[str, List[str]] = {
    # Emergency / Red Flag symptoms
    "chest pain": [
        "chest pain", "chest tightness", "chest pressure", "crushing chest pain",
        "chest ache", "pain in chest", "heaviness in chest", "squeezing in chest",
        "angina", "sternal pain", "substernal pain", "retrosternal pain",
        "crushing pain in center of chest", "pain in center of chest", "crushing pain in chest",
        "crushing pain"
    ],
    "pneumonia": [
        "pneumonia", "lung infection", "chest infection"
    ],
    "cardiac arrest": [
        "cardiac arrest", "heart attack", "myocardial infarction"
    ],
    "pain radiating to left arm": [
        "radiating down my left arm", "pain radiating to arm", "arm radiation",
        "left arm pain", "pain spreading to jaw", "pain into my neck and arm"
    ],
    "difficulty breathing": [
        "difficulty breathing", "shortness of breath", "short of breath", "dyspnea",
        "cannot breathe", "can't breathe", "breathless", "gasping for air",
        "trouble breathing", "hard to breathe", "winded", "wheezing loudly",
        "breathing trouble", "struggling to breathe"
    ],
    "cyanosis": [
        "blue lips", "blue tint on my lips", "bluish skin", "blue fingers",
        "cyanosis", "turning blue", "blue face"
    ],
    "stroke FAST signs": [
        "cannot move her right arm", "cannot move right arm", "unilateral arm weakness",
        "arm drift", "arm weakness", "slurred speech", "garbled speech",
        "speech is slurred", "facial droop", "face drooping", "face is numb",
        "sudden numbness on one side", "stroke signs"
    ],
    "loss of consciousness": [
        "collapsed", "unresponsive", "passed out", "blacked out", "fainted",
        "syncope", "will not wake up", "loss of consciousness", "unconscious"
    ],
    "severe uncontrolled bleeding": [
        "spurting bright red blood", "bleeding will not stop", "spurting blood",
        "severe uncontrolled bleeding", "arterial hemorrhage", "heavy blood loss",
        "soaking through bandages"
    ],
    "airway swelling": [
        "throat is swelling shut", "throat swelling", "swollen tongue",
        "swollen lips", "difficulty swallowing and breathing", "stridor",
        "angioedema", "throat closing"
    ],
    "thunderclap headache": [
        "worst headache of my entire life", "worst headache of my life",
        "thunderclap headache", "sudden severe explosion in head",
        "explosive headache", "thunderclap inside my skull"
    ],

    # Urgent symptoms (Level 2)
    "acute abdominal pain": [
        "severe sharp pain in the lower right abdomen", "lower right abdominal pain",
        "sharp abdominal pain", "severe stomach pain", "severe belly pain",
        "intense abdominal cramps", "right lower quadrant pain", "acute abdomen"
    ],
    "high fever": [
        "high fever", "fever of 102", "fever of 103", "fever of 104", "102f", "103f",
        "102.5f", "104f", "very high fever", "burning up with fever"
    ],
    "fever": [
        "fever", "feverish", "high temperature", "chills", "febrile", "hot to touch"
    ],
    "neck stiffness": [
        "stiff neck", "neck stiffness", "cannot bend neck", "nuchal rigidity",
        "painful to touch chin to chest"
    ],
    "unilateral calf swelling": [
        "swollen and very red, warm calf", "swollen calf", "calf redness", "calf warmth",
        "painful to walk on calf", "calf pain after flight", "deep vein thrombosis signs"
    ],
    "severe eye pain": [
        "severe throbbing eye pain", "severe eye pain", "eye pain with blurred vision",
        "seeing colored halos", "halos around lights", "acute eye redness and pain"
    ],
    "altered mental status": [
        "confusion", "feeling very drowsy", "fruity breath odor", "delirium",
        "disoriented", "verry drowzy", "extreme lethargy"
    ],

    # Routine symptoms (Level 3)
    "headache": [
        "headache", "head ache", "hedache", "head pounding", "throbbing headache",
        "migraine", "temple pain", "tension headache"
    ],
    "vomiting": [
        "vomiting", "throwing up", "throwin up", "emesis", "threw up", "puking"
    ],
    "nausea": [
        "nausea", "nauseous", "feeling sick", "queasy", "upset stomach"
    ],
    "cough": [
        "cough", "coughing", "persistent cough", "productive cough", "hacking cough",
        "dry cough", "phlegm", "green phlegm", "yellow mucus"
    ],
    "sore throat": [
        "sore throat", "throat pain", "scratchy throat", "painful swallowing", "pharyngitis"
    ],
    "rash": [
        "rash", "itchy rash", "itchy red rash", "hives", "urticaria", "skin redness",
        "eczema flare", "pruritus"
    ],
    "dysuria": [
        "burning during urination", "burning sensation during urination", "painful urination",
        "dysuria", "stinging when peeing", "burning when I pee", "urinary frequency"
    ],
    "back pain": [
        "back pain", "lower back pain", "dull ache in my lower back", "lumbar pain",
        "back strain", "back ache"
    ],
    "earache": [
        "ear pain", "earache", "ear ache", "pain in ear", "throbbing ear"
    ],
    "joint pain": [
        "joint pain", "swollen joint", "arthralgia", "knee pain", "wrist pain"
    ],

    # Self-care symptoms (Level 4)
    "runny nose": [
        "runny nose", "sneezing", "nasal congestion", "stuffy nose", "clear nasal discharge",
        "rhinorrhea", "sniffles"
    ],
    "mild fatigue": [
        "mild fatigue", "feeling tired", "slightly tired", "low energy", "fatigue"
    ],
    "muscle soreness": [
        "mild muscle soreness", "muscle ache after exercise", "muscle soreness",
        "sore calves", "doms", "stiff muscles after workout"
    ],
    "minor laceration": [
        "paper cut", "small superficial paper cut", "minor scratch", "minor scrape",
        "small cut"
    ],
    "mild thirst": [
        "mild thirst", "dry mouth", "feeling thirsty"
    ]
}

# Negation prefix markers
NEGATION_PATTERNS = [
    r"\bno\b",
    r"\bnot\b",
    r"\bdo not have\b",
    r"\bdon't have\b",
    r"\bdoes not have\b",
    r"\bdoesn't have\b",
    r"\bdenies\b",
    r"\bdenying\b",
    r"\bwithout\b",
    r"\bfree of\b",
    r"\bnegative for\b",
    r"\bnever had\b",
    r"\brule out\b",
    r"\bneither\b",
    r"\bnor\b",
]

# Historical markers (resolved or past conditions)
HISTORICAL_PATTERNS = [
    r"\byears ago\b",
    r"\bmonths ago\b",
    r"\bas a child\b",
    r"\bin the past\b",
    r"\bhistory of\b",
    r"\bpreviously had\b",
    r"\bused to have\b",
    r"\bresolved\b",
    r"\bfive years ago\b",
    r"\b10 years ago\b"
]

# Third-party context markers (family, acquaintance)
THIRD_PARTY_PATTERNS = [
    r"\bmy father\b",
    r"\bmy mother\b",
    r"\bmy brother\b",
    r"\bmy sister\b",
    r"\bmy grandfather\b",
    r"\bmy grandmother\b",
    r"\bmy friend\b",
    r"\bmy coworker\b",
    r"\bmy uncle\b",
    r"\bmy aunt\b",
    r"\bmy cousin\b",
]

# Uncertainty qualifiers
UNCERTAINTY_PATTERNS = [
    r"\bmaybe\b",
    r"\bperhaps\b",
    r"\bpossibly\b",
    r"\bnot sure\b",
    r"\bnot certain\b",
    r"\bmight be\b",
    r"\bfeels kind of\b",
    r"\bweird\b",
    r"\bstrange\b",
    r"\boff balance\b",
]

# Severity keywords
SEVERITY_KEYWORDS = {
    "severe": ["severe", "crushing", "unbearable", "excruciating", "horrible", "intense", "worst", "10/10", "agony"],
    "moderate": ["moderate", "medium", "somewhat", "bothersome", "throbbing", "persistent", "uncomfortable"],
    "mild": ["mild", "slight", "minor", "subtle", "little bit", "scratchy", "light"]
}

# Duration regex patterns
DURATION_PATTERNS = [
    r"\b\d+\s*(?:minute|min|hour|hr|day|week|month)s?\b",
    r"\bsince\s+(?:yesterday|morning|this morning|last night|today)\b",
    r"\bpast\s+\d+\s*(?:minute|min|hour|hr|day|week)s?\b",
    r"\bfor\s+\d+\s*(?:minute|min|hour|hr|day|week)s?\b",
]
