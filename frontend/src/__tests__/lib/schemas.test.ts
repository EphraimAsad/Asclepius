import { describe, it, expect } from 'vitest';
import {
  CHIEF_COMPLAINTS,
  SYMPTOM_SETS,
  EMERGENCY_SYMPTOMS,
  symptomSchema,
} from '@/lib/schemas/symptoms';

describe('Chief Complaints', () => {
  it('should have 21 chief complaints', () => {
    expect(CHIEF_COMPLAINTS).toHaveLength(21);
  });

  it('should have unique values', () => {
    const values = CHIEF_COMPLAINTS.map(c => c.value);
    const uniqueValues = new Set(values);
    expect(uniqueValues.size).toBe(values.length);
  });

  it('should have required fields for each complaint', () => {
    CHIEF_COMPLAINTS.forEach(complaint => {
      expect(complaint).toHaveProperty('value');
      expect(complaint).toHaveProperty('label');
      expect(complaint.value).toBeTruthy();
      expect(complaint.label).toBeTruthy();
    });
  });

  it('should include all expected pathways', () => {
    const values = CHIEF_COMPLAINTS.map(c => c.value);
    expect(values).toContain('chest_pain');
    expect(values).toContain('shortness_of_breath');
    expect(values).toContain('abdominal_pain');
    expect(values).toContain('headache');
    expect(values).toContain('dizziness');
    expect(values).toContain('fever');
    expect(values).toContain('back_pain');
    expect(values).toContain('anxiety_panic');
    expect(values).toContain('leg_swelling');
  });
});

describe('Symptom Sets', () => {
  it('should have symptom set for each chief complaint', () => {
    CHIEF_COMPLAINTS.forEach(complaint => {
      expect(SYMPTOM_SETS[complaint.value]).toBeDefined();
      expect(Array.isArray(SYMPTOM_SETS[complaint.value])).toBe(true);
    });
  });

  it('should have at least 5 symptoms per set', () => {
    Object.entries(SYMPTOM_SETS).forEach(([key, symptoms]) => {
      expect(symptoms.length).toBeGreaterThanOrEqual(5);
    });
  });

  it('should have required fields for each symptom', () => {
    Object.values(SYMPTOM_SETS).forEach(symptoms => {
      symptoms.forEach(symptom => {
        expect(symptom).toHaveProperty('field');
        expect(symptom).toHaveProperty('label');
        expect(symptom.field).toBeTruthy();
        expect(symptom.label).toBeTruthy();
      });
    });
  });
});

describe('Emergency Symptoms', () => {
  it('should have emergency symptoms defined', () => {
    expect(EMERGENCY_SYMPTOMS.length).toBeGreaterThan(0);
  });

  it('should include critical warning signs', () => {
    const fields = EMERGENCY_SYMPTOMS.map(s => s.field);
    expect(fields).toContain('unresponsive');
    expect(fields).toContain('not_breathing');
    expect(fields).toContain('facial_drooping');
  });
});

describe('Symptom Schema Validation', () => {
  it('should validate valid symptom data', () => {
    const validData = {
      chief_complaint: 'chest_pain',
      symptoms: { chest_pressure: true, shortness_of_breath: false },
      duration_hours: 2,
      severity: 7,
    };

    const result = symptomSchema.safeParse(validData);
    expect(result.success).toBe(true);
  });

  it('should reject empty chief complaint', () => {
    const invalidData = {
      chief_complaint: '',
      symptoms: {},
    };

    const result = symptomSchema.safeParse(invalidData);
    expect(result.success).toBe(false);
  });

  it('should reject severity out of range', () => {
    const invalidData = {
      chief_complaint: 'headache',
      symptoms: {},
      severity: 15,
    };

    const result = symptomSchema.safeParse(invalidData);
    expect(result.success).toBe(false);
  });

  it('should allow optional fields to be undefined', () => {
    const minimalData = {
      chief_complaint: 'fever',
    };

    const result = symptomSchema.safeParse(minimalData);
    expect(result.success).toBe(true);
  });
});
