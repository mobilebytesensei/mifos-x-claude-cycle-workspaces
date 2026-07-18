"""
Extract Module

Data extraction adapters for various sources.
"""

from .base import Extractor, BaseAdapter

# Register adapters here as they're created
# from .adapters.api_adapter import ApiAdapter
# from .adapters.csv_adapter import CsvAdapter
# from .adapters.database_adapter import DatabaseAdapter

ADAPTERS = {
    # "api": ApiAdapter,
    # "csv": CsvAdapter,
    # "database": DatabaseAdapter,
}

__all__ = ["Extractor", "BaseAdapter", "ADAPTERS"]
