"""
Staging Loader

SQLite staging database for intermediate storage.

Benefits:
- Checkpoint before Supabase sync
- Rollback capability
- Offline development
- Audit trail
"""

import sqlite3
from pathlib import Path
from typing import Any
import logging
import json

from .base import BaseLoader

logger = logging.getLogger(__name__)


class StagingLoader(BaseLoader):
    """
    SQLite staging database loader.

    Stores data locally before syncing to Supabase.

    Config:
        database: Path to SQLite file (default: data/staging.db)
        table_prefix: Prefix for table names (default: stg_)
    """

    def __init__(self, config: dict = None):
        super().__init__(config)
        self.db_path = Path(self.config.get("database", "data/staging.db"))
        self.table_prefix = self.config.get("table_prefix", "stg_")

        # Ensure directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Get SQLite connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self, conn: sqlite3.Connection, table: str, sample: dict) -> None:
        """Create table based on sample record."""
        columns = []
        for key, value in sample.items():
            if isinstance(value, int):
                col_type = "INTEGER"
            elif isinstance(value, float):
                col_type = "REAL"
            elif isinstance(value, bool):
                col_type = "INTEGER"
            elif isinstance(value, (dict, list)):
                col_type = "TEXT"  # Store as JSON
            else:
                col_type = "TEXT"
            columns.append(f"{key} {col_type}")

        # Add metadata columns
        columns.extend([
            "sync_status TEXT DEFAULT 'pending'",
            "staged_at TEXT DEFAULT CURRENT_TIMESTAMP",
            "synced_at TEXT",
        ])

        table_name = f"{self.table_prefix}{table}"
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"

        conn.execute(create_sql)
        conn.commit()
        logger.info(f"Created staging table: {table_name}")

    def load(self, data: list[dict], table: str) -> int:
        """
        Load data to staging table.

        Args:
            data: Records to stage
            table: Base table name (will be prefixed)

        Returns:
            Number of records staged
        """
        if not data:
            return 0

        table_name = f"{self.table_prefix}{table}"

        with self._get_connection() as conn:
            # Create table if not exists
            self._create_table(conn, table, data[0])

            # Get column names from first record
            columns = list(data[0].keys())
            placeholders = ", ".join(["?" for _ in columns])
            column_names = ", ".join(columns)

            insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

            for record in data:
                values = []
                for col in columns:
                    value = record.get(col)
                    # Serialize complex types
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value)
                    values.append(value)
                conn.execute(insert_sql, values)

            conn.commit()

        logger.info(f"Staged {len(data)} records to {table_name}")
        return len(data)

    def get_pending(self, table: str, limit: int = 100) -> list[dict]:
        """
        Get records pending sync.

        Args:
            table: Base table name
            limit: Max records to return

        Returns:
            List of pending records
        """
        table_name = f"{self.table_prefix}{table}"

        with self._get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {table_name} WHERE sync_status = 'pending' LIMIT ?",
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def mark_synced(self, table: str, ids: list) -> int:
        """
        Mark records as synced.

        Args:
            table: Base table name
            ids: List of record IDs to mark

        Returns:
            Number of records updated
        """
        if not ids:
            return 0

        table_name = f"{self.table_prefix}{table}"
        placeholders = ", ".join(["?" for _ in ids])

        with self._get_connection() as conn:
            cursor = conn.execute(
                f"""UPDATE {table_name}
                    SET sync_status = 'synced', synced_at = CURRENT_TIMESTAMP
                    WHERE id IN ({placeholders})""",
                ids
            )
            conn.commit()
            return cursor.rowcount

    def clear(self, table: str, synced_only: bool = True) -> int:
        """
        Clear staging table.

        Args:
            table: Base table name
            synced_only: If True, only delete synced records

        Returns:
            Number of records deleted
        """
        table_name = f"{self.table_prefix}{table}"

        with self._get_connection() as conn:
            if synced_only:
                cursor = conn.execute(
                    f"DELETE FROM {table_name} WHERE sync_status = 'synced'"
                )
            else:
                cursor = conn.execute(f"DELETE FROM {table_name}")
            conn.commit()
            return cursor.rowcount
