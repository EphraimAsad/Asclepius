"""
Prompt templates for LLM enhancement.

These prompts are designed to enhance explanations while maintaining
safety constraints. The LLM must never:
- Make triage decisions
- Change the disposition
- Diagnose conditions
- Prescribe treatments
- Provide false reassurance
"""

ENHANCEMENT_SYSTEM_PROMPT = """You are a medical education assistant for Asclepius, a triage guidance tool.

Your role is to make medical explanations clearer and more empathetic for patients while preserving the original guidance. You are NOT a doctor and cannot diagnose or prescribe.

STRICT RULES:
1. NEVER change the urgency level or recommended action
2. NEVER diagnose or suggest specific conditions
3. NEVER prescribe medications or treatments
4. NEVER provide false reassurance ("you're probably fine")
5. NEVER contradict the triage recommendation
6. Keep the same core message, just make it clearer
7. Use plain language a patient can understand
8. Be empathetic but direct about urgency when needed"""

ENHANCEMENT_USER_PROMPT = """Enhance this medical explanation to be clearer and more empathetic.

ORIGINAL EXPLANATION:
{explanation}

CONTEXT:
- Recommendation: {disposition}
- Main concern: {chief_complaint}
- Symptoms present: {symptoms}

INSTRUCTIONS:
- Rewrite to be more understandable for a patient
- Keep the same urgency level and core message
- Add helpful context about WHY this guidance applies
- Be empathetic but maintain appropriate urgency

Respond with the enhanced explanation only. No preamble or meta-commentary."""

FOLLOWUP_QUESTIONS_SYSTEM_PROMPT = """You are a medical education assistant helping patients prepare for healthcare visits.

Your role is to generate questions that a patient should be prepared to answer when they seek care. These questions help the healthcare provider understand the patient's situation.

STRICT RULES:
1. NEVER suggest diagnoses
2. NEVER recommend treatments
3. Focus on information gathering only
4. Questions should be relevant to the symptoms
5. Keep questions clear and simple"""

FOLLOWUP_QUESTIONS_USER_PROMPT = """Generate 2-3 questions this patient should be prepared to answer when seeking medical care.

CONTEXT:
- Main concern: {chief_complaint}
- Symptoms present: {symptoms}
- Recommendation: {disposition}

INSTRUCTIONS:
- Questions should help the patient prepare for their visit
- Focus on information a healthcare provider would need
- Include timing, severity, and relevant history
- Do NOT suggest diagnoses or treatments

Respond with ONLY a JSON array of question strings. Example format:
["When did the symptoms start?", "Have you experienced this before?", "Are you taking any medications?"]"""


def format_enhancement_prompt(
    explanation: str,
    disposition: str,
    chief_complaint: str,
    symptoms: dict
) -> str:
    """Format the enhancement prompt with context."""
    symptom_list = ", ".join(
        k.replace("_", " ") for k, v in symptoms.items()
        if v is True or (isinstance(v, str) and v)
    )
    if not symptom_list:
        symptom_list = "none specified"

    return ENHANCEMENT_USER_PROMPT.format(
        explanation=explanation,
        disposition=disposition.replace("_", " "),
        chief_complaint=chief_complaint.replace("_", " "),
        symptoms=symptom_list
    )


def format_followup_prompt(
    chief_complaint: str,
    symptoms: dict,
    disposition: str
) -> str:
    """Format the follow-up questions prompt with context."""
    symptom_list = ", ".join(
        k.replace("_", " ") for k, v in symptoms.items()
        if v is True or (isinstance(v, str) and v)
    )
    if not symptom_list:
        symptom_list = "none specified"

    return FOLLOWUP_QUESTIONS_USER_PROMPT.format(
        chief_complaint=chief_complaint.replace("_", " "),
        symptoms=symptom_list,
        disposition=disposition.replace("_", " ")
    )
