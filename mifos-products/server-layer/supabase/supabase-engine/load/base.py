"""
Base Loader

Abstract base class for data loaders.
"""

from abc import ABC, abstractmethod
from typing import Any
import logging

logger = logging.getLogger(__name__)


class BaseLoader(ABC):
    """
    Abstract base loader for data destinations.

    Implement this class for each destination type.
    """

    def __init__(self, config: dict = None):
        self.config = config or {}

    @abstractmethod
    def load(self, data: list[dict], table: str) -> int:
        """
        Load data to destination.

        Args:
            data: List of records to load
            table: Destination table/collection name

        Returns:
            Number of records loaded
        """
        pass

    def batch_load(self, data: list[dict], table: str, batch_size: int = 100) -> int:
        """
        Load data in batches.

        Args:
            data: List of records to load
            table: Destination table name
            batch_size: Records per batch

        Returns:
            Total records loaded
        """
        total = 0
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            loaded = self.load(batch, table)
            total += loaded
            logger.info(f"Loaded batch {i // batch_size + 1}: {loaded} records")
        return total
