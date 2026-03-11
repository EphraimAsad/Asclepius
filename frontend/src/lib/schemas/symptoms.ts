import { z } from 'zod';

export const symptomSchema = z.object({
  chief_complaint: z.string().min(1, 'Please select your main concern'),
  symptoms: z.record(z.boolean()).default({}),
  duration_hours: z.number().min(0).optional(),
  severity: z.number().min(1).max(10).optional(),
});

export type SymptomFormData = z.infer<typeof symptomSchema>;

export const CHIEF_COMPLAINTS = [
  { value: 'chest_pain', label: 'Chest Pain or Discomfort' },
  { value: 'shortness_of_breath', label: 'Shortness of Breath' },
  { value: 'abdominal_pain', label: 'Abdominal Pain' },
  { value: 'headache', label: 'Headache' },
  { value: 'dizziness', label: 'Dizziness / Vertigo' },
  { value: 'fever', label: 'Fever' },
  { value: 'back_pain', label: 'Back Pain' },
  { value: 'nausea_vomiting', label: 'Nausea / Vomiting' },
  { value: 'fatigue', label: 'Fatigue / Weakness' },
  { value: 'cough', label: 'Cough' },
  { value: 'sore_throat', label: 'Sore Throat' },
  { value: 'urinary_symptoms', label: 'Urinary Symptoms' },
  { value: 'skin_rash', label: 'Skin Rash' },
  { value: 'joint_pain', label: 'Joint Pain' },
  { value: 'anxiety_panic', label: 'Anxiety / Panic' },
  { value: 'palpitations', label: 'Heart Palpitations' },
  { value: 'numbness_tingling', label: 'Numbness / Tingling' },
  { value: 'vision_changes', label: 'Vision Changes' },
  { value: 'ear_pain', label: 'Ear Pain' },
  { value: 'allergic_reaction', label: 'Allergic Reaction' },
  { value: 'leg_swelling', label: 'Leg Swelling / Pain' },
];

export const EMERGENCY_SYMPTOMS = [
  { field: 'unresponsive', label: 'Person is unresponsive' },
  { field: 'not_breathing', label: 'Not breathing or gasping' },
  { field: 'facial_drooping', label: 'Sudden face drooping' },
  { field: 'arm_weakness_sudden', label: 'Sudden arm weakness' },
  { field: 'speech_difficulty_sudden', label: 'Sudden difficulty speaking' },
  { field: 'lips_turning_blue', label: 'Lips or fingernails turning blue' },
  { field: 'bleeding_not_stopping', label: "Severe bleeding that won't stop" },
];

export const CHEST_PAIN_SYMPTOMS = [
  { field: 'chest_pressure', label: 'Pressure, squeezing, or tightness in chest' },
  { field: 'shortness_of_breath', label: 'Shortness of breath' },
  { field: 'radiation_to_arm_jaw_back', label: 'Pain spreading to arm, jaw, or back' },
  { field: 'sweating', label: 'Unusual sweating (cold sweat)' },
  { field: 'nausea', label: 'Nausea or vomiting' },
  { field: 'fainting', label: 'Fainting or feeling faint' },
  { field: 'palpitations', label: 'Heart racing or palpitations' },
];

export const SHORTNESS_OF_BREATH_SYMPTOMS = [
  { field: 'sob_at_rest', label: 'Shortness of breath at rest' },
  { field: 'sob_with_exertion', label: 'Shortness of breath with activity' },
  { field: 'sudden_onset', label: 'Came on suddenly' },
  { field: 'chest_pain', label: 'Chest pain' },
  { field: 'wheezing', label: 'Wheezing' },
  { field: 'cough', label: 'Cough' },
  { field: 'fever', label: 'Fever' },
  { field: 'leg_swelling', label: 'Leg swelling' },
  { field: 'cant_speak_sentences', label: 'Cannot speak in full sentences' },
  { field: 'blue_lips', label: 'Blue lips or fingernails' },
  { field: 'confused', label: 'Feeling confused' },
];

export const ABDOMINAL_PAIN_SYMPTOMS = [
  { field: 'severe_pain', label: 'Severe pain (8-10/10)' },
  { field: 'sudden_onset', label: 'Came on suddenly' },
  { field: 'rigid_abdomen', label: 'Abdomen feels hard/rigid' },
  { field: 'bloody_stool', label: 'Blood in stool' },
  { field: 'vomiting_blood', label: 'Vomiting blood' },
  { field: 'fever', label: 'Fever' },
  { field: 'nausea', label: 'Nausea' },
  { field: 'diarrhea', label: 'Diarrhea' },
  { field: 'location_right_lower', label: 'Pain in right lower area' },
  { field: 'location_right_upper', label: 'Pain in right upper area' },
];

export const HEADACHE_SYMPTOMS = [
  { field: 'worst_headache_ever', label: 'Worst headache of my life' },
  { field: 'sudden_onset', label: 'Came on very suddenly' },
  { field: 'stiff_neck', label: 'Stiff neck' },
  { field: 'fever', label: 'Fever' },
  { field: 'vision_changes', label: 'Vision changes' },
  { field: 'confusion', label: 'Confusion' },
  { field: 'weakness', label: 'Weakness in arm or leg' },
  { field: 'nausea', label: 'Nausea or vomiting' },
  { field: 'light_sensitivity', label: 'Sensitivity to light' },
  { field: 'recent_head_injury', label: 'Recent head injury' },
];

export const DIZZINESS_SYMPTOMS = [
  { field: 'room_spinning', label: 'Room appears to spin' },
  { field: 'fainting', label: 'Fainted or nearly fainted' },
  { field: 'chest_pain', label: 'Chest pain' },
  { field: 'shortness_of_breath', label: 'Shortness of breath' },
  { field: 'slurred_speech', label: 'Slurred speech' },
  { field: 'weakness_one_side', label: 'Weakness on one side' },
  { field: 'hearing_loss', label: 'Hearing changes' },
  { field: 'nausea', label: 'Nausea' },
  { field: 'worse_with_position', label: 'Worse with head position changes' },
];

export const FEVER_SYMPTOMS = [
  { field: 'high_fever', label: 'Temperature above 101°F / 38.3°C' },
  { field: 'stiff_neck', label: 'Stiff neck' },
  { field: 'confusion', label: 'Confusion or altered mental state' },
  { field: 'rash', label: 'Rash' },
  { field: 'severe_headache', label: 'Severe headache' },
  { field: 'difficulty_breathing', label: 'Difficulty breathing' },
  { field: 'immunocompromised', label: 'Weakened immune system' },
  { field: 'recent_surgery', label: 'Recent surgery' },
  { field: 'cough', label: 'Cough' },
  { field: 'sore_throat', label: 'Sore throat' },
];

export const BACK_PAIN_SYMPTOMS = [
  { field: 'severe_pain', label: 'Severe pain (8-10/10)' },
  { field: 'sudden_onset', label: 'Came on suddenly' },
  { field: 'leg_weakness', label: 'Weakness in legs' },
  { field: 'bowel_bladder_changes', label: 'Loss of bowel or bladder control' },
  { field: 'numbness_legs', label: 'Numbness in legs or groin' },
  { field: 'fever', label: 'Fever' },
  { field: 'recent_trauma', label: 'Recent injury or fall' },
  { field: 'pain_radiating_leg', label: 'Pain shooting down leg' },
  { field: 'worse_at_night', label: 'Worse at night' },
];

export const NAUSEA_VOMITING_SYMPTOMS = [
  { field: 'vomiting_blood', label: 'Vomiting blood or dark material' },
  { field: 'severe_abdominal_pain', label: 'Severe abdominal pain' },
  { field: 'inability_to_keep_fluids', label: "Can't keep any fluids down" },
  { field: 'signs_of_dehydration', label: 'Signs of dehydration (dizzy, dry mouth)' },
  { field: 'headache', label: 'Headache' },
  { field: 'stiff_neck', label: 'Stiff neck' },
  { field: 'fever', label: 'Fever' },
  { field: 'diarrhea', label: 'Diarrhea' },
  { field: 'recent_head_injury', label: 'Recent head injury' },
];

export const FATIGUE_SYMPTOMS = [
  { field: 'sudden_onset', label: 'Came on suddenly' },
  { field: 'chest_pain', label: 'Chest pain' },
  { field: 'shortness_of_breath', label: 'Shortness of breath' },
  { field: 'one_sided_weakness', label: 'Weakness on one side of body' },
  { field: 'slurred_speech', label: 'Slurred speech' },
  { field: 'weight_loss', label: 'Unintentional weight loss' },
  { field: 'fever', label: 'Fever' },
  { field: 'depression_symptoms', label: 'Feeling depressed or hopeless' },
  { field: 'duration_weeks', label: 'Lasting more than 2 weeks' },
];

export const COUGH_SYMPTOMS = [
  { field: 'coughing_blood', label: 'Coughing up blood' },
  { field: 'shortness_of_breath', label: 'Shortness of breath' },
  { field: 'chest_pain', label: 'Chest pain' },
  { field: 'fever', label: 'Fever' },
  { field: 'wheezing', label: 'Wheezing' },
  { field: 'duration_weeks', label: 'Lasting more than 3 weeks' },
  { field: 'weight_loss', label: 'Unintentional weight loss' },
  { field: 'night_sweats', label: 'Night sweats' },
  { field: 'sore_throat', label: 'Sore throat' },
];

export const SORE_THROAT_SYMPTOMS = [
  { field: 'difficulty_breathing', label: 'Difficulty breathing' },
  { field: 'difficulty_swallowing', label: 'Difficulty swallowing' },
  { field: 'drooling', label: 'Unable to swallow saliva (drooling)' },
  { field: 'muffled_voice', label: 'Muffled or "hot potato" voice' },
  { field: 'fever', label: 'Fever' },
  { field: 'swollen_lymph_nodes', label: 'Swollen lymph nodes in neck' },
  { field: 'rash', label: 'Rash' },
  { field: 'cough', label: 'Cough' },
  { field: 'duration_days', label: 'Lasting more than a few days' },
];

export const URINARY_SYMPTOMS = [
  { field: 'blood_in_urine', label: 'Blood in urine' },
  { field: 'severe_flank_pain', label: 'Severe pain in side or back' },
  { field: 'fever', label: 'Fever' },
  { field: 'inability_to_urinate', label: 'Unable to urinate' },
  { field: 'painful_urination', label: 'Painful urination' },
  { field: 'frequency', label: 'Urinating very frequently' },
  { field: 'urgency', label: 'Urgent need to urinate' },
  { field: 'lower_abdominal_pain', label: 'Lower abdominal pain' },
  { field: 'back_pain', label: 'Back pain' },
];

export const SKIN_RASH_SYMPTOMS = [
  { field: 'difficulty_breathing', label: 'Difficulty breathing' },
  { field: 'swelling_face_throat', label: 'Swelling of face or throat' },
  { field: 'fever', label: 'Fever' },
  { field: 'spreading_rapidly', label: 'Spreading rapidly' },
  { field: 'painful_rash', label: 'Painful rash' },
  { field: 'blistering', label: 'Blistering' },
  { field: 'petechiae', label: 'Tiny purple/red dots that don\'t fade with pressure' },
  { field: 'itching', label: 'Itching' },
  { field: 'recent_new_medication', label: 'Started new medication recently' },
];

export const JOINT_PAIN_SYMPTOMS = [
  { field: 'fever', label: 'Fever' },
  { field: 'single_joint_swelling', label: 'Single joint is swollen' },
  { field: 'redness_warmth', label: 'Joint is red and warm' },
  { field: 'recent_injury', label: 'Recent injury' },
  { field: 'multiple_joints', label: 'Multiple joints affected' },
  { field: 'morning_stiffness', label: 'Morning stiffness lasting over an hour' },
  { field: 'rash', label: 'Rash' },
  { field: 'unable_to_bear_weight', label: 'Unable to put weight on joint' },
  { field: 'recent_infection', label: 'Recent infection' },
];

export const ANXIETY_PANIC_SYMPTOMS = [
  { field: 'chest_pain', label: 'Chest pain' },
  { field: 'shortness_of_breath', label: 'Shortness of breath' },
  { field: 'suicidal_thoughts', label: 'Thoughts of harming yourself' },
  { field: 'self_harm_thoughts', label: 'Thoughts of self-harm' },
  { field: 'palpitations', label: 'Heart racing' },
  { field: 'numbness_tingling', label: 'Numbness or tingling' },
  { field: 'sweating', label: 'Sweating' },
  { field: 'trembling', label: 'Trembling or shaking' },
  { field: 'first_episode', label: 'First time experiencing this' },
];

export const PALPITATIONS_SYMPTOMS = [
  { field: 'chest_pain', label: 'Chest pain' },
  { field: 'shortness_of_breath', label: 'Shortness of breath' },
  { field: 'fainting', label: 'Fainted or nearly fainted' },
  { field: 'dizziness', label: 'Dizziness or lightheadedness' },
  { field: 'prolonged_episode', label: 'Lasting more than a few minutes' },
  { field: 'at_rest', label: 'Happening at rest' },
  { field: 'caffeine_use', label: 'Recent caffeine or stimulant use' },
  { field: 'anxiety', label: 'Feeling anxious' },
  { field: 'known_heart_condition', label: 'Known heart condition' },
];

export const NUMBNESS_TINGLING_SYMPTOMS = [
  { field: 'sudden_onset', label: 'Came on suddenly' },
  { field: 'one_sided', label: 'Only on one side of body' },
  { field: 'facial_drooping', label: 'Face drooping' },
  { field: 'slurred_speech', label: 'Slurred speech' },
  { field: 'arm_weakness', label: 'Arm weakness' },
  { field: 'both_hands_feet', label: 'In both hands and/or both feet' },
  { field: 'back_pain', label: 'Back pain' },
  { field: 'bowel_bladder_changes', label: 'Bowel or bladder problems' },
  { field: 'recent_injury', label: 'Recent injury' },
];

export const VISION_CHANGES_SYMPTOMS = [
  { field: 'sudden_vision_loss', label: 'Sudden vision loss' },
  { field: 'one_eye', label: 'Only in one eye' },
  { field: 'headache', label: 'Headache' },
  { field: 'eye_pain', label: 'Eye pain' },
  { field: 'flashing_lights', label: 'Seeing flashing lights' },
  { field: 'floaters', label: 'New floaters (spots/cobwebs)' },
  { field: 'curtain_effect', label: 'Shadow or curtain over vision' },
  { field: 'double_vision', label: 'Seeing double' },
  { field: 'recent_trauma', label: 'Recent eye or head injury' },
];

export const EAR_PAIN_SYMPTOMS = [
  { field: 'fever', label: 'Fever' },
  { field: 'drainage', label: 'Drainage from ear' },
  { field: 'hearing_loss', label: 'Hearing loss' },
  { field: 'dizziness', label: 'Dizziness' },
  { field: 'facial_weakness', label: 'Weakness on one side of face' },
  { field: 'swelling_behind_ear', label: 'Swelling behind ear' },
  { field: 'recent_swimming', label: 'Recent swimming' },
  { field: 'recent_cold', label: 'Recent cold symptoms' },
  { field: 'severe_pain', label: 'Severe pain' },
];

export const ALLERGIC_REACTION_SYMPTOMS = [
  { field: 'difficulty_breathing', label: 'Difficulty breathing' },
  { field: 'throat_tightness', label: 'Throat tightness' },
  { field: 'tongue_swelling', label: 'Tongue swelling' },
  { field: 'face_swelling', label: 'Face swelling' },
  { field: 'widespread_hives', label: 'Hives all over body' },
  { field: 'dizziness', label: 'Dizziness or lightheadedness' },
  { field: 'nausea_vomiting', label: 'Nausea or vomiting' },
  { field: 'known_allergen', label: 'Exposed to known allergen' },
  { field: 'has_epipen', label: 'Have an EpiPen available' },
];

export const LEG_SWELLING_SYMPTOMS = [
  { field: 'one_leg_only', label: 'Only one leg affected' },
  { field: 'calf_pain', label: 'Calf pain or tenderness' },
  { field: 'warmth_redness', label: 'Leg feels warm and looks red' },
  { field: 'shortness_of_breath', label: 'Shortness of breath' },
  { field: 'chest_pain', label: 'Chest pain' },
  { field: 'recent_surgery', label: 'Recent surgery or hospitalization' },
  { field: 'recent_travel', label: 'Recent long travel (flight/car)' },
  { field: 'both_legs', label: 'Both legs affected' },
  { field: 'sudden_onset', label: 'Came on suddenly' },
];

// Symptom map for dynamic lookup
export const SYMPTOM_SETS: Record<string, { field: string; label: string }[]> = {
  chest_pain: CHEST_PAIN_SYMPTOMS,
  shortness_of_breath: SHORTNESS_OF_BREATH_SYMPTOMS,
  abdominal_pain: ABDOMINAL_PAIN_SYMPTOMS,
  headache: HEADACHE_SYMPTOMS,
  dizziness: DIZZINESS_SYMPTOMS,
  fever: FEVER_SYMPTOMS,
  back_pain: BACK_PAIN_SYMPTOMS,
  nausea_vomiting: NAUSEA_VOMITING_SYMPTOMS,
  fatigue: FATIGUE_SYMPTOMS,
  cough: COUGH_SYMPTOMS,
  sore_throat: SORE_THROAT_SYMPTOMS,
  urinary_symptoms: URINARY_SYMPTOMS,
  skin_rash: SKIN_RASH_SYMPTOMS,
  joint_pain: JOINT_PAIN_SYMPTOMS,
  anxiety_panic: ANXIETY_PANIC_SYMPTOMS,
  palpitations: PALPITATIONS_SYMPTOMS,
  numbness_tingling: NUMBNESS_TINGLING_SYMPTOMS,
  vision_changes: VISION_CHANGES_SYMPTOMS,
  ear_pain: EAR_PAIN_SYMPTOMS,
  allergic_reaction: ALLERGIC_REACTION_SYMPTOMS,
  leg_swelling: LEG_SWELLING_SYMPTOMS,
};
