'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useConsent } from '@/hooks/useConsent';
import { patientSchema, COMORBIDITY_OPTIONS } from '@/lib/schemas/patient';
import { CHIEF_COMPLAINTS } from '@/lib/schemas/symptoms';

const triageStartSchema = patientSchema.extend({
  chief_complaint: z.string().min(1, 'Please select your main concern'),
});

type TriageStartData = z.infer<typeof triageStartSchema>;

export default function TriagePage() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();
  const [selectedComorbidities, setSelectedComorbidities] = useState<string[]>([]);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<TriageStartData>({
    resolver: zodResolver(triageStartSchema),
    defaultValues: {
      comorbidities: [],
      medications: [],
    },
  });

  useEffect(() => {
    if (!isLoaded) return;
    if (!hasConsent) {
      router.push('/disclaimer');
    }
  }, [hasConsent, isLoaded, router]);

  const toggleComorbidity = (value: string) => {
    const updated = selectedComorbidities.includes(value)
      ? selectedComorbidities.filter((c) => c !== value)
      : [...selectedComorbidities, value];
    setSelectedComorbidities(updated);
    setValue('comorbidities', updated);
  };

  const onSubmit = (data: TriageStartData) => {
    // Store in sessionStorage for next page
    sessionStorage.setItem('triage_patient', JSON.stringify({
      age: data.age,
      sex: data.sex,
      comorbidities: data.comorbidities,
      medications: data.medications,
    }));
    sessionStorage.setItem('triage_chief_complaint', data.chief_complaint);
    router.push('/triage/symptoms');
  };

  if (!isLoaded) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  if (!hasConsent) return null;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Symptom Assessment
        </h1>
        <p className="text-gray-600">
          Please provide some basic information to help us understand your situation.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Patient Info */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Basic Information</h2>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="label">Age</label>
              <input
                type="number"
                {...register('age', { valueAsNumber: true })}
                className="input"
                placeholder="Enter your age"
              />
              {errors.age && (
                <p className="error-text">{errors.age.message}</p>
              )}
            </div>

            <div>
              <label className="label">Sex</label>
              <select {...register('sex')} className="input">
                <option value="">Select...</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
              {errors.sex && (
                <p className="error-text">{errors.sex.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Comorbidities */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">
            Medical History (select all that apply)
          </h2>

          <div className="grid grid-cols-2 gap-3">
            {COMORBIDITY_OPTIONS.map((option) => (
              <label
                key={option.value}
                className={`flex items-center gap-2 p-3 rounded-lg border cursor-pointer transition-colors ${
                  selectedComorbidities.includes(option.value)
                    ? 'bg-blue-50 border-blue-300'
                    : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                <input
                  type="checkbox"
                  checked={selectedComorbidities.includes(option.value)}
                  onChange={() => toggleComorbidity(option.value)}
                  className="h-4 w-4 text-blue-600 rounded"
                />
                <span className="text-sm">{option.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Chief Complaint */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">
            What is your main concern today?
          </h2>

          <div className="space-y-3">
            {CHIEF_COMPLAINTS.map((complaint) => (
              <label
                key={complaint.value}
                className="flex items-center gap-3 p-4 rounded-lg border border-gray-200 cursor-pointer hover:bg-gray-50"
              >
                <input
                  type="radio"
                  {...register('chief_complaint')}
                  value={complaint.value}
                  className="h-4 w-4 text-blue-600"
                />
                <span>{complaint.label}</span>
              </label>
            ))}
          </div>
          {errors.chief_complaint && (
            <p className="error-text mt-2">{errors.chief_complaint.message}</p>
          )}
        </div>

        <button type="submit" className="w-full btn btn-primary">
          Continue to Symptoms
        </button>
      </form>
    </div>
  );
}
