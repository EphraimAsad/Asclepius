"""
Lab status deriver for the rules engine.

Derives lab statuses (CRITICAL_LOW, LOW, NORMAL, HIGH, CRITICAL_HIGH)
from lab input values based on lab test definitions.
"""

from app.models.enums import LabStatus
from app.models.patient import LabInput
from app.models.rules import LabTest, StatusThreshold


class LabStatusDeriver:
    """Derives lab statuses from lab inputs using lab test definitions."""

    def derive_status(self, lab_input: LabInput, lab_test: LabTest) -> LabStatus:
        """
        Derive the status for a lab result.

        Args:
            lab_input: The lab input with value and optional reference ranges
            lab_test: The lab test definition with status logic

        Returns:
            The derived LabStatus
        """
        value = lab_input.value
        status_logic = lab_test.status_logic

        # Check critical_high first (most urgent)
        if self._check_threshold_high(
            value, lab_input, status_logic.critical_high
        ):
            return LabStatus.CRITICAL_HIGH

        # Check high
        if self._check_threshold_high(
            value, lab_input, status_logic.high
        ):
            return LabStatus.HIGH

        # Check critical_low
        if self._check_threshold_low(
            value, lab_input, status_logic.critical_low
        ):
            return LabStatus.CRITICAL_LOW

        # Check low
        if self._check_threshold_low(
            value, lab_input, status_logic.low
        ):
            return LabStatus.LOW

        return LabStatus.NORMAL

    def _check_threshold_high(
        self,
        value: float,
        lab_input: LabInput,
        threshold: StatusThreshold | None
    ) -> bool:
        """Check if value exceeds a high threshold."""
        if threshold is None:
            return False

        # Check simple value threshold first
        if threshold.value is not None:
            if value >= threshold.value:
                return True

        # Check multiplier of reference high
        if threshold.multiplier_of_reference_high is not None:
            if lab_input.reference_high is not None:
                limit = lab_input.reference_high * threshold.multiplier_of_reference_high
                if value >= limit:
                    return True

        # Check use_reference_high
        if threshold.use_reference_high:
            if lab_input.reference_high is not None:
                if value > lab_input.reference_high:
                    return True

        # Check absolute threshold by unit
        if threshold.absolute_threshold_by_unit:
            unit = lab_input.unit
            if unit in threshold.absolute_threshold_by_unit:
                limit = threshold.absolute_threshold_by_unit[unit]
                if value >= limit:
                    return True

        return False

    def _check_threshold_low(
        self,
        value: float,
        lab_input: LabInput,
        threshold: StatusThreshold | None
    ) -> bool:
        """Check if value falls below a low threshold."""
        if threshold is None:
            return False

        # Check simple value threshold first
        if threshold.value is not None:
            if value <= threshold.value:
                return True

        # Check multiplier of reference low
        if threshold.multiplier_of_reference_low is not None:
            if lab_input.reference_low is not None:
                limit = lab_input.reference_low * threshold.multiplier_of_reference_low
                if value <= limit:
                    return True

        # Check use_reference_low
        if threshold.use_reference_low:
            if lab_input.reference_low is not None:
                if value < lab_input.reference_low:
                    return True

        # Check absolute threshold by unit
        if threshold.absolute_threshold_by_unit:
            unit = lab_input.unit
            if unit in threshold.absolute_threshold_by_unit:
                limit = threshold.absolute_threshold_by_unit[unit]
                if value <= limit:
                    return True

        return False

    def derive_all_statuses(
        self,
        lab_inputs: list[LabInput],
        lab_tests: list[LabTest]
    ) -> dict[str, LabStatus]:
        """
        Derive statuses for all lab inputs.

        Args:
            lab_inputs: List of lab inputs
            lab_tests: List of lab test definitions

        Returns:
            Dictionary mapping test_code to LabStatus
        """
        # Build lookup for lab tests by code
        test_lookup = {test.test_code: test for test in lab_tests}

        statuses = {}
        for lab_input in lab_inputs:
            if lab_input.test_code in test_lookup:
                lab_test = test_lookup[lab_input.test_code]
                statuses[lab_input.test_code] = self.derive_status(lab_input, lab_test)

        return statuses
