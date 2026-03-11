"""
Rulebook loader for the rules engine.

Loads and validates the compiled rulebook at application startup.
"""

import json
from pathlib import Path
from typing import Any

import jsonschema
from pydantic import ValidationError

from app.models.rules import Rulebook


class RulebookLoader:
    """Loads and validates the compiled rulebook."""

    def __init__(
        self,
        rulebook_path: str | Path = "./rules/compiled/compiled_rulebook.json",
        schema_path: str | Path = "./rules/schema/rulebook.schema.json"
    ):
        self.rulebook_path = Path(rulebook_path)
        self.schema_path = Path(schema_path)

    def load(self) -> Rulebook:
        """
        Load and validate the rulebook.

        Returns:
            The validated Rulebook

        Raises:
            FileNotFoundError: If rulebook or schema file not found
            jsonschema.ValidationError: If JSON schema validation fails
            pydantic.ValidationError: If Pydantic validation fails
        """
        # Load the raw JSON
        rulebook_data = self._load_json(self.rulebook_path)

        # Validate against JSON schema (if available)
        if self.schema_path.exists():
            self._validate_schema(rulebook_data)

        # Parse into Pydantic model
        rulebook = self._parse_rulebook(rulebook_data)

        # Run additional validations
        self._validate_references(rulebook)

        return rulebook

    def _load_json(self, path: Path) -> dict[str, Any]:
        """Load a JSON file."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _validate_schema(self, data: dict[str, Any]) -> None:
        """Validate data against JSON schema."""
        schema = self._load_json(self.schema_path)
        jsonschema.validate(instance=data, schema=schema)

    def _parse_rulebook(self, data: dict[str, Any]) -> Rulebook:
        """Parse JSON data into a Rulebook model."""
        return Rulebook.model_validate(data)

    def _validate_references(self, rulebook: Rulebook) -> None:
        """
        Validate that all referenced keys exist in catalogs.

        Raises:
            ValueError: If any referenced key is missing
        """
        errors = []

        # Collect all explanation keys referenced
        all_explanation_keys = set()
        all_safety_net_keys = set()

        # From global emergency rules
        for rule in rulebook.global_emergency_rules:
            all_explanation_keys.update(rule.explanation_keys)
            all_safety_net_keys.update(rule.safety_net_keys)

        # From triage pathways
        for pathway in rulebook.triage_pathways:
            for rule in pathway.rules:
                all_explanation_keys.update(rule.explanation_keys)
                all_safety_net_keys.update(rule.safety_net_keys)

        # From lab tests
        for lab_test in rulebook.lab_tests:
            for rule in lab_test.urgency_rules:
                all_explanation_keys.update(rule.explanation_keys)
                all_safety_net_keys.update(rule.safety_net_keys)

        # From symptom-lab escalation rules
        for rule in rulebook.symptom_lab_escalation_rules:
            all_explanation_keys.update(rule.explanation_keys)
            all_safety_net_keys.update(rule.safety_net_keys)

        # Check explanation keys
        for key in all_explanation_keys:
            if key not in rulebook.explanation_catalog:
                errors.append(f"Missing explanation_catalog entry: {key}")

        # Check safety net keys
        for key in all_safety_net_keys:
            if key not in rulebook.safety_net_catalog:
                errors.append(f"Missing safety_net_catalog entry: {key}")

        if errors:
            raise ValueError(
                "Rulebook validation failed:\n" + "\n".join(errors)
            )

    def validate_only(self) -> list[str]:
        """
        Validate the rulebook and return a list of issues.

        Returns:
            List of validation error messages (empty if valid)
        """
        issues = []

        try:
            rulebook_data = self._load_json(self.rulebook_path)
        except FileNotFoundError as e:
            return [str(e)]
        except json.JSONDecodeError as e:
            return [f"Invalid JSON: {e}"]

        # Schema validation
        if self.schema_path.exists():
            try:
                self._validate_schema(rulebook_data)
            except jsonschema.ValidationError as e:
                issues.append(f"Schema validation error: {e.message}")
                return issues

        # Pydantic validation
        try:
            rulebook = self._parse_rulebook(rulebook_data)
        except ValidationError as e:
            issues.append(f"Model validation error: {e}")
            return issues

        # Reference validation
        try:
            self._validate_references(rulebook)
        except ValueError as e:
            issues.extend(str(e).split("\n")[1:])

        return issues
