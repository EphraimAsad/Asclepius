const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface PatientContext {
  age: number;
  sex: 'male' | 'female' | 'other';
  comorbidities: string[];
  medications: string[];
}

export interface SymptomInput {
  chief_complaint: string;
  symptoms: Record<string, boolean>;
  duration_hours?: number;
  severity?: number;
}

export interface LabInput {
  test_code: string;
  value: number;
  unit: string;
  reference_low?: number;
  reference_high?: number;
}

export interface TriageRequest {
  patient: PatientContext;
  symptoms: SymptomInput;
  labs: LabInput[];
  session_id: string;
}

export interface MatchedRule {
  rule_id: string;
  label: string;
  disposition: string;
  priority: string;
  reason_codes: string[];
}

export interface TriageResult {
  disposition: string;
  priority: string;
  matched_rule_ids: string[];
  matched_rules: MatchedRule[];
  reason_codes: string[];
  explanation: string;
  safety_warnings: string[];
  derived_lab_statuses: Record<string, string>;
  risk_modifiers_applied: string[];
  disclaimer: string;
}

export interface LabStatusResult {
  test_code: string;
  status: string;
  interpretation_title: string;
  interpretation_body: string;
}

export interface LabInterpretResult {
  lab_statuses: LabStatusResult[];
  overall_disposition?: string;
  reason_codes: string[];
  safety_warnings: string[];
  disclaimer: string;
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new ApiError(response.status, error.detail || 'Request failed');
  }

  return response.json();
}

export const api = {
  async evaluateTriage(request: TriageRequest): Promise<TriageResult> {
    return fetchApi<TriageResult>('/triage/evaluate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  async interpretLabs(
    patient: PatientContext,
    labs: LabInput[],
    sessionId: string
  ): Promise<LabInterpretResult> {
    return fetchApi<LabInterpretResult>('/labs/interpret', {
      method: 'POST',
      body: JSON.stringify({
        patient,
        labs,
        session_id: sessionId,
      }),
    });
  },

  async checkHealth(): Promise<{ status: string; app_name: string; version: string }> {
    return fetchApi('/health');
  },
};

export function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
}
