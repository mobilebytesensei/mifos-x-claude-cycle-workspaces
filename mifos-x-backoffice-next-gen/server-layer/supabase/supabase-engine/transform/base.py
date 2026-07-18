"""
Base Transformer

Strategy pattern for data transformations.

Usage:
    transformer = Transformer(config)
    transformed_data = transformer.transform(raw_data)

    # Custom strategy
    class MyStrategy(BaseStrategy):
        def apply(self, data: list[dict]) -> list[dict]:
            return [self.process(row) for row in data]
"""

from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseStrategy(ABC):
    """
    Abstract base strategy for transformations.

    Implement apply() method for each transform type.
    """

    def __init__(self, config: dict = None):
        self.config = config or {}

    @abstractmethod
    def apply(self, data: list[dict]) -> list[dict]:
        """
        Apply transformation to data.

        Args:
            data: List of records to transform

        Returns:
            Transformed list of records
        """
        pass


class CleanStrategy(BaseStrategy):
    """
    Clean data by stripping whitespace, handling nulls, etc.

    Config:
        strip_whitespace: bool (default True)
        remove_nulls: bool (default False)
        lowercase_fields: list of field names
    """

    def apply(self, data: list[dict]) -> list[dict]:
        """Clean each record."""
        strip_ws = self.config.get("strip_whitespace", True)
        remove_nulls = self.config.get("remove_nulls", False)
        lowercase_fields = self.config.get("lowercase_fields", [])

        cleaned = []
        for record in data:
            clean_record = {}
            for key, value in record.items():
                # Strip whitespace from strings
                if strip_ws and isinstance(value, str):
                    value = value.strip()

                # Remove null values
                if remove_nulls and value is None:
                    continue

                # Lowercase specified fields
                if key in lowercase_fields and isinstance(value, str):
                    value = value.lower()

                clean_record[key] = value
            cleaned.append(clean_record)

        logger.info(f"Cleaned {len(cleaned)} records")
        return cleaned


class NormalizeStrategy(BaseStrategy):
    """
    Normalize data formats and field names.

    Config:
        date_format: Target date format (default "%Y-%m-%d")
        decimal_places: Rounding precision for floats
        field_mappings: Dict of old_name: new_name
    """

    def apply(self, data: list[dict]) -> list[dict]:
        """Normalize each record."""
        date_format = self.config.get("date_format", "%Y-%m-%d")
        decimal_places = self.config.get("decimal_places", 2)
        field_mappings = self.config.get("field_mappings", {})

        normalized = []
        for record in data:
            norm_record = {}
            for key, value in record.items():
                # Apply field mapping
                new_key = field_mappings.get(key, key)

                # Normalize dates
                if isinstance(value, datetime):
                    value = value.strftime(date_format)
                elif isinstance(value, str) and self._looks_like_date(value):
                    value = self._parse_date(value, date_format)

                # Round decimals
                if isinstance(value, float):
                    value = round(value, decimal_places)

                norm_record[new_key] = value
            normalized.append(norm_record)

        logger.info(f"Normalized {len(normalized)} records")
        return normalized

    def _looks_like_date(self, value: str) -> bool:
        """Check if string looks like a date."""
        date_indicators = ["-", "/", "T"]
        return any(ind in value for ind in date_indicators) and len(value) >= 8

    def _parse_date(self, value: str, target_format: str) -> str:
        """Try to parse and reformat date string."""
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime(target_format)
            except ValueError:
                continue
        return value  # Return original if can't parse


class DedupeStrategy(BaseStrategy):
    """
    Remove duplicate records.

    Config:
        key_fields: Fields to use for duplicate detection
        strategy: "keep_first" or "keep_latest" (requires timestamp field)
    """

    def apply(self, data: list[dict]) -> list[dict]:
        """Deduplicate records."""
        key_fields = self.config.get("key_fields", ["id"])
        strategy = self.config.get("strategy", "keep_first")

        seen = {}
        for record in data:
            # Build composite key
            key = tuple(record.get(f) for f in key_fields)

            if key not in seen:
                seen[key] = record
            elif strategy == "keep_latest":
                # Keep record with later timestamp
                ts_field = self.config.get("timestamp_field", "updated_at")
                existing_ts = seen[key].get(ts_field, "")
                new_ts = record.get(ts_field, "")
                if new_ts > existing_ts:
                    seen[key] = record

        deduped = list(seen.values())
        removed = len(data) - len(deduped)
        if removed > 0:
            logger.info(f"Removed {removed} duplicates")
        return deduped


class Transformer:
    """
    Main transformer that applies a pipeline of strategies.

    Usage:
        config = {
            "pipeline": ["clean", "normalize", "dedupe"],
            "clean": {"strip_whitespace": True},
            ...
        }
        transformer = Transformer(config)
        result = transformer.transform(data)
    """

    STRATEGIES = {
        "clean": CleanStrategy,
        "normalize": NormalizeStrategy,
        "dedupe": DedupeStrategy,
    }

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.strategies = []

        # Build pipeline from config
        pipeline = self.config.get("pipeline", ["clean", "normalize", "dedupe"])
        for strategy_name in pipeline:
            strategy_class = self.STRATEGIES.get(strategy_name)
            if strategy_class:
                strategy_config = self.config.get(strategy_name, {})
                self.strategies.append(strategy_class(strategy_config))
            else:
                logger.warning(f"Unknown strategy: {strategy_name}")

    def add_strategy(self, strategy: BaseStrategy) -> None:
        """Add a custom strategy to the pipeline."""
        self.strategies.append(strategy)

    def transform(self, data: list[dict]) -> list[dict]:
        """Apply all strategies in sequence."""
        result = data
        for strategy in self.strategies:
            result = strategy.apply(result)
        return result
