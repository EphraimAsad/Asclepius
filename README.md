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
| Containers | Docker + docker-compose |

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
│   │   └── lib/             # API client, schemas
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
│   ├── pathways/            # Symptom pathways (chest_pain, etc.)
│   ├── labs/                # Lab test definitions
│   ├── catalogs/            # Explanations, safety warnings
│   └── compiled/            # Compiled master rulebook
│
├── scripts/
│   ├── compile_rules.py     # Compiles rules into single JSON
│   └── validate_rules.py    # Validates against schema
│
├── docker-compose.yml
├── README.md
├── Context.md               # Project status for collaboration
└── currentplan.txt          # Implementation plan
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
    "patient": {"age": 55, "sex": "male", "comorbidities": ["diabetes"], "medications": []},
    "symptoms": {"chief_complaint": "chest_pain", "symptoms": {"chest_pressure": true, "shortness_of_breath": true}},
    "labs": [],
    "session_id": "test123"
  }'
```

**Response:**
```json
{
  "disposition": "ER_NOW",
  "priority": "critical",
  "matched_rule_ids": ["cp_high_acuity"],
  "reason_codes": ["POSSIBLE_ACS", "DIABETES_CARDIAC_RISK"],
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
| URGENT_CARE_TODAY | Seek urgent care today | Amber |
| PRIMARY_CARE_24_72H | See primary care within 1-3 days | Yellow |
| SELF_CARE | Manage at home with monitoring | Green |

## Current Rules

### Global Emergency Rules (7 rules)
- Cardiac arrest signs → CALL_911
- Stroke (FAST criteria) → CALL_911
- Severe breathing difficulty → CALL_911
- Anaphylaxis → CALL_911
- Uncontrolled bleeding → CALL_911
- Loss of consciousness → CALL_911
- Classic heart attack (chest pain + radiation + sweating) → CALL_911

### Risk Modifiers (4 rules)
- Diabetes → Escalate by one level (max ER_NOW)
- Prior heart attack → Escalate by one level
- Age 65+ with cardiac symptoms → Minimum URGENT_CARE_TODAY
- Hypertension with chest pain → Add reason code

### Triage Pathways (1 pathway)
- **Chest Pain**: Evaluates pressure, shortness of breath, radiation, sweating, etc.

### Lab Tests (1 test)
- **Troponin**: Derives NORMAL/HIGH/CRITICAL_HIGH status, with urgency rules

## Testing

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

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

## License

This project is for educational purposes only.

## Contributing

Contributions welcome. Please ensure all rules follow safety-first principles and include appropriate explanations and safety warnings.
