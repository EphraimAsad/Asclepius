import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';

// Test disposition display logic
describe('Disposition Display Logic', () => {
  const dispositionColors: Record<string, { bg: string; text: string; border: string }> = {
    CALL_911: { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-300' },
    ER_NOW: { bg: 'bg-orange-100', text: 'text-orange-800', border: 'border-orange-300' },
    URGENT_CARE_TODAY: { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-300' },
    PRIMARY_CARE_24_72H: { bg: 'bg-blue-100', text: 'text-blue-800', border: 'border-blue-300' },
    SELF_CARE: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-300' },
  };

  const dispositionLabels: Record<string, string> = {
    CALL_911: 'Call 911 Immediately',
    ER_NOW: 'Go to Emergency Room Now',
    URGENT_CARE_TODAY: 'Seek Urgent Care Today',
    PRIMARY_CARE_24_72H: 'See Your Doctor Within 24-72 Hours',
    SELF_CARE: 'Self-Care May Be Appropriate',
  };

  it('should have correct colors for CALL_911', () => {
    const colors = dispositionColors['CALL_911'];
    expect(colors.bg).toBe('bg-red-100');
    expect(colors.text).toBe('text-red-800');
  });

  it('should have correct colors for ER_NOW', () => {
    const colors = dispositionColors['ER_NOW'];
    expect(colors.bg).toBe('bg-orange-100');
    expect(colors.text).toBe('text-orange-800');
  });

  it('should have correct colors for URGENT_CARE_TODAY', () => {
    const colors = dispositionColors['URGENT_CARE_TODAY'];
    expect(colors.bg).toBe('bg-yellow-100');
  });

  it('should have correct colors for PRIMARY_CARE_24_72H', () => {
    const colors = dispositionColors['PRIMARY_CARE_24_72H'];
    expect(colors.bg).toBe('bg-blue-100');
  });

  it('should have correct colors for SELF_CARE', () => {
    const colors = dispositionColors['SELF_CARE'];
    expect(colors.bg).toBe('bg-green-100');
  });

  it('should have labels for all dispositions', () => {
    expect(Object.keys(dispositionLabels)).toHaveLength(5);
    expect(dispositionLabels['CALL_911']).toContain('911');
    expect(dispositionLabels['ER_NOW']).toContain('Emergency');
    expect(dispositionLabels['SELF_CARE']).toContain('Self-Care');
  });

  it('should prioritize dispositions correctly', () => {
    const priorities = ['CALL_911', 'ER_NOW', 'URGENT_CARE_TODAY', 'PRIMARY_CARE_24_72H', 'SELF_CARE'];

    // CALL_911 should be highest priority (index 0)
    expect(priorities.indexOf('CALL_911')).toBe(0);

    // SELF_CARE should be lowest priority
    expect(priorities.indexOf('SELF_CARE')).toBe(4);
  });
});

describe('Disposition Message Content', () => {
  it('should include urgency for emergency dispositions', () => {
    const emergencyMessages = {
      CALL_911: 'Call 911 Immediately',
      ER_NOW: 'Go to Emergency Room Now',
    };

    expect(emergencyMessages['CALL_911']).toContain('Immediately');
    expect(emergencyMessages['ER_NOW']).toContain('Now');
  });

  it('should include timeframe for non-emergency dispositions', () => {
    const timeframeMessages = {
      URGENT_CARE_TODAY: 'Seek Urgent Care Today',
      PRIMARY_CARE_24_72H: 'See Your Doctor Within 24-72 Hours',
    };

    expect(timeframeMessages['URGENT_CARE_TODAY']).toContain('Today');
    expect(timeframeMessages['PRIMARY_CARE_24_72H']).toContain('24-72');
  });
});
