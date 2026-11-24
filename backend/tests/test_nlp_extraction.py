import pytest
from app.nlp.extractor import SymptomExtractor


@pytest.fixture
def extractor():
    return SymptomExtractor()


def test_positive_symptom_extraction(extractor):
    text = "I have had a headache since yesterday, and today I started vomiting."
    res = extractor.extract(text)
    assert "headache" in res.positive_symptoms
    assert "vomiting" in res.positive_symptoms
    assert len(res.negated_symptoms) == 0


def test_negation_handling(extractor):
    """'I have chest pain' vs 'I do NOT have any chest pain' must never produce the same result."""
    text_with_pain = "I have severe chest pain and cannot breathe."
    res_pos = extractor.extract(text_with_pain)
    assert "chest pain" in res_pos.positive_symptoms

    text_without_pain = "I do NOT have any chest pain, and I do not have difficulty breathing. Just mild nausea."
    res_neg = extractor.extract(text_without_pain)
    assert "chest pain" in res_neg.negated_symptoms
    assert "chest pain" not in res_neg.positive_symptoms
    assert "difficulty breathing" in res_neg.negated_symptoms
    assert "difficulty breathing" not in res_neg.positive_symptoms
    assert "nausea" in res_pos.positive_symptoms or "nausea" in res_neg.positive_symptoms


def test_historical_symptom_distinction(extractor):
    """Historical symptoms ('Five years ago I had pneumonia') must be marked as HISTORICAL, not acute."""
    text = "Five years ago I had pneumonia. Currently, I just have a mild scratchy throat since this morning."
    res = extractor.extract(text)
    assert "sore throat" in res.positive_symptoms
    assert len(res.historical_symptoms) > 0 or any(s.status == "HISTORICAL" for s in res.symptoms)


def test_third_party_symptom_distinction(extractor):
    """Mentions of family conditions ('my father had a cardiac arrest') must not trigger for the patient."""
    text = "My father had a cardiac arrest last year so I am worried, but I personally only have a mild runny nose and sneezing."
    res = extractor.extract(text)
    assert "runny nose" in res.positive_symptoms
    # Cardiac arrest or loss of consciousness must not be personal positive
    assert "loss of consciousness" not in res.positive_symptoms


def test_synonym_and_spelling_variation(extractor):
    """Tests colloquial synonyms like 'hedache', 'throwin up', 'verry drowzy'."""
    text = "My hedache is horible and im throwin up since 2 days, feeling verry drowzy."
    res = extractor.extract(text)
    assert "headache" in res.positive_symptoms
    assert "vomiting" in res.positive_symptoms
    assert "altered mental status" in res.positive_symptoms


def test_ambiguous_and_unsupported_text(extractor):
    """Text without recognized symptoms should be flagged with has_ambiguity and unsupported_terms."""
    text = "Feeling strange and off balance, things feel weird."
    res = extractor.extract(text)
    assert res.has_ambiguity is True
    assert len(res.positive_symptoms) == 0
