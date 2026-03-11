'use client';

import { useConsent } from '@/hooks/useConsent';

export function DisclaimerBanner() {
  const { hasConsent } = useConsent();

  if (!hasConsent) {
    return null;
  }

  return (
    <div className="bg-amber-100 border-b border-amber-200">
      <div className="container mx-auto px-4 py-2">
        <p className="text-sm text-amber-800 text-center">
          <strong>Reminder:</strong> This tool is for educational purposes only.
          It is NOT a medical diagnosis or treatment recommendation.
        </p>
      </div>
    </div>
  );
}
