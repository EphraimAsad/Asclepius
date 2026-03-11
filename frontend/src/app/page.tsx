'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useConsent } from '@/hooks/useConsent';

export default function Home() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();

  useEffect(() => {
    if (!isLoaded) return; // Wait for localStorage to load

    if (!hasConsent) {
      router.push('/disclaimer');
    } else {
      router.push('/home');
    }
  }, [hasConsent, isLoaded, router]);

  return (
    <div className="flex items-center justify-center min-h-[50vh]">
      <div className="animate-pulse text-gray-500">Loading...</div>
    </div>
  );
}
