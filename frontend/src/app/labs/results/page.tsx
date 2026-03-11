'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useConsent } from '@/hooks/useConsent';
import { LabInterpretResult } from '@/lib/api';

const STATUS_CONFIG: Record<string, { color: string; bg: string; label: string }> = {
  CRITICAL_LOW: { color: 'text-red-700', bg: 'bg-red-50', label: 'Critically Low' },
  LOW: { color: 'text-amber-700', bg: 'bg-amber-50', label: 'Low' },
  NORMAL: { color: 'text-green-700', bg: 'bg-green-50', label: 'Normal' },
  HIGH: { color: 'text-amber-700', bg: 'bg-amber-50', label: 'High' },
  CRITICAL_HIGH: { color: 'text-red-700', bg: 'bg-red-50', label: 'Critically High' },
};

export default function LabResultsPage() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();
  const [result, setResult] = useState<LabInterpretResult | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!isLoaded) return;

    if (!hasConsent) {
      router.push('/disclaimer');
      return;
    }

    const resultData = sessionStorage.getItem('lab_result');
    if (!resultData) {
      router.push('/labs');
      return;
    }

    setResult(JSON.parse(resultData));
    setIsReady(true);
  }, [hasConsent, isLoaded, router]);

  if (!isLoaded || !isReady) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Your Lab Interpretation
        </h1>
        <p className="text-gray-600">
          Here is educational information about your lab results.
        </p>
      </div>

      {/* Lab Results */}
      <div className="space-y-4 mb-6">
        {result.lab_statuses.map((lab) => {
          const config = STATUS_CONFIG[lab.status] || STATUS_CONFIG.NORMAL;
          return (
            <div
              key={lab.test_code}
              className={`card ${config.bg} border-l-4 ${
                lab.status.includes('CRITICAL') ? 'border-red-500' :
                lab.status === 'NORMAL' ? 'border-green-500' : 'border-amber-500'
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <h2 className="text-lg font-semibold">{lab.interpretation_title}</h2>
                <span className={`px-2 py-1 rounded text-sm font-medium ${config.color} ${config.bg}`}>
                  {config.label}
                </span>
              </div>
              <p className="text-gray-600">{lab.interpretation_body}</p>
            </div>
          );
        })}
      </div>

      {/* Safety Warnings */}
      {result.safety_warnings.length > 0 && (
        <div className="card mb-6 border-amber-200 bg-amber-50">
          <h2 className="text-lg font-semibold text-amber-800 mb-4">
            Important Notes
          </h2>
          <ul className="space-y-3">
            {result.safety_warnings.map((warning, i) => (
              <li key={i} className="flex items-start gap-2 text-amber-700">
                <span className="text-amber-500 mt-1">⚠️</span>
                <span>{warning}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Disclaimer */}
      <div className="card bg-gray-50 border-gray-200">
        <h2 className="text-sm font-semibold text-gray-500 mb-2">
          Important Disclaimer
        </h2>
        <p className="text-sm text-gray-500">
          {result.disclaimer}
        </p>
      </div>

      {/* Actions */}
      <div className="mt-8 flex gap-4">
        <Link href="/home" className="flex-1 btn btn-secondary text-center">
          Back to Home
        </Link>
        <Link href="/labs" className="flex-1 btn btn-primary text-center">
          New Interpretation
        </Link>
      </div>
    </div>
  );
}
