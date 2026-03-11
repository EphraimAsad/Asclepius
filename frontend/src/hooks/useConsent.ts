'use client';

import { useState, useEffect, useCallback } from 'react';

const CONSENT_KEY = 'asclepius_consent';
const CONSENT_EXPIRY_DAYS = 30;

interface ConsentData {
  granted: boolean;
  timestamp: number;
}

export function useConsent() {
  const [hasConsent, setHasConsent] = useState<boolean>(false);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load consent from localStorage on mount
  useEffect(() => {
    if (typeof window === 'undefined') return;

    try {
      const stored = localStorage.getItem(CONSENT_KEY);
      if (stored) {
        const data: ConsentData = JSON.parse(stored);

        // Check if consent has expired
        const expiryMs = CONSENT_EXPIRY_DAYS * 24 * 60 * 60 * 1000;
        const isExpired = Date.now() - data.timestamp > expiryMs;

        if (!isExpired && data.granted) {
          setHasConsent(true);
        } else {
          localStorage.removeItem(CONSENT_KEY);
        }
      }
    } catch (e) {
      localStorage.removeItem(CONSENT_KEY);
    }

    setIsLoaded(true);
  }, []);

  const setConsent = useCallback((granted: boolean) => {
    if (typeof window === 'undefined') return;

    const data: ConsentData = {
      granted,
      timestamp: Date.now(),
    };

    localStorage.setItem(CONSENT_KEY, JSON.stringify(data));
    setHasConsent(granted);
  }, []);

  const clearConsent = useCallback(() => {
    if (typeof window === 'undefined') return;

    localStorage.removeItem(CONSENT_KEY);
    setHasConsent(false);
  }, []);

  return {
    hasConsent,
    isLoaded,
    setConsent,
    clearConsent,
  };
}
