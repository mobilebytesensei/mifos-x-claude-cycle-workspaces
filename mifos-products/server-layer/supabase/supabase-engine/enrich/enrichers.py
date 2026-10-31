"""
Data Enrichers

Add computed fields, external data, and metadata.

Usage:
    enricher = Enricher()
    enricher.add(TimestampEnricher())
    enricher.add(HashEnricher(fields=["id", "name"]))
    enriched_data = enricher.enrich(data)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
import hashlib
import uuid
import logging

logger = logging.getLogger(__name__)


class BaseEnricher(ABC):
    """Abstract base enricher."""

    @abstractmethod
    def enrich(self, record: dict) -> dict:
        """
        Enrich a single record.

        Args:
            record: Record to enrich

        Returns:
            Enriched record
        """
        pass


class TimestampEnricher(BaseEnricher):
    """Add timestamp fields."""

    def __init__(self, field: str = "processed_at"):
        self.field = field

    def enrich(self, record: dict) -> dict:
        """Add processing timestamp."""
        record[self.field] = datetime.utcnow().isoformat()
        return record


class UUIDEnricher(BaseEnricher):
    """Add UUID if not present."""

    def __init__(self, field: str = "uuid"):
        self.field = field

    def enrich(self, record: dict) -> dict:
        """Add UUID if missing."""
        if not record.get(self.field):
            record[self.field] = str(uuid.uuid4())
        return record


class HashEnricher(BaseEnricher):
    """Generate hash from specified fields for change detection."""

    def __init__(self, fields: list[str], hash_field: str = "content_hash"):
        self.fields = fields
        self.hash_field = hash_field

    def enrich(self, record: dict) -> dict:
        """Generate content hash from specified fields."""
        values = [str(record.get(f, "")) for f in self.fields]
        content = "|".join(values)
        record[self.hash_field] = hashlib.md5(content.encode()).hexdigest()
        return record


class DefaultValueEnricher(BaseEnricher):
    """Set default values for missing fields."""

    def __init__(self, defaults: dict[str, Any]):
        self.defaults = defaults

    def enrich(self, record: dict) -> dict:
        """Apply default values."""
        for field, default in self.defaults.items():
            if record.get(field) is None:
                record[field] = default
        return record


class ComputedFieldEnricher(BaseEnricher):
    """Add computed fields based on existing data."""

    def __init__(self, computations: dict[str, callable]):
        """
        Args:
            computations: Dict of field_name: computation_function
                          Function takes record and returns computed value
        """
        self.computations = computations

    def enrich(self, record: dict) -> dict:
        """Compute and add fields."""
        for field, compute_fn in self.computations.items():
            try:
                record[field] = compute_fn(record)
            except Exception as e:
                logger.warning(f"Failed to compute {field}: {e}")
        return record


class ExternalDataEnricher(BaseEnricher):
    """
    Enrich with external data lookup.

    Example: Add category name from category ID lookup.
    """

    def __init__(
        self,
        lookup_field: str,
        target_field: str,
        lookup_data: dict[Any, Any],
        default: Any = None
    ):
        """
        Args:
            lookup_field: Field to use as lookup key
            target_field: Field to store looked-up value
            lookup_data: Dict mapping keys to values
            default: Default value if lookup fails
        """
        self.lookup_field = lookup_field
        self.target_field = target_field
        self.lookup_data = lookup_data
        self.default = default

    def enrich(self, record: dict) -> dict:
        """Add external data via lookup."""
        key = record.get(self.lookup_field)
        record[self.target_field] = self.lookup_data.get(key, self.default)
        return record


class Enricher:
    """
    Main enricher that chains multiple enrichers.

    Usage:
        enricher = Enricher()
        enricher.add(TimestampEnricher())
        enricher.add(HashEnricher(["id", "name"]))
        enriched = enricher.enrich(data)
    """

    def __init__(self):
        self.enrichers: list[BaseEnricher] = []

    def add(self, enricher: BaseEnricher) -> "Enricher":
        """Add an enricher to the chain."""
        self.enrichers.append(enricher)
        return self  # Allow chaining

    def enrich(self, data: list[dict]) -> list[dict]:
        """
        Apply all enrichers to data.

        Args:
            data: Records to enrich

        Returns:
            Enriched records
        """
        result = []
        for record in data:
            enriched = record.copy()
            for enricher in self.enrichers:
                enriched = enricher.enrich(enriched)
            result.append(enriched)

        logger.info(f"Enriched {len(result)} records with {len(self.enrichers)} enrichers")
        return result

    @classmethod
    def with_defaults(cls) -> "Enricher":
        """Create enricher with common defaults."""
        enricher = cls()
        enricher.add(TimestampEnricher())
        enricher.add(UUIDEnricher())
        return enricher
