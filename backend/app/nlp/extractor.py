"""
Rule-based NLP Symptom Extractor with Negation, Temporal, and Third-Party Resolution.
Classifies symptoms into: POSITIVE, NEGATED, HISTORICAL, THIRD_PARTY, UNCERTAIN, and UNSUPPORTED.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field

from app.nlp.symptom_lexicon import (
    SYMPTOM_SYNONYMS,
    NEGATION_PATTERNS,
    HISTORICAL_PATTERNS,
    THIRD_PARTY_PATTERNS,
    UNCERTAINTY_PATTERNS,
    SEVERITY_KEYWORDS,
    DURATION_PATTERNS,
)


@dataclass
class ExtractedMention:
    canonical_name: str
    status: str  # POSITIVE, NEGATED, HISTORICAL, THIRD_PARTY, UNCERTAIN, UNSUPPORTED
    severity: str
    duration: str
    raw_span: str


@dataclass
class ExtractionResult:
    raw_text: str
    symptoms: List[ExtractedMention] = field(default_factory=list)
    positive_symptoms: List[str] = field(default_factory=list)
    negated_symptoms: List[str] = field(default_factory=list)
    historical_symptoms: List[str] = field(default_factory=list)
    third_party_symptoms: List[str] = field(default_factory=list)
    uncertain_symptoms: List[str] = field(default_factory=list)
    unsupported_terms: List[str] = field(default_factory=list)
    detected_severity: str = "unknown"
    detected_duration: str = "unknown"
    has_ambiguity: bool = False


class SymptomExtractor:
    def __init__(self):
        # Compile synonym regexes for efficiency
        self.compiled_synonyms: List[Tuple[str, re.Pattern]] = []
        for canonical, phrases in SYMPTOM_SYNONYMS.items():
            for phrase in phrases:
                pattern = re.compile(rf"\b{re.escape(phrase)}\b", re.IGNORECASE)
                self.compiled_synonyms.append((canonical, pattern))

        # Negation regexes
        self.compiled_negations = [re.compile(p, re.IGNORECASE) for p in NEGATION_PATTERNS]
        self.compiled_historical = [re.compile(p, re.IGNORECASE) for p in HISTORICAL_PATTERNS]
        self.compiled_third_party = [re.compile(p, re.IGNORECASE) for p in THIRD_PARTY_PATTERNS]
        self.compiled_uncertainty = [re.compile(p, re.IGNORECASE) for p in UNCERTAINTY_PATTERNS]
        self.compiled_durations = [re.compile(p, re.IGNORECASE) for p in DURATION_PATTERNS]

    def _split_clauses(self, text: str) -> List[str]:
        """Split text into sentences and sub-clauses on punctuation or coordinating conjunctions."""
        # Split on sentence boundaries and contrasting connectors like 'but', 'however'
        raw_parts = re.split(r"[\.\!\?;\n]+|\b(?:but|however|although|whereas)\b", text, flags=re.IGNORECASE)
        return [p.strip() for p in raw_parts if p.strip()]

    def extract_severity(self, text: str) -> str:
        text_lower = text.lower()
        for sev, words in SEVERITY_KEYWORDS.items():
            for w in words:
                if re.search(rf"\b{re.escape(w)}\b", text_lower):
                    return sev
        return "unknown"

    def extract_duration(self, text: str) -> str:
        for pattern in self.compiled_durations:
            match = pattern.search(text)
            if match:
                return match.group(0).strip()
        return "unknown"

    def extract(self, text: str, user_duration: Optional[str] = None, user_severity: Optional[str] = None) -> ExtractionResult:
        result = ExtractionResult(raw_text=text)
        text_clean = text.strip()
        clauses = self._split_clauses(text_clean)

        overall_severity = user_severity if user_severity and user_severity != "unknown" else self.extract_severity(text_clean)
        overall_duration = user_duration if user_duration and user_duration != "unknown" else self.extract_duration(text_clean)

        result.detected_severity = overall_severity
        result.detected_duration = overall_duration

        found_canonicals: Dict[str, ExtractedMention] = {}

        for clause in clauses:
            clause_lower = clause.lower()

            # Check clause-level flags
            has_third_party = any(p.search(clause) for p in self.compiled_third_party)
            has_historical = any(p.search(clause) for p in self.compiled_historical)
            has_uncertainty = any(p.search(clause) for p in self.compiled_uncertainty)

            # Third party family history vs active acute proxy reporting:
            # "my father had a heart attack last year" -> family history (THIRD_PARTY)
            # "my mother suddenly cannot move her arm" -> acute reporting on behalf of mother (POSITIVE)
            is_family_history = has_third_party and (
                has_historical or
                bool(re.search(r"\b(?:had|suffered|history|worried|passed away|died|years ago|last year)\b", clause_lower)) or
                bool(re.search(r"\b(?:i personally|i only|for myself)\b", text_clean.lower()))
            )

            # Check each symptom synonym in this clause
            for canonical, syn_pattern in self.compiled_synonyms:
                match = syn_pattern.search(clause)
                if match:
                    span = match.group(0)
                    start_idx = match.start()
                    prefix_text = clause_lower[:start_idx]

                    # Negation check: looks back ~40 characters before the match in the clause
                    is_neg = False
                    lookback_window = prefix_text[-40:] if len(prefix_text) > 40 else prefix_text
                    for neg_p in self.compiled_negations:
                        if neg_p.search(lookback_window):
                            is_neg = True
                            break

                    # Also check for post-negation (e.g. "chest pain: none", "chest pain negative")
                    suffix_text = clause_lower[match.end():match.end() + 20]
                    if re.search(r"\b(?:negative|none|denied|ruled out)\b", suffix_text):
                        is_neg = True

                    # Determine status
                    if is_neg:
                        status = "NEGATED"
                    elif is_family_history and not re.search(r"\b(?:i|my own|me)\b", clause_lower[start_idx:]):
                        status = "THIRD_PARTY"
                    elif has_historical:
                        status = "HISTORICAL"
                    elif has_uncertainty:
                        status = "UNCERTAIN"
                    else:
                        status = "POSITIVE"

                    mention = ExtractedMention(
                        canonical_name=canonical,
                        status=status,
                        severity=overall_severity,
                        duration=overall_duration,
                        raw_span=span
                    )

                    # Update if not found or if upgraded to POSITIVE
                    if canonical not in found_canonicals or status == "POSITIVE":
                        found_canonicals[canonical] = mention

        # Aggregate mentions
        for canonical, mention in found_canonicals.items():
            result.symptoms.append(mention)
            if mention.status == "POSITIVE":
                result.positive_symptoms.append(canonical)
            elif mention.status == "NEGATED":
                result.negated_symptoms.append(canonical)
            elif mention.status == "HISTORICAL":
                result.historical_symptoms.append(canonical)
            elif mention.status == "THIRD_PARTY":
                result.third_party_symptoms.append(canonical)
            elif mention.status == "UNCERTAIN":
                result.uncertain_symptoms.append(canonical)

        # Ambiguity / Unsupported term check:
        # If no positive symptoms were detected, or phrases contain 'weird', 'strange', 'off balance'
        if not result.positive_symptoms:
            if any(p.search(text_clean) for p in self.compiled_uncertainty) or len(text_clean.split()) > 4:
                # Capture unparsed words as unsupported
                result.has_ambiguity = True
                words = [w for w in re.findall(r"\b\w+\b", text_clean.lower()) if len(w) > 3 and w not in ["have", "been", "since", "yesterday", "feeling", "with"]]
                result.unsupported_terms = words[:5]

        return result


extractor = SymptomExtractor()
