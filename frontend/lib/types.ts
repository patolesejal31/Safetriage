export type TriageLevel = "Level 1" | "Level 2" | "Level 3" | "Level 4";

export interface SymptomItem {
  name: string;
  status: "POSITIVE" | "NEGATED" | "HISTORICAL" | "THIRD_PARTY" | "UNCERTAIN" | "UNSUPPORTED";
  duration?: string;
  severity?: string;
  raw_text_span?: string;
}

export interface RuleTriggerItem {
  rule_id: string;
  rule_name: string;
  assigned_level: string;
  rationale: string;
  source_guideline: string;
}

export interface FollowUpQuestion {
  id: string;
  question: string;
  relevant_symptom: string;
  options: string[];
  critical_warning_if_yes?: string;
}

export interface AssessmentRequest {
  text: string;
  age_group?: string;
  duration?: string;
  severity?: string;
  associated_answers?: Record<string, string>;
}

export interface AssessmentResponse {
  id: string;
  created_at: string;
  triage_level: TriageLevel;
  title: string;
  care_recommendation: string;
  action_timeframe: string;
  color: string;
  is_emergency: boolean;
  uncertainty_flag: boolean;
  explanation: string;
  limitations: string;
  symptoms: SymptomItem[];
  negated_symptoms: string[];
  uncertain_symptoms: string[];
  unsupported_terms: string[];
  triggered_rules: RuleTriggerItem[];
  follow_up_questions: FollowUpQuestion[];
  emergency_contacts: {
    primary: string;
    ambulance: string;
    disclaimer: string;
  };
  execution_mode: string;
  latency_ms: number;
}

export interface AssessmentListItem {
  id: string;
  created_at: string;
  user_age_group: string;
  triage_level: TriageLevel;
  symptom_summary: string;
  is_emergency: boolean;
  execution_mode: string;
}

export interface AssessmentHistoryResponse {
  total: number;
  items: AssessmentListItem[];
}

export interface ClassMetric {
  precision: number;
  recall: number;
  f1_score: number;
  support: number;
}

export interface MetricReport {
  accuracy: number;
  macro_f1: number;
  weighted_f1: number;
  under_triage_rate_overall: number;
  under_triage_rate_eligible: number;
  over_triage_rate_overall: number;
  over_triage_rate_eligible: number;
  red_flag_sensitivity: number;
  confusion_matrix: number[][];
  classes: string[];
  per_class_metrics: Record<string, ClassMetric>;
  total_evaluated: number;
  failed_predictions: number;
  duration_ms: number;
}

export interface EvaluationPredictionItem {
  case_id: string;
  input_text: string;
  ground_truth_level: string;
  predicted_level: string;
  is_correct: boolean;
  under_triaged: boolean;
  over_triaged: boolean;
  triggered_rules: string[];
  latency_ms: number;
  error?: string;
}

export interface EvaluationRunResponse {
  run_id: string;
  timestamp: string;
  dataset_name: string;
  dataset_version: string;
  model_type: string;
  num_cases: number;
  metrics: MetricReport;
  predictions: EvaluationPredictionItem[];
}

export interface EvaluationRunSummary {
  id: string;
  timestamp: string;
  dataset_name: string;
  model_type: string;
  num_cases: number;
  accuracy: number;
  macro_f1: number;
  under_triage_rate: number;
  over_triage_rate: number;
  red_flag_sensitivity: number;
  duration_ms: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  environment: string;
  database: string;
  llm_provider: string;
  llm_configured: boolean;
  ml_baseline_ready: boolean;
  rules_loaded: number;
  emergency_contacts: {
    primary: string;
    ambulance: string;
    disclaimer: string;
  };
}

export interface DatasetStatsResponse {
  total_cases: number;
  splits: Record<string, number>;
  class_distribution: Record<string, number>;
  split_class_distribution: Record<string, Record<string, number>>;
  template_families_count: number;
  is_synthetic: boolean;
  provenance: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  role?: string;
}

