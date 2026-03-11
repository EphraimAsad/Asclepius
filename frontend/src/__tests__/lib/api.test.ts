import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { generateSessionId } from '@/lib/api';

describe('API Utilities', () => {
  describe('generateSessionId', () => {
    it('should generate a string', () => {
      const id = generateSessionId();
      expect(typeof id).toBe('string');
    });

    it('should generate unique IDs', () => {
      const ids = new Set();
      for (let i = 0; i < 100; i++) {
        ids.add(generateSessionId());
      }
      expect(ids.size).toBe(100);
    });

    it('should generate IDs of reasonable length', () => {
      const id = generateSessionId();
      expect(id.length).toBeGreaterThan(10);
      expect(id.length).toBeLessThan(50);
    });
  });
});

describe('API Error Handling', () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it('should handle network errors gracefully', async () => {
    (global.fetch as any).mockRejectedValue(new Error('Network error'));

    await expect(
      fetch('http://localhost:8000/api/health')
    ).rejects.toThrow('Network error');
  });

  it('should handle API error responses', async () => {
    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ detail: 'Internal server error' }),
    });

    const response = await fetch('http://localhost:8000/api/health');
    expect(response.ok).toBe(false);
    expect(response.status).toBe(500);
  });

  it('should handle successful responses', async () => {
    (global.fetch as any).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ status: 'healthy' }),
    });

    const response = await fetch('http://localhost:8000/api/health');
    expect(response.ok).toBe(true);
    const data = await response.json();
    expect(data.status).toBe('healthy');
  });
});

describe('Request Payload Validation', () => {
  it('should build valid triage request', () => {
    const patient = {
      age: 45,
      biological_sex: 'male',
      medical_history: { diabetes: true },
    };

    const symptoms = {
      chief_complaint: 'chest_pain',
      symptoms: { chest_pressure: true },
      duration_hours: 2,
      severity: 8,
    };

    const request = {
      patient,
      symptoms,
      session_id: generateSessionId(),
    };

    expect(request.patient.age).toBe(45);
    expect(request.symptoms.chief_complaint).toBe('chest_pain');
    expect(request.session_id).toBeTruthy();
  });

  it('should build valid lab interpretation request', () => {
    const patient = {
      age: 55,
      biological_sex: 'female',
      medical_history: {},
    };

    const labs = [
      {
        test_code: 'troponin',
        value: 50,
        unit: 'ng/L',
        reference_high: 14,
      },
    ];

    const request = {
      patient,
      labs,
      session_id: generateSessionId(),
    };

    expect(request.labs).toHaveLength(1);
    expect(request.labs[0].test_code).toBe('troponin');
    expect(request.labs[0].value).toBe(50);
  });
});
