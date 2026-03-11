'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useConsent } from '@/hooks/useConsent';
import {
  CHEST_PAIN_SYMPTOMS,
  EMERGENCY_SYMPTOMS,
} from '@/lib/schemas/symptoms';

export default function SymptomsPage() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();
  const [chiefComplaint, setChiefComplaint] = useState<string>('');
  const [symptoms, setSymptoms] = useState<Record<string, boolean>>({});
  const [duration, setDuration] = useState<number | undefined>();
  const [severity, setSeverity] = useState<number>(5);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!isLoaded) return;

    if (!hasConsent) {
      router.push('/disclaimer');
      return;
    }

    const stored = sessionStorage.getItem('triage_chief_complaint');
    if (!stored) {
      router.push('/triage');
      return;
    }
    setChiefComplaint(stored);
    setIsReady(true);
  }, [hasConsent, isLoaded, router]);

  const toggleSymptom = (field: string) => {
    setSymptoms((prev) => ({
      ...prev,
      [field]: !prev[field],
    }));
  };

  const getSymptomList = () => {
    switch (chiefComplaint) {
      case 'chest_pain':
        return CHEST_PAIN_SYMPTOMS;
      default:
        return CHEST_PAIN_SYMPTOMS; // Fallback for MVP
    }
  };

  const handleContinue = () => {
    sessionStorage.setItem('triage_symptoms', JSON.stringify({
      chief_complaint: chiefComplaint,
      symptoms,
      duration_hours: duration,
      severity,
    }));
    router.push('/triage/review');
  };

  if (!isLoaded || !isReady) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Tell us about your symptoms
        </h1>
        <p className="text-gray-600">
          Select all symptoms that apply to your current situation.
        </p>
      </div>

      {/* Emergency Symptoms Warning */}
      <div className="card mb-6 border-red-200 bg-red-50">
        <h2 className="text-lg font-semibold text-red-800 mb-4">
          Emergency Warning Signs
        </h2>
        <p className="text-sm text-red-700 mb-4">
          If you are experiencing any of these symptoms, call 911 immediately:
        </p>
        <div className="space-y-2">
          {EMERGENCY_SYMPTOMS.map((symptom) => (
            <label
              key={symptom.field}
              className="flex items-center gap-3 p-3 rounded-lg bg-white border border-red-200 cursor-pointer hover:bg-red-50"
            >
              <input
                type="checkbox"
                checked={symptoms[symptom.field] || false}
                onChange={() => toggleSymptom(symptom.field)}
                className="h-4 w-4 text-red-600 rounded"
              />
              <span className="text-red-800">{symptom.label}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Symptom Checklist */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">
          Symptoms related to your concern
        </h2>
        <div className="space-y-2">
          {getSymptomList().map((symptom) => (
            <label
              key={symptom.field}
              className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                symptoms[symptom.field]
                  ? 'bg-blue-50 border-blue-300'
                  : 'border-gray-200 hover:bg-gray-50'
              }`}
            >
              <input
                type="checkbox"
                checked={symptoms[symptom.field] || false}
                onChange={() => toggleSymptom(symptom.field)}
                className="h-4 w-4 text-blue-600 rounded"
              />
              <span>{symptom.label}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Duration and Severity */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Additional Information</h2>

        <div className="space-y-4">
          <div>
            <label className="label">
              How long have you had these symptoms? (hours)
            </label>
            <input
              type="number"
              value={duration || ''}
              onChange={(e) => setDuration(parseFloat(e.target.value) || undefined)}
              className="input"
              placeholder="e.g., 2"
              min="0"
              step="0.5"
            />
          </div>

          <div>
            <label className="label">
              How severe are your symptoms? (1 = mild, 10 = severe)
            </label>
            <div className="flex items-center gap-4">
              <input
                type="range"
                min="1"
                max="10"
                value={severity}
                onChange={(e) => setSeverity(parseInt(e.target.value))}
                className="flex-1"
              />
              <span className="text-lg font-semibold w-8 text-center">
                {severity}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex gap-4">
        <button
          onClick={() => router.back()}
          className="flex-1 btn btn-secondary"
        >
          Back
        </button>
        <button
          onClick={handleContinue}
          className="flex-1 btn btn-primary"
        >
          Review & Submit
        </button>
      </div>
    </div>
  );
}
