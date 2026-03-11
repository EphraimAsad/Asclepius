#!/usr/bin/env python3
"""
Asclepius Rule Compiler

Compiles individual rule files from rules/ subdirectories into a single
compiled_rulebook.json that the backend loads at startup.
"""

import json
import os
from pathlib import Path

RULES_DIR = Path('./rules')
COMPILED_RULEBOOK_PATH = RULES_DIR / 'compiled' / 'compiled_rulebook.json'


def load_json_files(directory: Path) -> list:
    """Load all JSON files from a directory."""
    items = []
    if directory.exists():
        for filepath in sorted(directory.glob('*.json')):
            with open(filepath, 'r', encoding='utf-8') as f:
                items.append(json.load(f))
    return items


def load_catalog_file(filepath: Path) -> dict:
    """Load a catalog JSON file (key-value pairs)."""
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def compile_rules():
    """Compile all rules into a single rulebook."""

    # Ensure compiled directory exists
    compiled_dir = RULES_DIR / 'compiled'
    compiled_dir.mkdir(parents=True, exist_ok=True)

    compiled_rulebook = {
        "schema_version": "1.0.0",
        "engine_metadata": {
            "name": "Asclepius Rules Engine",
            "jurisdiction": "US_ADULT_GENERAL",
            "intended_use": "care_navigation_and_result_explanation",
            "not_for": ["diagnosis", "treatment_prescription", "pediatric_use_under_18"]
        },
        "global_emergency_rules": [],
        "risk_modifiers": [],
        "triage_pathways": [],
        "lab_tests": [],
        "symptom_lab_escalation_rules": [],
        "explanation_catalog": {},
        "safety_net_catalog": {},
        "reason_codes": {}
    }

    # Load global emergency rules from core/
    core_dir = RULES_DIR / 'core'
    if core_dir.exists():
        # Load global emergencies
        emergencies_file = core_dir / 'global_emergencies.json'
        if emergencies_file.exists():
            with open(emergencies_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                compiled_rulebook['global_emergency_rules'] = data.get('global_emergency_rules', [])

        # Load risk modifiers
        modifiers_file = core_dir / 'risk_modifiers.json'
        if modifiers_file.exists():
            with open(modifiers_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                compiled_rulebook['risk_modifiers'] = data.get('risk_modifiers', [])

        # Load symptom-lab escalation rules
        escalation_file = core_dir / 'symptom_lab_escalation.json'
        if escalation_file.exists():
            with open(escalation_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                compiled_rulebook['symptom_lab_escalation_rules'] = data.get('symptom_lab_escalation_rules', [])

    # Load triage pathways
    pathways_dir = RULES_DIR / 'pathways'
    compiled_rulebook['triage_pathways'] = load_json_files(pathways_dir)

    # Load lab test definitions
    labs_dir = RULES_DIR / 'labs'
    compiled_rulebook['lab_tests'] = load_json_files(labs_dir)

    # Load catalogs
    catalogs_dir = RULES_DIR / 'catalogs'
    if catalogs_dir.exists():
        compiled_rulebook['explanation_catalog'] = load_catalog_file(
            catalogs_dir / 'explanations.json'
        )
        compiled_rulebook['safety_net_catalog'] = load_catalog_file(
            catalogs_dir / 'safety_nets.json'
        )
        compiled_rulebook['reason_codes'] = load_catalog_file(
            catalogs_dir / 'reason_codes.json'
        )

    # Write the compiled rulebook
    with open(COMPILED_RULEBOOK_PATH, 'w', encoding='utf-8') as outfile:
        json.dump(compiled_rulebook, outfile, indent=2)

    print(f"Compiled rulebook written to {COMPILED_RULEBOOK_PATH}")
    print(f"  - Global emergency rules: {len(compiled_rulebook['global_emergency_rules'])}")
    print(f"  - Risk modifiers: {len(compiled_rulebook['risk_modifiers'])}")
    print(f"  - Triage pathways: {len(compiled_rulebook['triage_pathways'])}")
    print(f"  - Lab tests: {len(compiled_rulebook['lab_tests'])}")
    print(f"  - Symptom-lab escalation rules: {len(compiled_rulebook['symptom_lab_escalation_rules'])}")
    print(f"  - Explanation catalog entries: {len(compiled_rulebook['explanation_catalog'])}")
    print(f"  - Safety net catalog entries: {len(compiled_rulebook['safety_net_catalog'])}")
    print(f"  - Reason codes: {len(compiled_rulebook['reason_codes'])}")


if __name__ == '__main__':
    compile_rules()
