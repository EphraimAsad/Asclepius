'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useConsent } from '@/hooks/useConsent';
import { patientSchema } from '@/lib/schemas/patient';

const labStartSchema = patientSchema;
type LabStartData = z.infer<typeof labStartSchema>;

export default function LabsPage() {
  const router = useRouter();
  const { hasConsent, isLoaded } = useConsent();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LabStartData>({
    resolver: zodResolver(labStartSchema),
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

  const onSubmit = (data: LabStartData) => {
    sessionStorage.setItem('lab_patient', JSON.stringify(data));
    router.push('/labs/input');
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
          Lab Result Interpretation
        </h1>
        <p className="text-gray-600">
          Enter your lab results to get educational information about what they mean.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Basic Information</h2>
          <p className="text-sm text-gray-500 mb-4">
            We need some basic information to provide context for your lab results.
          </p>

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

        <button type="submit" className="w-full btn btn-primary">
          Continue to Lab Input
        </button>
      </form>
    </div>
  );
}
