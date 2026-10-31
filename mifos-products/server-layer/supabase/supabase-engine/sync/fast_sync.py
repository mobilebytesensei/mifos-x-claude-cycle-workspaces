"""
Fast Sync: PostgreSQL to Supabase

High-performance synchronization from local PostgreSQL to remote Supabase.
Uses batch upserts for optimal throughput.

Performance:
    - Batch size 1000: ~2,500-4,000 records/second
    - 1M records: ~4-7 minutes
    - 1.3M movies: ~5-10 minutes

Usage:
    python sync/fast_sync.py                    # Sync dirty/pending rows
    python sync/fast_sync.py --full             # Full sync (reset all)
    python sync/fast_sync.py --table movies     # Sync specific table
    python sync/fast_sync.py --dry-run          # Show what would sync

Rule: RULE-ENGINE-SYNC-001
"""

import argparse
import asyncio
import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Generator

import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from supabase import create_client, Client

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    DATABASE_URL, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    SUPABASE_URL, SUPABASE_SERVICE_KEY,
    BATCH_SIZE, SYNC_COLUMNS, PRIMARY_TABLE
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class SyncStats:
    """Statistics for a sync operation."""
    table: str
    started_at: datetime
    completed_at: datetime | None = None
    total_rows: int = 0
    synced_rows: int = 0
    error_rows: int = 0
    skipped_rows: int = 0
    batches: int = 0
    duration_seconds: float = 0
    rows_per_second: float = 0


class FastSync:
    """High-performance PostgreSQL to Supabase sync."""

    def __init__(
        self,
        batch_size: int = BATCH_SIZE,
        sync_columns: set = None,
        dry_run: bool = False
    ):
        self.batch_size = batch_size
        self.sync_columns = sync_columns or SYNC_COLUMNS
        self.dry_run = dry_run

        # Initialize connections
        self.pg_conn = None
        self.supabase: Client = None

    def connect(self):
        """Establish database connections."""
        logger.info("Connecting to databases...")

        # PostgreSQL
        self.pg_conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        logger.info(f"Connected to PostgreSQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")

        # Supabase
        if not self.dry_run:
            if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
                raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY are required")

            self.supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            logger.info(f"Connected to Supabase: {SUPABASE_URL}")
        else:
            logger.info("DRY RUN: Supabase connection skipped")

    def close(self):
        """Close database connections."""
        if self.pg_conn:
            self.pg_conn.close()
        logger.info("Connections closed")

    def get_sync_stats(self, table: str) -> dict:
        """Get sync status counts for a table."""
        with self.pg_conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT sync_status, COUNT(*)
                FROM {table}
                GROUP BY sync_status
            """)
            return dict(cursor.fetchall())

    def get_dirty_rows(
        self,
        table: str,
        statuses: list = None
    ) -> Generator[list[dict], None, None]:
        """
        Yield batches of dirty/pending rows.

        Args:
            table: Table name
            statuses: List of sync statuses to fetch (default: pending, dirty, error)

        Yields:
            Batches of row dictionaries
        """
        if statuses is None:
            statuses = ["pending", "dirty", "error"]

        # Get column names (excluding sync columns)
        with self.pg_conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table,))
            all_columns = [row[0] for row in cursor.fetchall()]

        # Columns to sync (exclude sync tracking columns)
        sync_cols = [c for c in all_columns if c not in self.sync_columns]
        select_cols = ", ".join(sync_cols)

        # Stream rows in batches
        with self.pg_conn.cursor(
            name="sync_cursor",
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.itersize = self.batch_size

            placeholders = ", ".join(["%s"] * len(statuses))
            cursor.execute(f"""
                SELECT id, {select_cols}
                FROM {table}
                WHERE sync_status IN ({placeholders})
                ORDER BY id
            """, statuses)

            batch = []
            for row in cursor:
                batch.append(dict(row))

                if len(batch) >= self.batch_size:
                    yield batch
                    batch = []

            # Yield remaining rows
            if batch:
                yield batch

    def mark_synced(self, table: str, row_ids: list[str]):
        """Mark rows as synced."""
        if self.dry_run:
            return

        with self.pg_conn.cursor() as cursor:
            execute_values(
                cursor,
                f"""
                UPDATE {table}
                SET sync_status = 'synced',
                    sync_timestamp = NOW(),
                    sync_error = NULL
                WHERE id IN (%s)
                """,
                [(id_,) for id_ in row_ids],
                template="(%s)"
            )
        self.pg_conn.commit()

    def mark_error(self, table: str, row_ids: list[str], error: str):
        """Mark rows as error."""
        if self.dry_run:
            return

        with self.pg_conn.cursor() as cursor:
            execute_values(
                cursor,
                f"""
                UPDATE {table}
                SET sync_status = 'error',
                    sync_timestamp = NOW(),
                    sync_error = %s
                WHERE id IN (%s)
                """,
                [(error, id_) for id_ in row_ids],
                template="(%s, %s)"
            )
        self.pg_conn.commit()

    def reset_sync_status(self, table: str):
        """Reset all rows to pending for full re-sync."""
        if self.dry_run:
            logger.info(f"DRY RUN: Would reset sync status for {table}")
            return

        with self.pg_conn.cursor() as cursor:
            cursor.execute(f"""
                UPDATE {table}
                SET sync_status = 'pending',
                    sync_timestamp = NULL,
                    sync_error = NULL
            """)
            count = cursor.rowcount
        self.pg_conn.commit()
        logger.info(f"Reset {count} rows to pending in {table}")

    def sync_batch(self, table: str, rows: list[dict]) -> tuple[int, int]:
        """
        Sync a batch of rows to Supabase.

        Returns:
            Tuple of (synced_count, error_count)
        """
        if not rows:
            return 0, 0

        row_ids = [row["id"] for row in rows]

        if self.dry_run:
            logger.info(f"DRY RUN: Would sync {len(rows)} rows")
            return len(rows), 0

        try:
            # Upsert to Supabase
            self.supabase.table(table).upsert(rows).execute()

            # Mark as synced
            self.mark_synced(table, row_ids)

            return len(rows), 0

        except Exception as e:
            error_msg = str(e)[:500]  # Truncate error message
            logger.error(f"Batch sync error: {error_msg}")

            # Mark as error
            self.mark_error(table, row_ids, error_msg)

            return 0, len(rows)

    def sync_table(
        self,
        table: str,
        full_sync: bool = False,
        statuses: list = None
    ) -> SyncStats:
        """
        Sync a table from PostgreSQL to Supabase.

        Args:
            table: Table name
            full_sync: If True, reset all rows to pending first
            statuses: Specific statuses to sync

        Returns:
            SyncStats with operation statistics
        """
        stats = SyncStats(
            table=table,
            started_at=datetime.now()
        )

        logger.info("=" * 60)
        logger.info(f"Starting sync for table: {table}")
        logger.info(f"Full sync: {full_sync}")
        logger.info(f"Batch size: {self.batch_size}")
        logger.info(f"Dry run: {self.dry_run}")
        logger.info("=" * 60)

        # Show current stats
        current_stats = self.get_sync_stats(table)
        logger.info(f"Current sync status: {current_stats}")

        if full_sync:
            self.reset_sync_status(table)

        # Count rows to sync
        if statuses is None:
            statuses = ["pending", "dirty", "error"]

        with self.pg_conn.cursor() as cursor:
            placeholders = ", ".join(["%s"] * len(statuses))
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {table}
                WHERE sync_status IN ({placeholders})
            """, statuses)
            stats.total_rows = cursor.fetchone()[0]

        logger.info(f"Rows to sync: {stats.total_rows}")

        if stats.total_rows == 0:
            logger.info("No rows to sync")
            stats.completed_at = datetime.now()
            return stats

        # Sync in batches
        start_time = time.time()

        for batch in self.get_dirty_rows(table, statuses):
            synced, errors = self.sync_batch(table, batch)
            stats.synced_rows += synced
            stats.error_rows += errors
            stats.batches += 1

            # Progress logging
            elapsed = time.time() - start_time
            rate = stats.synced_rows / elapsed if elapsed > 0 else 0
            logger.info(
                f"Progress: {stats.synced_rows}/{stats.total_rows} "
                f"({stats.synced_rows * 100 // stats.total_rows}%) "
                f"@ {rate:.0f} rows/sec"
            )

        # Final stats
        stats.completed_at = datetime.now()
        stats.duration_seconds = time.time() - start_time
        stats.rows_per_second = (
            stats.synced_rows / stats.duration_seconds
            if stats.duration_seconds > 0 else 0
        )

        logger.info("=" * 60)
        logger.info(f"Sync complete for: {table}")
        logger.info(f"Duration: {stats.duration_seconds:.1f} seconds")
        logger.info(f"Synced: {stats.synced_rows}")
        logger.info(f"Errors: {stats.error_rows}")
        logger.info(f"Rate: {stats.rows_per_second:.0f} rows/second")
        logger.info("=" * 60)

        return stats


def main():
    parser = argparse.ArgumentParser(
        description="Sync PostgreSQL to Supabase"
    )
    parser.add_argument(
        "--table",
        default=PRIMARY_TABLE,
        help=f"Table to sync (default: {PRIMARY_TABLE})"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full sync (reset all rows to pending)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
        help=f"Batch size (default: {BATCH_SIZE})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without syncing"
    )
    parser.add_argument(
        "--status-only",
        action="store_true",
        help="Only show sync status, don't sync"
    )

    args = parser.parse_args()

    syncer = FastSync(
        batch_size=args.batch_size,
        dry_run=args.dry_run
    )

    try:
        syncer.connect()

        if args.status_only:
            stats = syncer.get_sync_stats(args.table)
            print(f"\nSync status for {args.table}:")
            print("-" * 30)
            total = sum(stats.values())
            for status, count in sorted(stats.items()):
                pct = count * 100 / total if total > 0 else 0
                print(f"  {status}: {count:,} ({pct:.1f}%)")
            print("-" * 30)
            print(f"  Total: {total:,}")
        else:
            result = syncer.sync_table(
                table=args.table,
                full_sync=args.full
            )

            # Exit with error if any rows failed
            if result.error_rows > 0:
                sys.exit(1)

    except Exception as e:
        logger.error(f"Sync failed: {e}")
        sys.exit(1)
    finally:
        syncer.close()


if __name__ == "__main__":
    main()
