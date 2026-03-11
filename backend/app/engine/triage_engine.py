"""
Main triage engine orchestrator.

Implements the 8-step deterministic evaluation pipeline.
"""

from typing import Any

from app.models.enums import Disposition, Priority, JoinType
from app.models.patient import LabInput
from app.models.request import TriageRequest
from app.models.response import TriageResult, MatchedRule
from app.models.rules import Rulebook, DecisionRule, RiskModifier

from .condition_evaluator import ConditionEvaluator
from .rule_evaluator import RuleEvaluator
from .lab_status_deriver import LabStatusDeriver
from .disposition_selector import DispositionSelector
from .explanation_generator import ExplanationGenerator


class TriageEngine:
    """
    Main triage engine implementing the 8-step deterministic evaluation.

    Evaluation Order:
    1. Derive lab statuses from results
    2. Run global emergency rules
    3. Evaluate triage pathway rules
    4. Apply risk modifiers
    5. Run lab urgency rules
    6. Apply symptom-lab escalation rules
    7. Select highest urgency disposition
    8. Assemble structured output
    """

    def __init__(self, rulebook: Rulebook):
        self.rulebook = rulebook
        self.condition_evaluator = ConditionEvaluator()
        self.rule_evaluator = RuleEvaluator(self.condition_evaluator)
        self.lab_status_deriver = LabStatusDeriver()
        self.disposition_selector = DispositionSelector()
        self.explanation_generator = ExplanationGenerator(rulebook)

    def evaluate(self, request: TriageRequest) -> TriageResult:
        """
        Evaluate a triage request and return the result.

        Args:
            request: The triage request with patient info, symptoms, and labs

        Returns:
            TriageResult with disposition, explanations, and warnings
        """
        # Build evaluation context
        context = self._build_context(request)
        all_matched_rules: list[DecisionRule] = []
        matched_modifiers: list[RiskModifier] = []

        # Step 1: Derive lab statuses
        lab_statuses = self.lab_status_deriver.derive_all_statuses(
            request.labs, self.rulebook.lab_tests
        )
        context["derived"] = {"lab_status": lab_statuses}

        # Step 2: Run global emergency rules (highest priority)
        emergency_matches = self.rule_evaluator.evaluate_rules(
            self.rulebook.global_emergency_rules, context
        )

        if emergency_matches:
            # Global emergencies take immediate precedence
            return self._build_result(
                emergency_matches,
                [],
                lab_statuses,
                is_emergency=True
            )

        # Step 3: Evaluate triage pathway rules
        pathway = self._select_pathway(request.symptoms.chief_complaint)
        if pathway:
            pathway_matches = self.rule_evaluator.evaluate_rules(
                pathway.rules, context
            )
            all_matched_rules.extend(pathway_matches)

        # Step 4: Find matching risk modifiers
        matched_modifiers = self._evaluate_risk_modifiers(context)

        # Step 5: Run lab urgency rules
        for lab_test in self.rulebook.lab_tests:
            lab_matches = self.rule_evaluator.evaluate_rules(
                lab_test.urgency_rules, context
            )
            all_matched_rules.extend(lab_matches)

        # Step 6: Apply symptom-lab escalation rules
        escalation_matches = self.rule_evaluator.evaluate_rules(
            self.rulebook.symptom_lab_escalation_rules, context
        )
        all_matched_rules.extend(escalation_matches)

        # Step 7 & 8: Select disposition and build result
        return self._build_result(
            all_matched_rules,
            matched_modifiers,
            lab_statuses,
            is_emergency=False
        )

    def _build_context(self, request: TriageRequest) -> dict[str, Any]:
        """Build the evaluation context from the request."""
        return {
            "patient": {
                "age": request.patient.age,
                "sex": request.patient.sex,
                "comorbidities": request.patient.comorbidities,
                "medications": request.patient.medications,
            },
            "symptoms": request.symptoms.symptoms,
            "chief_complaint": request.symptoms.chief_complaint,
            "duration_hours": request.symptoms.duration_hours,
            "severity": request.symptoms.severity,
            "labs": {
                lab.test_code: {
                    "value": lab.value,
                    "unit": lab.unit,
                    "reference_low": lab.reference_low,
                    "reference_high": lab.reference_high,
                }
                for lab in request.labs
            },
        }

    def _select_pathway(self, chief_complaint: str):
        """Select the appropriate triage pathway for the complaint."""
        for pathway in self.rulebook.triage_pathways:
            if chief_complaint == pathway.pathway_id:
                return pathway
            if chief_complaint in pathway.chief_complaint_aliases:
                return pathway
        return None

    def _evaluate_risk_modifiers(
        self,
        context: dict[str, Any]
    ) -> list[RiskModifier]:
        """Evaluate risk modifiers and return those that match."""
        matched = []
        for modifier in self.rulebook.risk_modifiers:
            # Evaluate conditions
            results = [
                self.condition_evaluator.evaluate(cond, context)
                for cond in modifier.conditions
            ]

            if modifier.join == JoinType.ALL:
                if all(results):
                    matched.append(modifier)
            elif modifier.join == JoinType.ANY:
                if any(results):
                    matched.append(modifier)

        return matched

    def _build_result(
        self,
        matched_rules: list[DecisionRule],
        matched_modifiers: list[RiskModifier],
        lab_statuses: dict,
        is_emergency: bool
    ) -> TriageResult:
        """Build the final triage result."""

        # Select base disposition from matched rules
        base_disposition = self.disposition_selector.select_highest(
            matched_rules, default=Disposition.SELF_CARE
        )

        # Apply risk modifiers
        final_disposition, applied_modifiers = self.disposition_selector.apply_modifiers(
            base_disposition, matched_modifiers
        )

        # Determine priority
        if matched_rules:
            # Use highest priority from matched rules
            priorities = [rule.priority for rule in matched_rules]
            priority = self._get_highest_priority(priorities)
        else:
            priority = Priority.LOW

        # Generate explanation
        explanation = self.explanation_generator.generate_explanation(matched_rules)

        # Generate safety warnings
        safety_warnings = self.explanation_generator.generate_safety_warnings(
            matched_rules
        )

        # Collect reason codes
        reason_codes = self.explanation_generator.collect_reason_codes(matched_rules)

        # Add reason codes from modifiers
        for modifier in matched_modifiers:
            for code in modifier.reason_codes:
                if code not in reason_codes:
                    reason_codes.append(code)

        # Build matched rules details
        matched_rule_details = [
            MatchedRule(
                rule_id=rule.id,
                label=rule.label,
                disposition=rule.disposition,
                priority=rule.priority,
                reason_codes=rule.reason_codes,
            )
            for rule in matched_rules
        ]

        return TriageResult(
            disposition=final_disposition,
            priority=priority,
            matched_rule_ids=[rule.id for rule in matched_rules],
            matched_rules=matched_rule_details,
            reason_codes=reason_codes,
            explanation=explanation,
            safety_warnings=safety_warnings,
            derived_lab_statuses=lab_statuses,
            risk_modifiers_applied=applied_modifiers,
        )

    def _get_highest_priority(self, priorities: list[Priority]) -> Priority:
        """Get the highest priority from a list."""
        order = [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]
        for p in order:
            if p in priorities:
                return p
        return Priority.LOW
