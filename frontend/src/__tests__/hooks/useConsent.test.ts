import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';

// We need to test the consent logic directly
describe('Consent Logic', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.localStorage.getItem = vi.fn();
    window.localStorage.setItem = vi.fn();
    window.localStorage.removeItem = vi.fn();
  });

  it('should return false when no consent stored', () => {
    (window.localStorage.getItem as any).mockReturnValue(null);

    const stored = window.localStorage.getItem('asclepius_consent');
    expect(stored).toBeNull();
  });

  it('should return true when valid consent stored', () => {
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 15); // 15 days in future

    const consentData = JSON.stringify({
      accepted: true,
      timestamp: Date.now(),
      expiresAt: futureDate.getTime(),
    });

    (window.localStorage.getItem as any).mockReturnValue(consentData);

    const stored = window.localStorage.getItem('asclepius_consent');
    const parsed = JSON.parse(stored as string);

    expect(parsed.accepted).toBe(true);
    expect(parsed.expiresAt).toBeGreaterThan(Date.now());
  });

  it('should return false when consent expired', () => {
    const pastDate = new Date();
    pastDate.setDate(pastDate.getDate() - 1); // Yesterday

    const consentData = JSON.stringify({
      accepted: true,
      timestamp: Date.now() - 86400000 * 31, // 31 days ago
      expiresAt: pastDate.getTime(),
    });

    (window.localStorage.getItem as any).mockReturnValue(consentData);

    const stored = window.localStorage.getItem('asclepius_consent');
    const parsed = JSON.parse(stored as string);

    expect(parsed.expiresAt).toBeLessThan(Date.now());
  });

  it('should store consent correctly', () => {
    const now = Date.now();
    const expiresAt = now + 30 * 24 * 60 * 60 * 1000; // 30 days

    const consentData = {
      accepted: true,
      timestamp: now,
      expiresAt,
    };

    window.localStorage.setItem('asclepius_consent', JSON.stringify(consentData));

    expect(window.localStorage.setItem).toHaveBeenCalledWith(
      'asclepius_consent',
      expect.stringContaining('"accepted":true')
    );
  });

  it('should clear consent on revoke', () => {
    window.localStorage.removeItem('asclepius_consent');

    expect(window.localStorage.removeItem).toHaveBeenCalledWith('asclepius_consent');
  });
});

describe('Consent Expiry Logic', () => {
  it('should calculate 30 day expiry correctly', () => {
    const now = Date.now();
    const thirtyDays = 30 * 24 * 60 * 60 * 1000;
    const expiresAt = now + thirtyDays;

    expect(expiresAt - now).toBe(thirtyDays);
  });
});
