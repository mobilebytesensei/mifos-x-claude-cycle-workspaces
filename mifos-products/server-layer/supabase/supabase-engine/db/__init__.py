"""
Database Module

Database initialization and management utilities.

Components:
    - init_db: Initialize PostgreSQL database with schema
    - schema.sql: Database schema with sync tracking
"""

from .init_db import (
    init_database,
    create_database,
    drop_database,
    run_schema,
    get_table_stats,
    database_exists,
)

__all__ = [
    "init_database",
    "create_database",
    "drop_database",
    "run_schema",
    "get_table_stats",
    "database_exists",
]
