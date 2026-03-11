"""
Prompt templates for LLM explanation enhancement in Asclepius.

Optimized for small models (gemma:7b) with:
- Shorter prompts (~120 words vs ~400)
- Positive framing instead of negative
- Few-shot examples
- Simple sentence structure
"""

# ==============================
# Explanation Enhancement Prompts
# ==============================

ENHANCEMENT_SYSTEM_PROMPT = """You rewrite medical explanations to be clearer.

TASK: Make the text easier to read. Keep the same meaning.

RULES:
1. Keep all medical recommendations exactly the same
2. Keep the same urgency level
3. Use simpler words
4. Do not add new medical information
5. Do not add diagnoses, treatments, or causes
6. If the text is already clear, return it unchanged

OUTPUT: Only the rewritten text. No commentary.
"""


ENHANCEMENT_USER_PROMPT = """Rewrite this explanation to be clearer. Keep the exact same meaning.

ORIGINAL:
{explanation}

EXAMPLE:
Original: "Your symptoms include chest pressure combined with shortness of breath. This combination can indicate serious conditions requiring evaluation."
Rewritten: "You have chest pressure and shortness of breath together. This combination needs medical evaluation."

Now rewrite the ORIGINAL text above. Output only the rewritten text.
"""


# ==============================
# Follow-up Question Prompts
# ==============================

FOLLOWUP_QUESTIONS_SYSTEM_PROMPT = """You generate questions to help patients prepare for doctor visits.

RULES:
1. Ask about symptom timing, severity, and history
2. Do not suggest diagnoses
3. Do not give medical advice
4. Keep questions under 15 words each

OUTPUT: JSON array of 2-3 questions only.
"""


FOLLOWUP_QUESTIONS_USER_PROMPT = """Generate 2-3 questions a doctor might ask about these symptoms.

Symptoms: {symptoms}
Main concern: {chief_complaint}

EXAMPLE OUTPUT:
["When did your symptoms start?", "Has the pain gotten worse?", "Have you had this before?"]

Output only the JSON array:
"""


# ==============================
# Prompt Formatting Functions
# ==============================

def _format_symptoms(symptoms: dict) -> str:
    """Convert symptoms dict to readable string."""
    symptom_list = ", ".join(
        k.replace("_", " ")
        for k, v in symptoms.items()
        if v is True or (isinstance(v, str) and v)
    )
    return symptom_list if symptom_list else "none specified"


def format_enhancement_prompt(
    explanation: str,
    disposition: str = "",
    chief_complaint: str = "",
    symptoms: dict = None
):
    """Format the enhancement prompt.

    Note: disposition, chief_complaint, symptoms kept for backwards
    compatibility but not used in optimized prompt.
    """
    return ENHANCEMENT_USER_PROMPT.format(explanation=explanation)


def format_followup_prompt(
    chief_complaint: str,
    symptoms: dict,
    disposition: str = ""
):
    """Format the follow-up questions prompt.

    Note: disposition kept for backwards compatibility but not used.
    """
    return FOLLOWUP_QUESTIONS_USER_PROMPT.format(
        chief_complaint=chief_complaint.replace("_", " "),
        symptoms=_format_symptoms(symptoms)
    )