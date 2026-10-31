"""
Data Validators

Validation rules and validator implementation.

Usage:
    config = {
        "rules": {
            "id": {"required": True, "type": "int"},
            "email": {"required": True, "type": "str", "pattern": r".*@.*"},
        },
        "on_failure": "skip"  # skip, fail, log
    }
    validator = Validator(config)
    valid, invalid = validator.validate(data)
"""

from dataclasses import dataclass
from typing import Any
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class ValidationRule:
    """Single validation rule for a field."""
    field: str
    required: bool = False
    field_type: str = "str"
    min_value: float | None = None
    max_value: float | None = None
    min_length: int | None = None
    max_length: int | None = None
    pattern: str | None = None
    allowed_values: list | None = None


@dataclass
class ValidationError:
    """Validation error details."""
    field: str
    value: Any
    rule: str
    message: str


class Validator:
    """
    Data validator with configurable rules.

    Config:
        rules: Dict of field_name: rule_config
        on_failure: "skip" (exclude), "fail" (raise), or "log" (include with warning)
    """

    TYPE_MAP = {
        "str": str,
        "int": int,
        "float": (int, float),
        "bool": bool,
        "list": list,
        "dict": dict,
        "datetime": str,  # Date strings
    }

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.rules = self._parse_rules(self.config.get("rules", {}))
        self.on_failure = self.config.get("on_failure", "skip")

    def _parse_rules(self, rules_config: dict) -> list[ValidationRule]:
        """Parse config into ValidationRule objects."""
        rules = []
        for field, rule_config in rules_config.items():
            rule = ValidationRule(
                field=field,
                required=rule_config.get("required", False),
                field_type=rule_config.get("type", "str"),
                min_value=rule_config.get("min_value"),
                max_value=rule_config.get("max_value"),
                min_length=rule_config.get("min_length"),
                max_length=rule_config.get("max_length"),
                pattern=rule_config.get("pattern"),
                allowed_values=rule_config.get("allowed_values"),
            )
            rules.append(rule)
        return rules

    def validate(self, data: list[dict]) -> tuple[list[dict], list[dict]]:
        """
        Validate all records.

        Args:
            data: Records to validate

        Returns:
            Tuple of (valid_records, invalid_records)
        """
        valid = []
        invalid = []

        for record in data:
            errors = self._validate_record(record)
            if errors:
                if self.on_failure == "fail":
                    raise ValueError(f"Validation failed: {errors}")
                elif self.on_failure == "log":
                    for error in errors:
                        logger.warning(f"Validation error: {error}")
                    valid.append(record)
                else:  # skip
                    record["_validation_errors"] = [e.__dict__ for e in errors]
                    invalid.append(record)
            else:
                valid.append(record)

        return valid, invalid

    def _validate_record(self, record: dict) -> list[ValidationError]:
        """Validate single record against all rules."""
        errors = []

        for rule in self.rules:
            value = record.get(rule.field)

            # Required check
            if rule.required and (value is None or value == ""):
                errors.append(ValidationError(
                    field=rule.field,
                    value=value,
                    rule="required",
                    message=f"Field '{rule.field}' is required"
                ))
                continue

            # Skip further checks if value is None
            if value is None:
                continue

            # Type check
            expected_type = self.TYPE_MAP.get(rule.field_type, str)
            if not isinstance(value, expected_type):
                errors.append(ValidationError(
                    field=rule.field,
                    value=value,
                    rule="type",
                    message=f"Field '{rule.field}' must be {rule.field_type}"
                ))
                continue

            # Min/Max value (numeric)
            if isinstance(value, (int, float)):
                if rule.min_value is not None and value < rule.min_value:
                    errors.append(ValidationError(
                        field=rule.field,
                        value=value,
                        rule="min_value",
                        message=f"Field '{rule.field}' must be >= {rule.min_value}"
                    ))
                if rule.max_value is not None and value > rule.max_value:
                    errors.append(ValidationError(
                        field=rule.field,
                        value=value,
                        rule="max_value",
                        message=f"Field '{rule.field}' must be <= {rule.max_value}"
                    ))

            # Min/Max length (strings)
            if isinstance(value, str):
                if rule.min_length is not None and len(value) < rule.min_length:
                    errors.append(ValidationError(
                        field=rule.field,
                        value=value,
                        rule="min_length",
                        message=f"Field '{rule.field}' must be at least {rule.min_length} chars"
                    ))
                if rule.max_length is not None and len(value) > rule.max_length:
                    errors.append(ValidationError(
                        field=rule.field,
                        value=value,
                        rule="max_length",
                        message=f"Field '{rule.field}' must be at most {rule.max_length} chars"
                    ))

            # Pattern (regex)
            if rule.pattern and isinstance(value, str):
                if not re.match(rule.pattern, value):
                    errors.append(ValidationError(
                        field=rule.field,
                        value=value,
                        rule="pattern",
                        message=f"Field '{rule.field}' must match pattern {rule.pattern}"
                    ))

            # Allowed values (enum)
            if rule.allowed_values and value not in rule.allowed_values:
                errors.append(ValidationError(
                    field=rule.field,
                    value=value,
                    rule="allowed_values",
                    message=f"Field '{rule.field}' must be one of {rule.allowed_values}"
                ))

        return errors

    def validate_single(self, record: dict) -> tuple[bool, list[ValidationError]]:
        """
        Validate a single record.

        Returns:
            Tuple of (is_valid, errors)
        """
        errors = self._validate_record(record)
        return len(errors) == 0, errors
