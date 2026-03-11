'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useConsent } from '@/hooks/useConsent';

export default function DisclaimerPage() {
  const router = useRouter();
  const { setConsent } = useConsent();
  const [ageConfirmed, setAgeConfirmed] = useState(false);
  const [understandConfirmed, setUnderstandConfirmed] = useState(false);

  const canProceed = ageConfirmed && understandConfirmed;

  const handleAccept = () => {
    if (canProceed) {
      setConsent(true);
      router.push('/home');
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Important Disclaimer
        </h1>

        <div className="space-y-4 mb-8">
          <div className="bg-red-50 border-l-4 border-red-500 p-4">
            <p className="text-red-800 font-medium">
              This tool is for EDUCATIONAL PURPOSES ONLY
            </p>
          </div>

          <div className="prose prose-sm text-gray-600">
            <p>
              <strong>Asclepius</strong> is a care navigation and education tool.
              It provides general health information to help you understand when
              to seek medical care.
            </p>

            <h3 className="text-lg font-semibold text-gray-900 mt-4">
              This tool is NOT:
            </h3>
            <ul className="list-disc list-inside space-y-1">
              <li>A substitute for professional medical advice</li>
              <li>A diagnostic tool</li>
              <li>A treatment recommendation system</li>
              <li>Suitable for medical emergencies</li>
              <li>Designed for use by minors (under 18)</li>
            </ul>

            <h3 className="text-lg font-semibold text-gray-900 mt-4">
              If you are experiencing a medical emergency:
            </h3>
            <p className="text-red-700 font-bold">
              CALL 911 IMMEDIATELY or go to your nearest emergency room.
            </p>

            <p className="mt-4">
              Always consult with a qualified healthcare provider for any
              health concerns. The information provided by this tool should
              not be used to make medical decisions.
            </p>
          </div>
        </div>

        <div className="space-y-4 border-t pt-6">
          <label className="flex items-start gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={ageConfirmed}
              onChange={(e) => setAgeConfirmed(e.target.checked)}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-gray-700">
              I confirm that I am <strong>18 years of age or older</strong>
            </span>
          </label>

          <label className="flex items-start gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={understandConfirmed}
              onChange={(e) => setUnderstandConfirmed(e.target.checked)}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-gray-700">
              I understand that this tool is <strong>NOT for medical diagnosis
              or treatment</strong> and that I should always consult a healthcare
              professional for medical advice
            </span>
          </label>
        </div>

        <div className="mt-8">
          <button
            onClick={handleAccept}
            disabled={!canProceed}
            className={`w-full btn ${
              canProceed ? 'btn-primary' : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            I Understand - Continue
          </button>
        </div>
      </div>
    </div>
  );
}
