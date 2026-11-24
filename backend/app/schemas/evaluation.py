from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class EvaluationRequest(BaseModel):
    model_types: List[str] = Field(
        default=["rule_based", "hybrid"],
        description="List of models to evaluate: rule_based, ml_baseline, llm_only, hybrid"
    )
    dataset_name: Optional[str] = Field(default="synthetic_bundled", description="synthetic_bundled or uploaded")
    split: Optional[str] = Field(default="test", description="Dataset split to evaluate: 'test', 'val', 'train', or 'all'")
    custom_cases: Optional[List[Dict[str, Any]]] = None


class ClassMetricSchema(BaseModel):
    precision: float
    recall: float
    f1_score: float
    support: int


class MetricReportSchema(BaseModel):
    accuracy: float
    macro_f1: float
    weighted_f1: float
    under_triage_rate_overall: float
    under_triage_rate_eligible: float
    over_triage_rate_overall: float
    over_triage_rate_eligible: float
    red_flag_sensitivity: float
    confusion_matrix: List[List[int]]
    classes: List[str]
    per_class_metrics: Dict[str, ClassMetricSchema]
    total_evaluated: int
    failed_predictions: int
    duration_ms: float


class EvaluationPredictionItem(BaseModel):
    case_id: str
    input_text: str
    ground_truth_level: str
    predicted_level: str
    is_correct: bool
    under_triaged: bool
    over_triaged: bool
    triggered_rules: List[str]
    latency_ms: float
    error: Optional[str] = None


class EvaluationRunResponse(BaseModel):
    run_id: str
    timestamp: datetime
    dataset_name: str
    dataset_version: str
    model_type: str
    num_cases: int
    metrics: MetricReportSchema
    predictions: List[EvaluationPredictionItem]


class EvaluationRunSummary(BaseModel):
    id: str
    timestamp: datetime
    dataset_name: str
    model_type: str
    num_cases: int
    accuracy: float
    macro_f1: float
    under_triage_rate: float
    over_triage_rate: float
    red_flag_sensitivity: float
    duration_ms: float


class DatasetStatsResponse(BaseModel):
    total_cases: int
    splits: Dict[str, int]
    class_distribution: Dict[str, int]
    split_class_distribution: Dict[str, Dict[str, int]]
    template_families_count: int
    is_synthetic: bool
    provenance: str

