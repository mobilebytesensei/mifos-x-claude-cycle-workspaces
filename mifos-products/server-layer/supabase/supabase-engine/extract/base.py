"""
Base Extractor

Abstract base classes for data extraction.

Usage:
    # Using with adapter
    extractor = Extractor(source_config)
    data = extractor.extract()

    # Creating custom adapter
    class MyAdapter(BaseAdapter):
        def fetch(self) -> list[dict]:
            return [{"id": 1, "name": "Item"}]
"""

from abc import ABC, abstractmethod
from typing import Any
import logging

logger = logging.getLogger(__name__)


class BaseAdapter(ABC):
    """
    Abstract base adapter for data extraction.

    Implement this class for each data source type.
    """

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def fetch(self) -> list[dict]:
        """
        Fetch data from source.

        Returns:
            List of dictionaries representing extracted records.
        """
        pass

    def paginate(self, page_size: int = 100) -> list[dict]:
        """
        Fetch data with pagination support.

        Override this method for paginated sources.
        Default implementation calls fetch() directly.
        """
        return self.fetch()


class ApiAdapter(BaseAdapter):
    """
    HTTP API adapter for REST endpoints.

    Config:
        url: Base URL
        api_key: API key (optional)
        endpoints: Dict of endpoint paths
        rate_limit: Requests per minute
    """

    def fetch(self) -> list[dict]:
        """Fetch data from API endpoint."""
        import httpx

        url = self.config.get("url", "")
        api_key = self.config.get("api_key", "")
        endpoints = self.config.get("endpoints", {})

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        all_data = []
        with httpx.Client(headers=headers, timeout=30.0) as client:
            for name, endpoint in endpoints.items():
                logger.info(f"Fetching from {name}: {endpoint}")
                try:
                    response = client.get(f"{url}{endpoint}")
                    response.raise_for_status()
                    data = response.json()
                    if isinstance(data, list):
                        all_data.extend(data)
                    elif isinstance(data, dict) and "data" in data:
                        all_data.extend(data["data"])
                    else:
                        all_data.append(data)
                except Exception as e:
                    logger.error(f"Failed to fetch {endpoint}: {e}")

        return all_data


class CsvAdapter(BaseAdapter):
    """
    CSV file adapter.

    Config:
        path: Directory containing CSV files
        files: List of CSV filenames
        encoding: File encoding (default: utf-8)
    """

    def fetch(self) -> list[dict]:
        """Read data from CSV files."""
        import csv
        from pathlib import Path

        base_path = Path(self.config.get("path", "data/sources"))
        files = self.config.get("files", [])
        encoding = self.config.get("encoding", "utf-8")

        all_data = []
        for filename in files:
            file_path = base_path / filename
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                continue

            logger.info(f"Reading {file_path}")
            with open(file_path, "r", encoding=encoding) as f:
                reader = csv.DictReader(f)
                all_data.extend(list(reader))

        return all_data


class DatabaseAdapter(BaseAdapter):
    """
    Database adapter using SQLAlchemy.

    Config:
        connection_string: Database connection URL
        tables: List of tables to extract
    """

    def fetch(self) -> list[dict]:
        """Extract data from database tables."""
        from sqlalchemy import create_engine, text

        connection_string = self.config.get("connection_string", "")
        tables = self.config.get("tables", [])

        if not connection_string:
            logger.error("No connection string provided")
            return []

        engine = create_engine(connection_string)
        all_data = []

        with engine.connect() as conn:
            for table in tables:
                logger.info(f"Extracting from table: {table}")
                try:
                    result = conn.execute(text(f"SELECT * FROM {table}"))
                    rows = [dict(row._mapping) for row in result]
                    all_data.extend(rows)
                except Exception as e:
                    logger.error(f"Failed to extract {table}: {e}")

        return all_data


class Extractor:
    """
    Main extractor class that uses appropriate adapter based on config.

    Usage:
        config = {"type": "api", "url": "...", "endpoints": {...}}
        extractor = Extractor(config)
        data = extractor.extract()
    """

    ADAPTERS = {
        "api": ApiAdapter,
        "csv": CsvAdapter,
        "database": DatabaseAdapter,
    }

    def __init__(self, config: dict):
        self.config = config
        source_type = config.get("type", "api")
        adapter_class = self.ADAPTERS.get(source_type)

        if not adapter_class:
            raise ValueError(f"Unknown source type: {source_type}")

        self.adapter = adapter_class(config)

    def extract(self) -> list[dict]:
        """Extract data using configured adapter."""
        logger.info(f"Extracting with {self.adapter.__class__.__name__}")
        return self.adapter.fetch()
