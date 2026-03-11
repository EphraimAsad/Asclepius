'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useConsent } from '@/hooks/useConsent';

export default function HomePage() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();

  useEffect(() => {
    if (!isLoaded) return; // Wait for localStorage to load

    if (!hasConsent) {
      router.push('/disclaimer');
    }
  }, [hasConsent, isLoaded, router]);

  // Show loading while checking consent
  if (!isLoaded) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  if (!hasConsent) {
    return null;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Welcome to Asclepius
        </h1>
        <p className="text-lg text-gray-600">
          Educational health information and care navigation
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Symptom Triage Card */}
        <Link href="/triage" className="card hover:shadow-lg transition-shadow group">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
              <svg
                className="w-8 h-8 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                Symptom Assessment
              </h2>
              <p className="text-gray-600">
                Answer questions about your symptoms to get guidance on the
                appropriate level of care.
              </p>
            </div>
          </div>
        </Link>

        {/* Lab Interpretation Card */}
        <Link href="/labs" className="card hover:shadow-lg transition-shadow group">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-green-100 rounded-lg group-hover:bg-green-200 transition-colors">
              <svg
                className="w-8 h-8 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                Lab Result Interpretation
              </h2>
              <p className="text-gray-600">
                Enter your lab results to get educational information about
                what they mean.
              </p>
            </div>
          </div>
        </Link>
      </div>

      <div className="mt-12 bg-amber-50 border border-amber-200 rounded-lg p-6">
        <h3 className="font-semibold text-amber-800 mb-2">
          Important Reminder
        </h3>
        <p className="text-amber-700 text-sm">
          This tool provides educational information only. It is not a
          substitute for professional medical advice, diagnosis, or treatment.
          Always seek the advice of your physician or other qualified health
          provider with any questions you may have regarding a medical condition.
        </p>
      </div>
    </div>
  );
}
