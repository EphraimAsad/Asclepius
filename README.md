# Asclepius

A **rules-first AI medical triage** and **lab-result interpretation** web application for US adult users (18+).

> **IMPORTANT DISCLAIMER**: This tool is for **educational purposes only**. It is NOT for diagnosis, treatment prescription, or medical emergencies. Always consult with a healthcare professional for medical advice.

## Overview

Asclepius is a care navigation and education tool that uses deterministic rules (not AI/LLM for decisions) to provide guidance on appropriate levels of care based on symptoms and lab results.

### Key Principles

- **Rules-First**: All triage decisions are made by deterministic rules, not AI
- **Safety-First**: Always prefers escalation over false reassurance
- **Auditable**: Every matched rule is logged for transparency
- **Adults Only**: Designed for users 18 years and older
- **US-Focused**: Wording and care levels appropriate for US healthcare

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js 14+ / TypeScript / Tailwind CSS |
| Forms | React Hook Form + Zod validation |
| Backend | FastAPI / Python 3.11+ / Pydantic v2 |
| Database | PostgreSQL (for audit logging) |
| Rules | JSON-based with JSON Schema validation |
| LLM Enhancement | Ollama (local) / OpenAI / Anthropic (optional) |
| Testing | pytest (backend), Vitest (frontend), Playwright (E2E) |
| Containers | Docker + docker-compose |
| CI/CD | GitHub Actions |

## Quick Start

### Option 1: Local Development (Recommended for Development)

**Prerequisites:**
- Python 3.11+
- Node.js 20+

**Step 1: Compile the rules**
```bash
cd C:\Asclepius
python scripts/compile_rules.py
```

**Step 2: Start the backend**
```bash
cd C:\Asclepius\backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Step 3: Start the frontend (new terminal)**
```bash
cd C:\Asclepius\frontend
npm install
npm run dev
```

**Step 4: Open in browser**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Option 2: Docker (Production-like)

**Prerequisites:**
- Docker Desktop (must be running!)

```bash
cd C:\Asclepius
python scripts/compile_rules.py
docker-compose up --build
```

## Project Structure

```
C:\Asclepius\
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js App Router pages
│   │   │   ├── disclaimer/  # Consent gate (required first)
│   │   │   ├── home/        # Main menu
│   │   │   ├── triage/      # Symptom assessment flow
│   │   │   └── labs/        # Lab interpretation flow
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── lib/             # API client, schemas
│   │   └── __tests__/       # Vitest unit tests
│   ├── e2e/                 # Playwright E2E tests
│   ├── vitest.config.ts
│   ├── playwright.config.ts
│   ├── package.json
│   └── Dockerfile
│
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── models/          # Pydantic models
│   │   ├── engine/          # Rules engine components
│   │   └── main.py          # FastAPI app
│   ├── tests/               # pytest tests
│   ├── requirements.txt
│   └── Dockerfile
│
├── rules/                    # All triage rules (JSON)
│   ├── schema/              # JSON Schema for validation
│   ├── core/                # Global emergency rules, risk modifiers
│   ├── pathways/            # 21 symptom pathways
│   ├── labs/                # 21 lab test definitions
│   ├── catalogs/            # Explanations, safety warnings
│   └── compiled/            # Compiled master rulebook
│
├── scripts/
│   ├── compile_rules.py     # Compiles rules into single JSON
│   └── validate_rules.py    # Validates against schema
│
├── .github/workflows/       # CI/CD configuration
│   └── ci.yml
│
├── docker-compose.yml
├── README.md
└── Context.md               # Project status for collaboration
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/triage/evaluate` | Evaluate symptoms, return disposition |
| POST | `/api/v1/labs/interpret` | Interpret lab results |
| POST | `/api/v1/rules/validate` | Validate the compiled rulebook |

### Example: Triage Evaluation

```bash
curl -X POST http://localhost:8000/api/v1/triage/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "patient": {"age": 55, "sex": "male", "medical_history": {"diabetes": true}},
    "symptoms": {"chief_complaint": "chest_pain", "symptoms": {"chest_pressure": true, "shortness_of_breath": true}},
    "session_id": "test123"
  }'
```

**Response:**
```json
{
  "disposition": "ER_NOW",
  "priority": "critical",
  "matched_rule_ids": ["cp_high_acuity"],
  "reason_codes": ["POSSIBLE_ACS"],
  "explanation": "Your symptoms include chest pressure combined with shortness of breath...",
  "safety_warnings": ["If your symptoms worsen...seek emergency care immediately."],
  "disclaimer": "This is not a medical diagnosis..."
}
```

## Rules Engine

The triage engine follows an **8-step deterministic evaluation**:

1. **Derive lab statuses** from results
2. **Run global emergency rules** (CALL_911 - never overridden)
3. **Evaluate triage pathway rules** based on chief complaint
4. **Apply risk modifiers** (diabetes, prior MI, age, etc.)
5. **Run lab urgency rules**
6. **Apply symptom-lab escalation rules**
7. **Select highest urgency disposition**
8. **Assemble structured output** with explanations

### Disposition Levels (Highest to Lowest Urgency)

| Level | Description | Color |
|-------|-------------|-------|
| CALL_911 | Medical emergency - call 911 immediately | Red |
| ER_NOW | Go to emergency room now | Orange |
| URGENT_CARE_TODAY | Seek urgent care today | Yellow |
| PRIMARY_CARE_24_72H | See primary care within 1-3 days | Blue |
| SELF_CARE | Manage at home with monitoring | Green |

## Current Rules

### Compiled Rulebook Stats
- **Global emergency rules**: 7
- **Risk modifiers**: 4
- **Triage pathways**: 21
- **Lab tests**: 21
- **Symptom-lab escalation rules**: 2
- **Explanation catalog entries**: 234
- **Safety net entries**: 14
- **Reason codes**: 162

### Triage Pathways (21)

| Pathway | Description |
|---------|-------------|
| Chest Pain | Cardiac and pulmonary symptoms |
| Shortness of Breath | Respiratory distress evaluation |
| Abdominal Pain | GI and surgical emergencies |
| Headache | Neurological symptoms |
| Dizziness | Vertigo and syncope |
| Fever | Infection and sepsis signs |
| Back Pain | Spinal emergencies |
| Nausea/Vomiting | GI symptoms and dehydration |
| Fatigue | Weakness and systemic illness |
| Cough | Respiratory conditions |
| Sore Throat | Airway and infection |
| Urinary Symptoms | UTI and kidney issues |
| Skin Rash | Allergic and infectious rashes |
| Joint Pain | Arthritis and septic joints |
| Anxiety/Panic | Mental health crisis |
| Palpitations | Cardiac arrhythmias |
| Numbness/Tingling | Neurological symptoms |
| Vision Changes | Eye emergencies |
| Ear Pain | Ear infections |
| Allergic Reaction | Anaphylaxis screening |
| Leg Swelling | DVT and PE concerns |

### Lab Tests (21)

| Category | Tests |
|----------|-------|
| Cardiac | Troponin |
| Metabolic | Glucose, HbA1c |
| Hematology | Hemoglobin, Hematocrit, WBC, Platelet |
| Renal | Creatinine, BUN |
| Electrolytes | Sodium, Potassium, Chloride, CO2, Calcium, Magnesium |
| Liver | AST, ALT, Bilirubin, Alkaline Phosphatase |
| Thyroid | TSH |
| Coagulation | D-Dimer |

## Testing

### Backend Tests
```bash
cd backend
pytest -v
```

### Frontend Unit Tests
```bash
cd frontend
npm test           # Watch mode
npm run test:run   # Single run
```

### Frontend E2E Tests
```bash
cd frontend
npm run test:e2e      # Headless
npm run test:e2e:ui   # Interactive UI
```

### CI/CD

The project includes GitHub Actions CI that:
- Runs backend tests (pytest)
- Runs frontend unit tests (Vitest)
- Runs frontend E2E tests (Playwright)
- Validates the compiled rulebook
- Builds Docker images

## Adding New Rules

1. Create JSON file in appropriate directory:
   - `rules/pathways/` for symptom pathways
   - `rules/labs/` for lab tests
   - `rules/core/` for global rules

2. Add catalog entries to:
   - `rules/catalogs/explanations.json`
   - `rules/catalogs/safety_nets.json`
   - `rules/catalogs/reason_codes.json`

3. Compile and validate:
   ```bash
   python scripts/compile_rules.py
   python scripts/validate_rules.py
   ```

## Safety Features

- Global emergency rules (CALL_911) can never be overridden
- Age 18+ validation enforced at API level
- All matched rules logged for audit trail
- LLM only used for explanations, never for decisions
- Persistent "not a diagnosis" disclaimer throughout UI
- Consent gate required before accessing any features

## LLM Enhancement (Optional)

Asclepius optionally uses LLM to enhance explanations and generate follow-up questions. **LLM never makes triage decisions** - all dispositions come from deterministic rules.

### Supported Providers

| Provider | Status | Use Case |
|----------|--------|----------|
| Ollama | Full support | Local/private deployment |
| OpenAI | Stub (future) | Cloud deployment |
| Anthropic | Stub (future) | Cloud deployment |

### Configuration

Set these environment variables (or in `.env` file):

```env
# Enable/disable LLM enhancement
LLM_ENABLED=true

# Provider: "ollama", "openai", "anthropic"
LLM_PROVIDER=ollama

# Model name (provider-specific)
LLM_MODEL=qwen3.5:4b

# Ollama endpoint (for local deployment)
LLM_BASE_URL=http://127.0.0.1:11434

# API key (for OpenAI/Anthropic)
LLM_API_KEY=sk-...

# Timeout for LLM requests (seconds)
LLM_TIMEOUT_SECONDS=60.0

# Cache TTL for identical requests (seconds)
LLM_CACHE_TTL_SECONDS=3600
```

### Using with Ollama (Local)

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull qwen3.5:4b`
3. Start Ollama: `ollama serve`
4. Set environment variables and start the backend

### Features

- **Explanation Enhancement**: Makes rule-based explanations clearer and more empathetic
- **Follow-up Questions**: Generates questions patients should be prepared to answer
- **Caching**: Identical symptom combinations use cached responses
- **Graceful Fallback**: If LLM fails/times out, original explanation is used

### Response Fields

When LLM is enabled, triage responses include:

```json
{
  "disposition": "ER_NOW",
  "explanation": "Enhanced, patient-friendly explanation...",
  "follow_up_questions": [
    "When did your symptoms start?",
    "Have you experienced this before?",
    "Are you taking any medications?"
  ],
  "llm_enhanced": true
}
```

## License

This project is for educational purposes only.

## Contributing

Contributions welcome. Please ensure all rules follow safety-first principles and include appropriate explanations and safety warnings.
