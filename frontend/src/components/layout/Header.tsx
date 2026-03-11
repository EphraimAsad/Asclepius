'use client';

import Link from 'next/link';
import { useConsent } from '@/hooks/useConsent';

export function Header() {
  const { hasConsent, clearConsent } = useConsent();

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
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
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
            <span className="text-xl font-bold text-gray-900">Asclepius</span>
          </Link>

          <nav className="flex items-center gap-6">
            {hasConsent && (
              <>
                <Link
                  href="/home"
                  className="text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Home
                </Link>
                <Link
                  href="/triage"
                  className="text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Symptom Check
                </Link>
                <Link
                  href="/labs"
                  className="text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Lab Results
                </Link>
                <button
                  onClick={clearConsent}
                  className="text-sm text-gray-500 hover:text-gray-700"
                >
                  Reset Consent
                </button>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}
