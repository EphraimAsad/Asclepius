'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useConsent } from '@/hooks/useConsent';
import { api, generateSessionId, LabInput } from '@/lib/api';

const AVAILABLE_LABS = [
  // Cardiac
  {
    code: 'troponin',
    name: 'Troponin',
    category: 'Cardiac',
    units: ['ng/L', 'ng/mL'],
    defaultUnit: 'ng/L',
  },
  // Metabolic
  {
    code: 'glucose',
    name: 'Glucose',
    category: 'Metabolic',
    units: ['mg/dL', 'mmol/L'],
    defaultUnit: 'mg/dL',
  },
  {
    code: 'hba1c',
    name: 'Hemoglobin A1c',
    category: 'Metabolic',
    units: ['%'],
    defaultUnit: '%',
  },
  // Hematology
  {
    code: 'hemoglobin',
    name: 'Hemoglobin',
    category: 'Hematology',
    units: ['g/dL', 'g/L'],
    defaultUnit: 'g/dL',
  },
  {
    code: 'hematocrit',
    name: 'Hematocrit',
    category: 'Hematology',
    units: ['%'],
    defaultUnit: '%',
  },
  {
    code: 'wbc',
    name: 'White Blood Cell Count',
    category: 'Hematology',
    units: ['K/uL', '10^9/L'],
    defaultUnit: 'K/uL',
  },
  {
    code: 'platelet',
    name: 'Platelet Count',
    category: 'Hematology',
    units: ['K/uL', '10^9/L'],
    defaultUnit: 'K/uL',
  },
  // Renal
  {
    code: 'creatinine',
    name: 'Creatinine',
    category: 'Renal',
    units: ['mg/dL', 'umol/L'],
    defaultUnit: 'mg/dL',
  },
  {
    code: 'bun',
    name: 'BUN (Blood Urea Nitrogen)',
    category: 'Renal',
    units: ['mg/dL', 'mmol/L'],
    defaultUnit: 'mg/dL',
  },
  // Electrolytes
  {
    code: 'sodium',
    name: 'Sodium',
    category: 'Electrolytes',
    units: ['mEq/L', 'mmol/L'],
    defaultUnit: 'mEq/L',
  },
  {
    code: 'potassium',
    name: 'Potassium',
    category: 'Electrolytes',
    units: ['mEq/L', 'mmol/L'],
    defaultUnit: 'mEq/L',
  },
  {
    code: 'chloride',
    name: 'Chloride',
    category: 'Electrolytes',
    units: ['mEq/L', 'mmol/L'],
    defaultUnit: 'mEq/L',
  },
  {
    code: 'co2',
    name: 'CO2 / Bicarbonate',
    category: 'Electrolytes',
    units: ['mEq/L', 'mmol/L'],
    defaultUnit: 'mEq/L',
  },
  {
    code: 'calcium',
    name: 'Calcium',
    category: 'Electrolytes',
    units: ['mg/dL', 'mmol/L'],
    defaultUnit: 'mg/dL',
  },
  {
    code: 'magnesium',
    name: 'Magnesium',
    category: 'Electrolytes',
    units: ['mg/dL', 'mEq/L', 'mmol/L'],
    defaultUnit: 'mg/dL',
  },
  // Liver
  {
    code: 'ast',
    name: 'AST (SGOT)',
    category: 'Liver',
    units: ['U/L', 'IU/L'],
    defaultUnit: 'U/L',
  },
  {
    code: 'alt',
    name: 'ALT (SGPT)',
    category: 'Liver',
    units: ['U/L', 'IU/L'],
    defaultUnit: 'U/L',
  },
  {
    code: 'bilirubin',
    name: 'Total Bilirubin',
    category: 'Liver',
    units: ['mg/dL', 'umol/L'],
    defaultUnit: 'mg/dL',
  },
  {
    code: 'alkaline_phosphatase',
    name: 'Alkaline Phosphatase',
    category: 'Liver',
    units: ['U/L', 'IU/L'],
    defaultUnit: 'U/L',
  },
  // Thyroid
  {
    code: 'tsh',
    name: 'TSH',
    category: 'Thyroid',
    units: ['mIU/L', 'uIU/mL'],
    defaultUnit: 'mIU/L',
  },
  // Coagulation
  {
    code: 'd_dimer',
    name: 'D-Dimer',
    category: 'Coagulation',
    units: ['ng/mL', 'ug/L', 'mg/L FEU'],
    defaultUnit: 'ng/mL',
  },
];

// Group labs by category
const LAB_CATEGORIES = AVAILABLE_LABS.reduce((acc, lab) => {
  if (!acc[lab.category]) {
    acc[lab.category] = [];
  }
  acc[lab.category].push(lab);
  return acc;
}, {} as Record<string, typeof AVAILABLE_LABS>);

export default function LabInputPage() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();
  const [patient, setPatient] = useState<any>(null);
  const [labs, setLabs] = useState<LabInput[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);

  // Form state for new lab
  const [selectedLab, setSelectedLab] = useState('troponin');
  const [value, setValue] = useState('');
  const [unit, setUnit] = useState('ng/L');
  const [refLow, setRefLow] = useState('');
  const [refHigh, setRefHigh] = useState('');

  useEffect(() => {
    if (!isLoaded) return;

    if (!hasConsent) {
      router.push('/disclaimer');
      return;
    }

    const patientData = sessionStorage.getItem('lab_patient');
    if (!patientData) {
      router.push('/labs');
      return;
    }
    setPatient(JSON.parse(patientData));
    setIsReady(true);
  }, [hasConsent, isLoaded, router]);

  const addLab = () => {
    if (!value) return;

    const labInfo = AVAILABLE_LABS.find((l) => l.code === selectedLab);
    if (!labInfo) return;

    const newLab: LabInput = {
      test_code: selectedLab,
      value: parseFloat(value),
      unit,
      reference_low: refLow ? parseFloat(refLow) : undefined,
      reference_high: refHigh ? parseFloat(refHigh) : undefined,
    };

    setLabs([...labs, newLab]);
    setValue('');
    setRefLow('');
    setRefHigh('');
  };

  const removeLab = (index: number) => {
    setLabs(labs.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    if (labs.length === 0) {
      setError('Please add at least one lab result');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const result = await api.interpretLabs(patient, labs, generateSessionId());
      sessionStorage.setItem('lab_result', JSON.stringify(result));
      router.push('/labs/results');
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isLoaded || !isReady) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  const currentLabInfo = AVAILABLE_LABS.find((l) => l.code === selectedLab);

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Enter Your Lab Results
        </h1>
        <p className="text-gray-600">
          Add your lab test results below. Include reference ranges if available.
        </p>
      </div>

      {/* Add Lab Form */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Add Lab Result</h2>

        <div className="space-y-4">
          <div>
            <label className="label">Lab Test</label>
            <select
              value={selectedLab}
              onChange={(e) => {
                setSelectedLab(e.target.value);
                const lab = AVAILABLE_LABS.find((l) => l.code === e.target.value);
                if (lab) setUnit(lab.defaultUnit);
              }}
              className="input"
            >
              {Object.entries(LAB_CATEGORIES).map(([category, categoryLabs]) => (
                <optgroup key={category} label={category}>
                  {categoryLabs.map((lab) => (
                    <option key={lab.code} value={lab.code}>
                      {lab.name}
                    </option>
                  ))}
                </optgroup>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Value</label>
              <input
                type="number"
                value={value}
                onChange={(e) => setValue(e.target.value)}
                className="input"
                placeholder="Enter value"
                step="any"
              />
            </div>
            <div>
              <label className="label">Unit</label>
              <select
                value={unit}
                onChange={(e) => setUnit(e.target.value)}
                className="input"
              >
                {currentLabInfo?.units.map((u) => (
                  <option key={u} value={u}>{u}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Reference Range Low (optional)</label>
              <input
                type="number"
                value={refLow}
                onChange={(e) => setRefLow(e.target.value)}
                className="input"
                placeholder="e.g., 0"
                step="any"
              />
            </div>
            <div>
              <label className="label">Reference Range High (optional)</label>
              <input
                type="number"
                value={refHigh}
                onChange={(e) => setRefHigh(e.target.value)}
                className="input"
                placeholder="e.g., 14"
                step="any"
              />
            </div>
          </div>

          <button
            onClick={addLab}
            disabled={!value}
            className="btn btn-secondary w-full"
          >
            Add Lab Result
          </button>
        </div>
      </div>

      {/* Added Labs */}
      {labs.length > 0 && (
        <div className="card mb-6">
          <h2 className="text-lg font-semibold mb-4">Your Lab Results</h2>
          <div className="space-y-3">
            {labs.map((lab, index) => {
              const labInfo = AVAILABLE_LABS.find((l) => l.code === lab.test_code);
              return (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div>
                    <span className="font-medium">{labInfo?.name}</span>
                    <span className="text-gray-600 ml-2">
                      {lab.value} {lab.unit}
                    </span>
                    {(lab.reference_low !== undefined || lab.reference_high !== undefined) && (
                      <span className="text-gray-500 text-sm ml-2">
                        (ref: {lab.reference_low ?? '?'} - {lab.reference_high ?? '?'})
                      </span>
                    )}
                  </div>
                  <button
                    onClick={() => removeLab(index)}
                    className="text-red-600 hover:text-red-800"
                  >
                    Remove
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      <div className="flex gap-4">
        <button
          onClick={() => router.back()}
          className="flex-1 btn btn-secondary"
          disabled={isSubmitting}
        >
          Back
        </button>
        <button
          onClick={handleSubmit}
          className="flex-1 btn btn-primary"
          disabled={isSubmitting || labs.length === 0}
        >
          {isSubmitting ? 'Processing...' : 'Get Interpretation'}
        </button>
      </div>
    </div>
  );
}
