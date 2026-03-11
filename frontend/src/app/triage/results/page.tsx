'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useConsent } from '@/hooks/useConsent';
import { DispositionCard } from '@/components/triage/DispositionCard';
import { TriageResult } from '@/lib/api';

export default function ResultsPage() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();
  const [result, setResult] = useState<TriageResult | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!isLoaded) return;

    if (!hasConsent) {
      router.push('/disclaimer');
      return;
    }

    const resultData = sessionStorage.getItem('triage_result');
    if (!resultData) {
      router.push('/triage');
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
          Your Assessment Results
        </h1>
        <p className="text-gray-600">
          Based on the information you provided, here is our recommendation.
        </p>
      </div>

      {/* Disposition Card */}
      <div className="mb-6">
        <DispositionCard
          disposition={result.disposition}
          priority={result.priority}
        />
      </div>

      {/* Explanation */}
      {result.explanation && (
        <div className="card mb-6">
          <h2 className="text-lg font-semibold mb-4">Why This Recommendation</h2>
          <div className="prose prose-sm max-w-none text-gray-600">
            {result.explanation.split('\n\n').map((paragraph, i) => (
              <p key={i} className="mb-3">
                {paragraph.startsWith('**') ? (
                  <>
                    <strong>{paragraph.replace(/\*\*/g, '').split('\n')[0]}</strong>
                    <br />
                    {paragraph.split('\n').slice(1).join('\n')}
                  </>
                ) : (
                  paragraph
                )}
              </p>
            ))}
          </div>
        </div>
      )}

      {/* Safety Warnings */}
      {result.safety_warnings.length > 0 && (
        <div className="card mb-6 border-amber-200 bg-amber-50">
          <h2 className="text-lg font-semibold text-amber-800 mb-4">
            Important Safety Information
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
        <Link href="/triage" className="flex-1 btn btn-primary text-center">
          New Assessment
        </Link>
      </div>

      {/* Debug info (for development) */}
      {process.env.NODE_ENV === 'development' && (
        <details className="mt-8 p-4 bg-gray-100 rounded-lg">
          <summary className="cursor-pointer text-sm text-gray-500">
            Debug: Matched Rules
          </summary>
          <pre className="mt-2 text-xs overflow-auto">
            {JSON.stringify(result.matched_rules, null, 2)}
          </pre>
        </details>
      )}
    </div>
  );
}
