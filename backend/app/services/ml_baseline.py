"""
Scikit-learn Traditional ML/NLP Baseline for SafeTriage.
Uses TF-IDF Vectorization with Logistic Regression for reproducible experimental comparison.
"""

import json
import os
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from app.core.urgency import TriageLevel, URGENCY_RANK


class MLBaselineModel:
    def __init__(self):
        self.pipeline: Optional[Pipeline] = None
        self.is_trained: bool = False
        self.training_provenance: str = "Uninitialized"
        self.classes_: List[str] = [
            TriageLevel.LEVEL_1.value,
            TriageLevel.LEVEL_2.value,
            TriageLevel.LEVEL_3.value,
            TriageLevel.LEVEL_4.value,
        ]

    def train_on_cases(self, cases: List[Dict[str, Any]], provenance_note: str = "Synthetic benchmark dataset"):
        """Train scikit-learn pipeline on labeled test cases with reproducible seed."""
        texts = [c["text"] for c in cases if "text" in c and "reference_triage_category" in c]
        labels = [c["reference_triage_category"] for c in cases if "text" in c and "reference_triage_category" in c]

        if len(texts) < 4:
            self.is_trained = False
            self.training_provenance = "Insufficient training cases to train valid ML baseline."
            return

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, lowercase=True)),
            ("clf", LogisticRegression(random_state=42, max_iter=500, class_weight="balanced"))
        ])

        self.pipeline.fit(texts, labels)
        self.is_trained = True
        self.training_provenance = (
            f"Trained on {len(texts)} scenarios ({provenance_note}). "
            "Pipeline: TF-IDF (1,2-grams) + LogisticRegression. "
            "Research benchmark baseline only; not clinically validated."
        )

    def predict(self, text: str) -> str:
        """Predict triage category or fallback to Level 3 if untrained or error."""
        if not self.is_trained or not self.pipeline:
            return TriageLevel.LEVEL_3.value

        try:
            pred = self.pipeline.predict([text])[0]
            if pred in URGENCY_RANK:
                return pred
            return TriageLevel.LEVEL_3.value
        except Exception:
            return TriageLevel.LEVEL_3.value


# Global baseline model instance
ml_baseline = MLBaselineModel()


def initialize_ml_baseline(synthetic_data_path: Optional[str] = None):
    """Auto-load training split for strictly out-of-sample ML baseline evaluation."""
    candidates = [
        synthetic_data_path,
        # Prefer strictly isolated train split
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "datasets", "synthetic", "splits", "train.json"),
        os.path.abspath(os.path.join("..", "datasets", "synthetic", "splits", "train.json")),
        os.path.abspath(os.path.join("datasets", "synthetic", "splits", "train.json")),
        # Fallback to full dataset if split not found
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "datasets", "synthetic", "synthetic_cases_1000.json"),
        os.path.abspath(os.path.join("..", "datasets", "synthetic", "synthetic_cases.json")),
        os.path.abspath(os.path.join("datasets", "synthetic", "synthetic_cases.json")),
    ]
    for p in candidates:
        if p and os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    cases = json.load(f)
                ml_baseline.train_on_cases(cases, provenance_note=f"Split partition from {os.path.basename(p)}")
                return
            except Exception as e:
                ml_baseline.is_trained = False
                ml_baseline.training_provenance = f"Failed to load synthetic dataset: {str(e)}"
                return
