"""
SQLite to PostgreSQL Migration

Migrates data from existing SQLite database to PostgreSQL.
Useful for projects that started with SQLite staging and want
to migrate to PostgreSQL for team collaboration.

Usage:
    python sync/migration.py --source data/staging.db
    python sync/migration.py --source data/staging.db --table movies
    python sync/migration.py --source data/staging.db --dry-run

Rule: RULE-ENGINE-AUTO-001
"""

import argparse
import logging
import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from typing import Generator

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SQLiteToPostgresMigration:
    """Migrate data from SQLite to PostgreSQL."""

    def __init__(
        self,
        sqlite_path: str,
        batch_size: int = 1000,
        dry_run: bool = False
    ):
        self.sqlite_path = Path(sqlite_path)
        self.batch_size = batch_size
        self.dry_run = dry_run

        self.sqlite_conn = None
        self.pg_conn = None

    def connect(self):
        """Establish database connections."""
        # SQLite
        if not self.sqlite_path.exists():
            raise FileNotFoundError(f"SQLite database not found: {self.sqlite_path}")

        self.sqlite_conn = sqlite3.connect(self.sqlite_path)
        self.sqlite_conn.row_factory = sqlite3.Row
        logger.info(f"Connected to SQLite: {self.sqlite_path}")

        # PostgreSQL
        self.pg_conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        logger.info(f"Connected to PostgreSQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")

    def close(self):
        """Close database connections."""
        if self.sqlite_conn:
            self.sqlite_conn.close()
        if self.pg_conn:
            self.pg_conn.close()
        logger.info("Connections closed")

    def get_sqlite_tables(self) -> list[str]:
        """Get list of tables in SQLite database."""
        cursor = self.sqlite_conn.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
        """)
        return [row[0] for row in cursor.fetchall()]

    def get_sqlite_columns(self, table: str) -> list[str]:
        """Get column names for a SQLite table."""
        cursor = self.sqlite_conn.execute(f"PRAGMA table_info({table})")
        return [row[1] for row in cursor.fetchall()]

    def get_sqlite_row_count(self, table: str) -> int:
        """Get row count for a SQLite table."""
        cursor = self.sqlite_conn.execute(f"SELECT COUNT(*) FROM {table}")
        return cursor.fetchone()[0]

    def get_pg_columns(self, table: str) -> list[str]:
        """Get column names for a PostgreSQL table."""
        with self.pg_conn.cursor() as cursor:
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table,))
            return [row[0] for row in cursor.fetchall()]

    def stream_sqlite_rows(
        self,
        table: str,
        columns: list[str]
    ) -> Generator[list[dict], None, None]:
        """Stream rows from SQLite in batches."""
        select_cols = ", ".join(columns)
        cursor = self.sqlite_conn.execute(
            f"SELECT {select_cols} FROM {table}"
        )

        batch = []
        for row in cursor:
            batch.append(dict(row))

            if len(batch) >= self.batch_size:
                yield batch
                batch = []

        if batch:
            yield batch

    def migrate_table(self, table: str) -> dict:
        """
        Migrate a single table from SQLite to PostgreSQL.

        Returns:
            Dictionary with migration statistics
        """
        stats = {
            "table": table,
            "rows_migrated": 0,
            "rows_skipped": 0,
            "errors": 0,
            "started_at": datetime.now(),
            "completed_at": None,
        }

        logger.info(f"\n{'=' * 60}")
        logger.info(f"Migrating table: {table}")
        logger.info(f"{'=' * 60}")

        # Get columns
        sqlite_cols = self.get_sqlite_columns(table)
        pg_cols = self.get_pg_columns(table)

        if not pg_cols:
            logger.warning(f"Table {table} does not exist in PostgreSQL, skipping")
            stats["errors"] = -1  # Signal table doesn't exist
            return stats

        # Find common columns (columns that exist in both)
        common_cols = [c for c in sqlite_cols if c in pg_cols]

        # Add sync tracking columns if not present in source
        sync_cols = ["sync_status", "sync_timestamp", "sync_error"]
        for col in sync_cols:
            if col not in common_cols and col in pg_cols:
                # Will be set by default value
                pass

        logger.info(f"SQLite columns: {len(sqlite_cols)}")
        logger.info(f"PostgreSQL columns: {len(pg_cols)}")
        logger.info(f"Common columns: {len(common_cols)}")
        logger.info(f"Columns to migrate: {common_cols}")

        total_rows = self.get_sqlite_row_count(table)
        logger.info(f"Total rows to migrate: {total_rows}")

        if self.dry_run:
            logger.info("DRY RUN: Would migrate rows, but not actually inserting")
            stats["rows_migrated"] = total_rows
            stats["completed_at"] = datetime.now()
            return stats

        # Migrate in batches
        migrated = 0
        for batch in self.stream_sqlite_rows(table, common_cols):
            try:
                # Prepare insert statement
                col_names = sql.SQL(", ").join(
                    [sql.Identifier(c) for c in common_cols]
                )
                placeholders = sql.SQL(", ").join(
                    [sql.Placeholder() for _ in common_cols]
                )

                insert_sql = sql.SQL("""
                    INSERT INTO {table} ({columns})
                    VALUES ({placeholders})
                    ON CONFLICT (id) DO UPDATE SET
                    {updates}
                """).format(
                    table=sql.Identifier(table),
                    columns=col_names,
                    placeholders=placeholders,
                    updates=sql.SQL(", ").join([
                        sql.SQL("{} = EXCLUDED.{}").format(
                            sql.Identifier(c), sql.Identifier(c)
                        )
                        for c in common_cols if c != "id"
                    ])
                )

                # Execute batch
                with self.pg_conn.cursor() as cursor:
                    for row in batch:
                        values = [row.get(c) for c in common_cols]
                        try:
                            cursor.execute(insert_sql, values)
                            migrated += 1
                        except Exception as e:
                            logger.warning(f"Row error: {e}")
                            stats["errors"] += 1

                self.pg_conn.commit()
                stats["rows_migrated"] = migrated

                # Progress
                pct = migrated * 100 // total_rows if total_rows > 0 else 100
                logger.info(f"Progress: {migrated}/{total_rows} ({pct}%)")

            except Exception as e:
                logger.error(f"Batch error: {e}")
                stats["errors"] += len(batch)
                self.pg_conn.rollback()

        stats["completed_at"] = datetime.now()
        duration = (stats["completed_at"] - stats["started_at"]).total_seconds()
        rate = migrated / duration if duration > 0 else 0

        logger.info(f"\nMigration complete for: {table}")
        logger.info(f"Rows migrated: {migrated}")
        logger.info(f"Errors: {stats['errors']}")
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Rate: {rate:.0f} rows/second")

        return stats

    def migrate_all(self, tables: list[str] = None) -> list[dict]:
        """
        Migrate all tables (or specified tables).

        Returns:
            List of migration statistics per table
        """
        if tables is None:
            tables = self.get_sqlite_tables()

        logger.info(f"Tables to migrate: {tables}")

        results = []
        for table in tables:
            result = self.migrate_table(table)
            results.append(result)

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("MIGRATION SUMMARY")
        logger.info("=" * 60)

        total_rows = sum(r["rows_migrated"] for r in results)
        total_errors = sum(r["errors"] for r in results if r["errors"] > 0)

        for r in results:
            status = "✅" if r["errors"] <= 0 else "⚠️"
            logger.info(
                f"{status} {r['table']}: {r['rows_migrated']} rows"
                f"{f', {r[\"errors\"]} errors' if r['errors'] > 0 else ''}"
            )

        logger.info("-" * 60)
        logger.info(f"Total: {total_rows} rows migrated, {total_errors} errors")

        return results


def main():
    parser = argparse.ArgumentParser(
        description="Migrate SQLite to PostgreSQL"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to SQLite database file"
    )
    parser.add_argument(
        "--table",
        action="append",
        help="Table to migrate (can specify multiple)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Batch size (default: 1000)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be migrated without migrating"
    )
    parser.add_argument(
        "--list-tables",
        action="store_true",
        help="List tables in SQLite database and exit"
    )

    args = parser.parse_args()

    migrator = SQLiteToPostgresMigration(
        sqlite_path=args.source,
        batch_size=args.batch_size,
        dry_run=args.dry_run
    )

    try:
        migrator.connect()

        if args.list_tables:
            tables = migrator.get_sqlite_tables()
            print("\nTables in SQLite database:")
            print("-" * 40)
            for table in tables:
                count = migrator.get_sqlite_row_count(table)
                cols = len(migrator.get_sqlite_columns(table))
                print(f"  {table}: {count:,} rows, {cols} columns")
        else:
            results = migrator.migrate_all(tables=args.table)

            # Exit with error if any migration failed
            if any(r["errors"] > 0 for r in results):
                sys.exit(1)

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)
    finally:
        migrator.close()


if __name__ == "__main__":
    main()
