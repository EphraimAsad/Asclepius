'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useConsent } from '@/hooks/useConsent';
import { api, generateSessionId } from '@/lib/api';

export default function ReviewPage() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();
  const [patient, setPatient] = useState<any>(null);
  const [symptoms, setSymptoms] = useState<any>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!isLoaded) return;

    if (!hasConsent) {
      router.push('/disclaimer');
      return;
    }

    const patientData = sessionStorage.getItem('triage_patient');
    const symptomData = sessionStorage.getItem('triage_symptoms');

    if (!patientData || !symptomData) {
      router.push('/triage');
      return;
    }

    setPatient(JSON.parse(patientData));
    setSymptoms(JSON.parse(symptomData));
    setIsReady(true);
  }, [hasConsent, isLoaded, router]);

  const handleSubmit = async () => {
    if (!patient || !symptoms) return;

    setIsSubmitting(true);
    setError(null);

    try {
      const request = {
        patient,
        symptoms: {
          chief_complaint: symptoms.chief_complaint,
          symptoms: symptoms.symptoms,
          duration_hours: symptoms.duration_hours,
          severity: symptoms.severity,
        },
        labs: [],
        session_id: generateSessionId(),
      };

      const result = await api.evaluateTriage(request);
      sessionStorage.setItem('triage_result', JSON.stringify(result));
      router.push('/triage/results');
    } catch (err: any) {
      setError(err.message || 'An error occurred while processing your request');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isLoaded || !isReady) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  const activeSymptoms = Object.entries(symptoms.symptoms)
    .filter(([_, value]) => value)
    .map(([key]) => key.replace(/_/g, ' '));

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Review Your Information
        </h1>
        <p className="text-gray-600">
          Please review the information below before submitting.
        </p>
      </div>

      {/* Patient Info */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Your Information</h2>
        <dl className="grid grid-cols-2 gap-4">
          <div>
            <dt className="text-sm text-gray-500">Age</dt>
            <dd className="font-medium">{patient.age}</dd>
          </div>
          <div>
            <dt className="text-sm text-gray-500">Sex</dt>
            <dd className="font-medium capitalize">{patient.sex}</dd>
          </div>
          {patient.comorbidities.length > 0 && (
            <div className="col-span-2">
              <dt className="text-sm text-gray-500">Medical History</dt>
              <dd className="font-medium">
                {patient.comorbidities.map((c: string) => c.replace(/_/g, ' ')).join(', ')}
              </dd>
            </div>
          )}
        </dl>
      </div>

      {/* Symptoms */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Your Symptoms</h2>
        <dl className="space-y-4">
          <div>
            <dt className="text-sm text-gray-500">Main Concern</dt>
            <dd className="font-medium capitalize">
              {symptoms.chief_complaint.replace(/_/g, ' ')}
            </dd>
          </div>
          {activeSymptoms.length > 0 && (
            <div>
              <dt className="text-sm text-gray-500">Symptoms Present</dt>
              <dd className="mt-2">
                <ul className="list-disc list-inside space-y-1">
                  {activeSymptoms.map((s) => (
                    <li key={s} className="capitalize">{s}</li>
                  ))}
                </ul>
              </dd>
            </div>
          )}
          {symptoms.duration_hours && (
            <div>
              <dt className="text-sm text-gray-500">Duration</dt>
              <dd className="font-medium">{symptoms.duration_hours} hours</dd>
            </div>
          )}
          {symptoms.severity && (
            <div>
              <dt className="text-sm text-gray-500">Severity</dt>
              <dd className="font-medium">{symptoms.severity}/10</dd>
            </div>
          )}
        </dl>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      <div className="flex gap-4">
        <button
          onClick={() => router.back()}
          className="flex-1 btn btn-secondary"
          disabled={isSubmitting}
        >
          Go Back
        </button>
        <button
          onClick={handleSubmit}
          className="flex-1 btn btn-primary"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Processing...' : 'Submit for Assessment'}
        </button>
      </div>
    </div>
  );
}
