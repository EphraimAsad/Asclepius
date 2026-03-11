import { z } from 'zod';

export const patientSchema = z.object({
  age: z
    .number()
    .min(18, 'You must be 18 or older to use this tool')
    .max(120, 'Please enter a valid age'),
  sex: z.enum(['male', 'female', 'other'], {
    required_error: 'Please select your sex',
  }),
  comorbidities: z.array(z.string()).default([]),
  medications: z.array(z.string()).default([]),
});

export type PatientFormData = z.infer<typeof patientSchema>;

export const COMORBIDITY_OPTIONS = [
  { value: 'diabetes', label: 'Diabetes' },
  { value: 'hypertension', label: 'High Blood Pressure' },
  { value: 'heart_disease', label: 'Heart Disease' },
  { value: 'prior_mi', label: 'Previous Heart Attack' },
  { value: 'copd', label: 'COPD/Lung Disease' },
  { value: 'asthma', label: 'Asthma' },
  { value: 'kidney_disease', label: 'Kidney Disease' },
  { value: 'liver_disease', label: 'Liver Disease' },
  { value: 'cancer', label: 'Cancer' },
  { value: 'immunocompromised', label: 'Immunocompromised' },
];
