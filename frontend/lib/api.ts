import { API_BASE_URL } from "./constants";
import {
  AssessmentRequest,
  AssessmentResponse,
  AssessmentHistoryResponse,
  EvaluationRunResponse,
  EvaluationRunSummary,
  HealthResponse,
  DatasetStatsResponse,
  User,
  AuthResponse,
  LoginRequest,
  RegisterRequest,
} from "./types";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

function getStoredToken(): string | null {
  if (typeof window !== "undefined") {
    try {
      return localStorage.getItem("safetriage_token");
    } catch {
      return null;
    }
  }
  return null;
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = getStoredToken();
  const authHeader: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {};

  const headers = {
    "Content-Type": "application/json",
    ...authHeader,
    ...options.headers,
  };

  try {
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      let errorMsg = `API Error ${res.status}: ${res.statusText}`;
      try {
        const errorJson = await res.json();
        if (errorJson.detail) errorMsg = errorJson.detail;
      } catch {
        // use default error message
      }
      throw new ApiError(errorMsg, res.status);
    }
    return (await res.json()) as T;
  } catch (err: any) {
    if (err instanceof ApiError) throw err;
    throw new Error(`Network failure connecting to ${url}: ${err.message}`);
  }
}

export const api = {
  // Assessment
  async submitAssessment(data: AssessmentRequest): Promise<AssessmentResponse> {
    return request<AssessmentResponse>("/assessments", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async getAssessment(id: string): Promise<AssessmentResponse> {
    return request<AssessmentResponse>(`/assessments/${id}`);
  },

  async listAssessments(limit = 50, offset = 0): Promise<AssessmentHistoryResponse> {
    return request<AssessmentHistoryResponse>(`/assessments?limit=${limit}&offset=${offset}`);
  },

  async deleteAssessment(id: string): Promise<{ status: string; message: string }> {
    return request<{ status: string; message: string }>(`/assessments/${id}`, {
      method: "DELETE",
    });
  },

  async clearAllAssessments(): Promise<{ status: string; message: string }> {
    return request<{ status: string; message: string }>("/assessments", {
      method: "DELETE",
    });
  },

  // Research Evaluation
  async runEvaluation(payload: {
    model_types: string[];
    dataset_name?: string;
    split?: string;
    custom_cases?: any[];
  }): Promise<EvaluationRunResponse[]> {
    return request<EvaluationRunResponse[]>("/research/evaluate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async getDatasetStats(): Promise<DatasetStatsResponse> {
    return request<DatasetStatsResponse>("/research/dataset-stats");
  },

  async listEvaluationRuns(): Promise<EvaluationRunSummary[]> {
    return request<EvaluationRunSummary[]>("/research/runs");
  },

  async getEvaluationRun(id: string): Promise<EvaluationRunResponse> {
    return request<EvaluationRunResponse>(`/research/runs/${id}`);
  },

  async getSyntheticCases(split?: string): Promise<any[]> {
    const query = split ? `?split=${encodeURIComponent(split)}` : "";
    return request<any[]>(`/research/synthetic-cases${query}`);
  },

  async uploadDataset(file: File): Promise<{
    status: string;
    dataset_name: string;
    total_rows_parsed: number;
    valid_cases_count: number;
    cases: any[];
    validation_errors: string[];
  }> {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_BASE_URL}/research/upload-dataset`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Upload failed" }));
      throw new Error(err.detail || "Failed to upload dataset");
    }

    return res.json();
  },

  // Health
  async getHealth(): Promise<HealthResponse> {
    return request<HealthResponse>("/health");
  },

  // Authentication
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const res = await request<AuthResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
    api.setSession(res.access_token, res.user);
    return res;
  },

  async login(data: LoginRequest): Promise<AuthResponse> {
    const res = await request<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
    api.setSession(res.access_token, res.user);
    return res;
  },

  async getMe(): Promise<User> {
    return request<User>("/auth/me");
  },

  async logout(): Promise<void> {
    try {
      await request("/auth/logout", { method: "POST" });
    } catch {
      // Ignore network errors on logout
    } finally {
      api.clearSession();
    }
  },

  setSession(token: string, user: User): void {
    if (typeof window !== "undefined") {
      try {
        localStorage.setItem("safetriage_token", token);
        localStorage.setItem("safetriage_user", JSON.stringify(user));
        window.dispatchEvent(new Event("auth-change"));
      } catch {
        // LocalStorage fallback
      }
    }
  },

  clearSession(): void {
    if (typeof window !== "undefined") {
      try {
        localStorage.removeItem("safetriage_token");
        localStorage.removeItem("safetriage_user");
        window.dispatchEvent(new Event("auth-change"));
      } catch {
        // LocalStorage fallback
      }
    }
  },

  getCurrentUser(): User | null {
    if (typeof window !== "undefined") {
      try {
        const u = localStorage.getItem("safetriage_user");
        return u ? JSON.parse(u) : null;
      } catch {
        return null;
      }
    }
    return null;
  },

  isAuthenticated(): boolean {
    return !!getStoredToken();
  },
};
