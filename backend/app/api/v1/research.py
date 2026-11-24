import csv
import io
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.database import get_db
from app.models.evaluation import EvaluationRun, EvaluationPrediction
from app.schemas.evaluation import (
    EvaluationRequest,
    EvaluationRunResponse,
    EvaluationRunSummary,
    DatasetStatsResponse,
)
from app.research.benchmark_runner import (
    benchmark_runner,
    load_bundled_synthetic_cases,
    load_dataset_split,
)
from app.core.urgency import URGENCY_RANK

router = APIRouter(prefix="/research", tags=["Research Laboratory"])


@router.get("/dataset-stats", response_model=DatasetStatsResponse)
def get_dataset_stats():
    """Retrieve verified statistics, split partitions, and class distributions for the 1,000 synthetic cases."""
    all_cases = load_dataset_split("all")
    total = len(all_cases)

    splits: dict = {}
    class_dist: dict = {}
    split_class_dist: dict = {}
    families = set()

    for c in all_cases:
        s = c.get("split", "unknown")
        cat = c.get("reference_triage_category", "unknown")
        fam = c.get("template_family_id")
        if fam:
            families.add(fam)

        splits[s] = splits.get(s, 0) + 1
        class_dist[cat] = class_dist.get(cat, 0) + 1

        if s not in split_class_dist:
            split_class_dist[s] = {}
        split_class_dist[s][cat] = split_class_dist[s].get(cat, 0) + 1

    return DatasetStatsResponse(
        total_cases=total,
        splits=splits,
        class_distribution=class_dist,
        split_class_distribution=split_class_dist,
        template_families_count=len(families),
        is_synthetic=True,
        provenance="Synthetic clinical vignettes for research benchmarking. Split isolation enforced by template family."
    )


@router.get("/synthetic-cases")
def get_synthetic_cases(split: Optional[str] = "all"):
    """Retrieve bundled synthetic test cases with reference annotations (optionally filtered by split: 'test', 'val', 'train', 'all')."""
    return load_dataset_split(split or "all")


@router.post("/evaluate", response_model=List[EvaluationRunResponse])
async def run_evaluation(
    request: EvaluationRequest,
    db: Session = Depends(get_db)
):
    """
    Execute comparative evaluation runs across requested models:
    - 'rule_based': Deterministic rule engine baseline
    - 'ml_baseline': Scikit-learn TF-IDF + Logistic Regression
    - 'llm_only': Unconstrained LLM output (experimental research benchmark)
    - 'hybrid': Proposed SafeTriage framework with safety invariant enforcement
    """
    split_name = request.split or "test"
    cases = request.custom_cases if request.custom_cases else load_dataset_split(split_name)
    ds_name = request.dataset_name or f"synthetic_{split_name}"

    results: List[EvaluationRunResponse] = []
    for model_type in request.model_types:
        run_res = await benchmark_runner.execute_evaluation(
            model_type=model_type,
            cases=cases,
            dataset_name=ds_name,
            db=db
        )
        results.append(run_res)

    return results


@router.get("/runs", response_model=List[EvaluationRunSummary])
def list_evaluation_runs(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List historical research evaluation runs."""
    records = db.query(EvaluationRun).order_by(desc(EvaluationRun.timestamp)).limit(limit).all()
    return [
        EvaluationRunSummary(
            id=r.id,
            timestamp=r.timestamp,
            dataset_name=r.dataset_name,
            model_type=r.model_type,
            num_cases=r.num_cases,
            accuracy=r.accuracy,
            macro_f1=r.macro_f1,
            under_triage_rate=r.under_triage_rate,
            over_triage_rate=r.over_triage_rate,
            red_flag_sensitivity=r.red_flag_sensitivity,
            duration_ms=r.duration_ms
        )
        for r in records
    ]


@router.get("/runs/{run_id}")
def get_evaluation_run(
    run_id: str,
    db: Session = Depends(get_db)
):
    """Get complete details and itemized predictions of an evaluation run."""
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation run not found.")

    return {
        "run_id": run.id,
        "timestamp": run.timestamp,
        "dataset_name": run.dataset_name,
        "dataset_version": run.dataset_version,
        "model_type": run.model_type,
        "num_cases": run.num_cases,
        "metrics": json.loads(run.metrics_json),
        "predictions": [
            {
                "case_id": p.case_id,
                "input_text": p.input_text,
                "ground_truth_level": p.ground_truth_level,
                "predicted_level": p.predicted_level,
                "is_correct": p.is_correct,
                "under_triaged": p.under_triaged,
                "over_triaged": p.over_triaged,
                "triggered_rules": json.loads(p.triggered_rules_json or "[]"),
                "latency_ms": p.latency_ms,
                "error": p.error
            }
            for p in run.predictions
        ]
    }


@router.post("/upload-dataset")
async def upload_dataset(
    file: UploadFile = File(...)
):
    """
    Upload and validate a custom research CSV or JSON dataset.
    Validates required columns: case_id, text, reference_triage_category.
    """
    content = await file.read()
    filename = file.filename.lower() if file.filename else ""

    parsed_cases = []

    if filename.endswith(".json"):
        try:
            data = json.loads(content.decode("utf-8"))
            if not isinstance(data, list):
                raise ValueError("JSON file must contain an array of case objects.")
            parsed_cases = data
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")

    elif filename.endswith(".csv"):
        try:
            text_data = content.decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text_data))
            for row in reader:
                parsed_cases.append(row)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Only CSV and JSON datasets are supported.")

    if not parsed_cases:
        raise HTTPException(status_code=400, detail="Uploaded dataset contains 0 valid rows.")

    # Validation
    required_keys = ["case_id", "text", "reference_triage_category"]
    valid_cases = []
    errors = []

    for i, c in enumerate(parsed_cases):
        missing = [k for k in required_keys if k not in c or not str(c[k]).strip()]
        if missing:
            errors.append(f"Row {i+1}: Missing required keys {missing}")
            continue

        ref_cat = str(c["reference_triage_category"]).strip()
        if ref_cat not in URGENCY_RANK:
            errors.append(f"Row {i+1} ({c.get('case_id')}): Invalid category '{ref_cat}'. Must be one of {list(URGENCY_RANK.keys())}")
            continue

        valid_cases.append({
            "case_id": str(c["case_id"]).strip(),
            "text": str(c["text"]).strip(),
            "reference_triage_category": ref_cat,
            "age_group": str(c.get("age_group", "unknown")).strip(),
            "duration": str(c.get("duration", "unknown")).strip(),
            "severity": str(c.get("severity", "unknown")).strip(),
            "rationale": str(c.get("rationale", "")).strip(),
            "provenance": str(c.get("provenance", "Uploaded dataset")).strip(),
        })

    if not valid_cases:
        raise HTTPException(status_code=400, detail=f"No rows passed schema validation. Errors: {errors[:5]}")

    return {
        "status": "success",
        "dataset_name": file.filename,
        "total_rows_parsed": len(parsed_cases),
        "valid_cases_count": len(valid_cases),
        "validation_errors": errors[:10],
        "cases": valid_cases
    }


@router.get("/export/{run_id}")
def export_evaluation(
    run_id: str,
    format: str = "json",
    db: Session = Depends(get_db)
):
    """Export evaluation predictions and calculated metrics as JSON or CSV."""
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation run not found.")

    if format.lower() == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "run_id", "model_type", "dataset_name", "case_id", "ground_truth_level",
            "predicted_level", "is_correct", "under_triaged", "over_triaged",
            "triggered_rules", "latency_ms", "error"
        ])
        for p in run.predictions:
            writer.writerow([
                run.id, run.model_type, run.dataset_name, p.case_id,
                p.ground_truth_level, p.predicted_level, p.is_correct,
                p.under_triaged, p.over_triaged, p.triggered_rules_json,
                p.latency_ms, p.error or ""
            ])

        response = Response(content=output.getvalue(), media_type="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename=safetriage_run_{run_id}.csv"
        return response

    # Default JSON export
    export_data = {
        "run_id": run.id,
        "timestamp": run.timestamp.isoformat(),
        "model_type": run.model_type,
        "dataset_name": run.dataset_name,
        "num_cases": run.num_cases,
        "metrics": json.loads(run.metrics_json),
        "predictions": [
            {
                "case_id": p.case_id,
                "input_text": p.input_text,
                "ground_truth_level": p.ground_truth_level,
                "predicted_level": p.predicted_level,
                "is_correct": p.is_correct,
                "under_triaged": p.under_triaged,
                "over_triaged": p.over_triaged,
                "triggered_rules": json.loads(p.triggered_rules_json or "[]"),
                "latency_ms": p.latency_ms,
                "error": p.error
            }
            for p in run.predictions
        ]
    }
    response = Response(content=json.dumps(export_data, indent=2), media_type="application/json")
    response.headers["Content-Disposition"] = f"attachment; filename=safetriage_run_{run_id}.json"
    return response
