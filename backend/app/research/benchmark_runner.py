"""
Benchmark Runner for Comparative Research Evaluation in SafeTriage.
Executes batch evaluations across:
A. Rule-Based Baseline
B. Traditional ML/NLP Baseline (Scikit-learn)
C. LLM-Only Baseline (Controlled experimental benchmark)
D. Proposed SafeTriage Hybrid Model
"""

import json
import os
import time
import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.urgency import (
    TriageLevel,
    URGENCY_RANK,
    is_less_urgent,
    is_more_urgent,
    enforce_safety_invariant,
)
from app.nlp.extractor import extractor
from app.triage.safety_engine import safety_engine
from app.services.ml_baseline import ml_baseline, initialize_ml_baseline
from app.services.llm_provider import get_llm_provider
from app.research.evaluator import calculate_evaluation_metrics
from app.models.evaluation import EvaluationRun, EvaluationPrediction
from app.schemas.evaluation import EvaluationRunResponse, EvaluationPredictionItem


def get_synthetic_dataset_dir() -> str:
    candidates = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "datasets", "synthetic"),
        os.path.abspath(os.path.join("..", "datasets", "synthetic")),
        os.path.abspath(os.path.join("datasets", "synthetic")),
    ]
    for p in candidates:
        if os.path.exists(os.path.join(p, "synthetic_cases_1000.json")) or os.path.exists(os.path.join(p, "synthetic_cases.json")):
            return p
    raise FileNotFoundError(f"Could not locate synthetic dataset directory in: {candidates}")


def load_dataset_split(split_name: str = "test") -> List[Dict[str, Any]]:
    """Load specific dataset partition ('test', 'val', 'train', or 'all')."""
    d_dir = get_synthetic_dataset_dir()
    if split_name in ["test", "val", "train"]:
        split_file = os.path.join(d_dir, "splits", f"{split_name}.json")
        if os.path.exists(split_file):
            with open(split_file, "r", encoding="utf-8") as f:
                return json.load(f)

    # Fallback to full 1000 cases or default
    full_1000 = os.path.join(d_dir, "synthetic_cases_1000.json")
    if os.path.exists(full_1000):
        with open(full_1000, "r", encoding="utf-8") as f:
            cases = json.load(f)
            if split_name in ["test", "val", "train"]:
                filtered = [c for c in cases if c.get("split") == split_name]
                if filtered:
                    return filtered
            return cases

    default_file = os.path.join(d_dir, "synthetic_cases.json")
    with open(default_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_bundled_synthetic_cases(split: str = "test") -> List[Dict[str, Any]]:
    """Load bundled synthetic cases. Defaults to held-out test split for zero-leakage evaluation."""
    return load_dataset_split(split)


class BenchmarkRunner:
    def __init__(self):
        # Ensure ML baseline is trained if synthetic data exists
        initialize_ml_baseline()
        self.llm_provider = get_llm_provider()

    async def run_single_prediction(
        self,
        model_type: str,
        case: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run prediction for one case under the designated model architecture."""
        text = case.get("text", "")
        ground_truth = case.get("reference_triage_category", TriageLevel.LEVEL_3.value)
        case_id = case.get("case_id", "UNKNOWN")
        age_group = case.get("age_group", "unknown")
        duration = case.get("duration", "unknown")
        severity = case.get("severity", "unknown")

        start = time.perf_counter()
        pred_level = TriageLevel.LEVEL_3.value
        triggered_rules: List[str] = []
        error: Optional[str] = None

        try:
            if model_type == "rule_based":
                extraction = extractor.extract(text, duration, severity)
                res = safety_engine.evaluate(
                    positive_symptoms=extraction.positive_symptoms,
                    negated_symptoms=extraction.negated_symptoms,
                    uncertain_symptoms=extraction.uncertain_symptoms,
                    unsupported_terms=extraction.unsupported_terms,
                    severity=extraction.detected_severity,
                    duration=extraction.detected_duration,
                    age_group=age_group,
                    has_ambiguity=extraction.has_ambiguity
                )
                pred_level = res.triage_level
                triggered_rules = [r.rule_id for r in res.triggered_rules]

            elif model_type == "ml_baseline":
                pred_level = ml_baseline.predict(text)

            elif model_type == "llm_only":
                # Controlled research benchmark: Unconstrained LLM output without safety engine
                extraction = extractor.extract(text, duration, severity)
                llm_res = await self.llm_provider.generate_explanation(
                    raw_text=text,
                    positive_symptoms=extraction.positive_symptoms,
                    negated_symptoms=extraction.negated_symptoms,
                    deterministic_level=TriageLevel.LEVEL_3.value,  # Neutral baseline
                    triggered_rule_names=[]
                )
                pred_level = llm_res.suggested_triage_level

            elif model_type == "hybrid":
                # Proposed SafeTriage Hybrid framework
                extraction = extractor.extract(text, duration, severity)
                res = safety_engine.evaluate(
                    positive_symptoms=extraction.positive_symptoms,
                    negated_symptoms=extraction.negated_symptoms,
                    uncertain_symptoms=extraction.uncertain_symptoms,
                    unsupported_terms=extraction.unsupported_terms,
                    severity=extraction.detected_severity,
                    duration=extraction.detected_duration,
                    age_group=age_group,
                    has_ambiguity=extraction.has_ambiguity
                )
                triggered_rules = [r.rule_id for r in res.triggered_rules]
                rule_level = res.triage_level

                llm_res = await self.llm_provider.generate_explanation(
                    raw_text=text,
                    positive_symptoms=extraction.positive_symptoms,
                    negated_symptoms=extraction.negated_symptoms,
                    deterministic_level=rule_level,
                    triggered_rule_names=[r.rule_name for r in res.triggered_rules]
                )

                # Enforce invariant: LLM cannot downgrade deterministic rule urgency
                pred_level = enforce_safety_invariant(rule_level, llm_res.suggested_triage_level)

            else:
                error = f"Unsupported model type '{model_type}'"
                pred_level = TriageLevel.LEVEL_3.value

        except Exception as e:
            error = str(e)
            pred_level = TriageLevel.LEVEL_3.value

        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        # Safety classifications
        is_correct = (pred_level == ground_truth)
        under_triaged = is_less_urgent(pred_level, ground_truth)
        over_triaged = is_more_urgent(pred_level, ground_truth)

        return {
            "case_id": case_id,
            "input_text": text,
            "ground_truth_level": ground_truth,
            "predicted_level": pred_level,
            "is_correct": is_correct,
            "under_triaged": under_triaged,
            "over_triaged": over_triaged,
            "triggered_rules": triggered_rules,
            "latency_ms": latency_ms,
            "error": error
        }

    async def execute_evaluation(
        self,
        model_type: str,
        cases: Optional[List[Dict[str, Any]]] = None,
        dataset_name: str = "synthetic_bundled",
        db: Optional[Session] = None
    ) -> EvaluationRunResponse:
        cases_to_eval = cases if cases is not None else load_bundled_synthetic_cases()

        run_id = str(uuid.uuid4())
        start_run = time.perf_counter()

        prediction_results: List[Dict[str, Any]] = []
        for case in cases_to_eval:
            item = await self.run_single_prediction(model_type, case)
            prediction_results.append(item)

        total_duration_ms = (time.perf_counter() - start_run) * 1000

        # Calculate pure-Python metrics
        metrics = calculate_evaluation_metrics(prediction_results, duration_ms=total_duration_ms)

        prediction_items = [
            EvaluationPredictionItem(
                case_id=p["case_id"],
                input_text=p["input_text"],
                ground_truth_level=p["ground_truth_level"],
                predicted_level=p["predicted_level"],
                is_correct=p["is_correct"],
                under_triaged=p["under_triaged"],
                over_triaged=p["over_triaged"],
                triggered_rules=p["triggered_rules"],
                latency_ms=p["latency_ms"],
                error=p["error"]
            )
            for p in prediction_results
        ]

        # Persist to database if db session is provided
        if db is not None:
            db_run = EvaluationRun(
                id=run_id,
                dataset_name=dataset_name,
                dataset_version="1.0.0",
                model_type=model_type,
                num_cases=len(cases_to_eval),
                accuracy=metrics.accuracy,
                macro_f1=metrics.macro_f1,
                weighted_f1=metrics.weighted_f1,
                under_triage_rate=metrics.under_triage_rate_overall,
                over_triage_rate=metrics.over_triage_rate_overall,
                red_flag_sensitivity=metrics.red_flag_sensitivity,
                metrics_json=metrics.model_dump_json(),
                duration_ms=total_duration_ms
            )
            db.add(db_run)

            for p in prediction_results:
                db_pred = EvaluationPrediction(
                    run_id=run_id,
                    case_id=p["case_id"],
                    input_text=p["input_text"][:500],
                    ground_truth_level=p["ground_truth_level"],
                    predicted_level=p["predicted_level"],
                    is_correct=p["is_correct"],
                    under_triaged=p["under_triaged"],
                    over_triaged=p["over_triaged"],
                    triggered_rules_json=json.dumps(p["triggered_rules"]),
                    latency_ms=p["latency_ms"],
                    error=p["error"]
                )
                db.add(db_pred)

            try:
                db.commit()
            except Exception:
                db.rollback()

        return EvaluationRunResponse(
            run_id=run_id,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            dataset_name=dataset_name,
            dataset_version="1.0.0",
            model_type=model_type,
            num_cases=len(cases_to_eval),
            metrics=metrics,
            predictions=prediction_items
        )


benchmark_runner = BenchmarkRunner()
