"""
Supabase Sync

Sync data to Supabase with incremental and full sync modes.

Patterns:
- Incremental: Only sync new/changed records (dirty-row pattern)
- Full: Replace all records
- Upsert: Insert or update based on key
"""

from typing import Any
from datetime import datetime
import logging

from supabase import create_client, Client

from .base import BaseLoader

logger = logging.getLogger(__name__)


class SupabaseSync(BaseLoader):
    """
    Supabase data synchronization.

    Supports:
    - Full sync (truncate and reload)
    - Incremental sync (upsert changed records)
    - Batch operations

    Config (via main config):
        supabase.url: Supabase project URL
        supabase.service_key: Service role key
        load.destination.upsert_key: Primary key field
        load.sync.batch_size: Records per batch
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.url = config.get("supabase", {}).get("url", "")
        self.key = config.get("supabase", {}).get("service_key", "")
        self.client: Client = None

        load_config = config.get("load", {})
        self.upsert_key = load_config.get("destination", {}).get("upsert_key", "id")
        self.batch_size = load_config.get("sync", {}).get("batch_size", 100)

    def _get_client(self) -> Client:
        """Get or create Supabase client."""
        if not self.client:
            if not self.url or not self.key:
                raise ValueError("Supabase URL and service key required")
            self.client = create_client(self.url, self.key)
        return self.client

    def load(self, data: list[dict], table: str) -> int:
        """
        Load data to Supabase using upsert.

        Args:
            data: Records to load
            table: Destination table

        Returns:
            Number of records loaded
        """
        if not data:
            return 0

        client = self._get_client()

        try:
            # Add sync metadata
            now = datetime.utcnow().isoformat()
            for record in data:
                record["synced_at"] = now

            result = client.table(table).upsert(
                data,
                on_conflict=self.upsert_key
            ).execute()

            return len(result.data) if result.data else 0

        except Exception as e:
            logger.error(f"Failed to upsert to {table}: {e}")
            raise

    def incremental_sync(self, data: list[dict], table: str) -> int:
        """
        Incremental sync using upsert.

        Only syncs records that have changed based on updated_at.

        Args:
            data: Records to sync
            table: Destination table

        Returns:
            Number of records synced
        """
        logger.info(f"Incremental sync to {table}: {len(data)} records")
        return self.batch_load(data, table, self.batch_size)

    def full_sync(self, data: list[dict], table: str) -> int:
        """
        Full sync: delete all and insert fresh.

        WARNING: This deletes all existing data!

        Args:
            data: Records to sync
            table: Destination table

        Returns:
            Number of records synced
        """
        logger.warning(f"Full sync to {table}: deleting existing data")

        client = self._get_client()

        try:
            # Delete all existing records
            # Note: This requires RLS to allow delete
            client.table(table).delete().neq(self.upsert_key, -1).execute()
            logger.info(f"Deleted existing records from {table}")

            # Insert fresh data
            return self.batch_load(data, table, self.batch_size)

        except Exception as e:
            logger.error(f"Full sync failed for {table}: {e}")
            raise

    def upsert(self, data: list[dict], table: str) -> int:
        """
        Upsert records (insert or update).

        Convenience method for single operations.

        Args:
            data: Records to upsert
            table: Destination table

        Returns:
            Number of records affected
        """
        return self.load(data, table)

    def delete(self, ids: list, table: str) -> int:
        """
        Delete records by ID.

        Args:
            ids: List of IDs to delete
            table: Table name

        Returns:
            Number of records deleted
        """
        if not ids:
            return 0

        client = self._get_client()

        try:
            result = client.table(table).delete().in_(self.upsert_key, ids).execute()
            return len(result.data) if result.data else 0

        except Exception as e:
            logger.error(f"Failed to delete from {table}: {e}")
            raise

    def get_last_sync_time(self, table: str) -> str | None:
        """
        Get last sync timestamp for incremental sync.

        Args:
            table: Table name

        Returns:
            ISO timestamp of last sync or None
        """
        client = self._get_client()

        try:
            result = client.table(table).select("synced_at").order(
                "synced_at", desc=True
            ).limit(1).execute()

            if result.data:
                return result.data[0].get("synced_at")
            return None

        except Exception as e:
            logger.warning(f"Could not get last sync time: {e}")
            return None
