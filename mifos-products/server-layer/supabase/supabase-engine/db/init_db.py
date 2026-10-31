"""
Database Initialization Script

Initializes the local PostgreSQL database with schema.
Can be used standalone or as part of the pipeline.

Usage:
    python db/init_db.py
    python db/init_db.py --reset  # Drop and recreate

Rule: RULE-ENGINE-AUTO-001
"""

import argparse
import logging
import sys
from pathlib import Path

import psycopg2
from psycopg2 import sql

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_connection(database: str = None):
    """Get database connection."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=database or DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def database_exists() -> bool:
    """Check if database exists."""
    try:
        # Connect to postgres database to check
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_NAME,)
        )
        exists = cursor.fetchone() is not None

        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        logger.error(f"Error checking database: {e}")
        return False


def create_database():
    """Create the database if it doesn't exist."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_NAME,)
        )

        if not cursor.fetchone():
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
            )
            logger.info(f"Created database: {DB_NAME}")
        else:
            logger.info(f"Database already exists: {DB_NAME}")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise


def drop_database():
    """Drop the database if it exists."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Terminate existing connections
        cursor.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = %s
            AND pid <> pg_backend_pid()
        """, (DB_NAME,))

        # Drop database
        cursor.execute(
            sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(DB_NAME))
        )
        logger.info(f"Dropped database: {DB_NAME}")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error dropping database: {e}")
        raise


def run_schema(schema_path: Path = None):
    """Run schema SQL file."""
    if schema_path is None:
        schema_path = Path(__file__).parent / "schema.sql"

    if not schema_path.exists():
        logger.error(f"Schema file not found: {schema_path}")
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    logger.info(f"Loading schema from: {schema_path}")

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Execute schema
        cursor.execute(schema_sql)
        conn.commit()

        logger.info("Schema applied successfully")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error applying schema: {e}")
        raise


def get_table_stats() -> dict:
    """Get statistics about tables in the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get table list
        cursor.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        tables = [row[0] for row in cursor.fetchall()]

        stats = {}
        for table in tables:
            cursor.execute(
                sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table))
            )
            count = cursor.fetchone()[0]
            stats[table] = {"row_count": count}

            # Get sync stats if sync_status column exists
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s AND column_name = 'sync_status'
            """, (table,))

            if cursor.fetchone():
                cursor.execute(
                    sql.SQL("""
                        SELECT sync_status, COUNT(*)
                        FROM {}
                        GROUP BY sync_status
                    """).format(sql.Identifier(table))
                )
                stats[table]["sync_stats"] = dict(cursor.fetchall())

        cursor.close()
        conn.close()

        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {}


def init_database(reset: bool = False, schema_path: Path = None):
    """Initialize the database with schema."""
    logger.info("=" * 60)
    logger.info("Database Initialization")
    logger.info("=" * 60)
    logger.info(f"Host: {DB_HOST}:{DB_PORT}")
    logger.info(f"Database: {DB_NAME}")
    logger.info(f"User: {DB_USER}")
    logger.info(f"Reset: {reset}")
    logger.info("=" * 60)

    if reset:
        logger.warning("RESET MODE: Dropping existing database!")
        drop_database()

    create_database()
    run_schema(schema_path)

    # Show stats
    stats = get_table_stats()
    logger.info("\nDatabase Tables:")
    for table, info in stats.items():
        logger.info(f"  - {table}: {info.get('row_count', 0)} rows")
        if "sync_stats" in info:
            logger.info(f"    Sync: {info['sync_stats']}")

    logger.info("\nDatabase initialization complete!")
    return True


def main():
    parser = argparse.ArgumentParser(description="Initialize database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate database"
    )
    parser.add_argument(
        "--schema",
        type=Path,
        help="Path to schema SQL file"
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Only show database statistics"
    )

    args = parser.parse_args()

    if args.stats_only:
        if not database_exists():
            logger.error(f"Database {DB_NAME} does not exist")
            sys.exit(1)

        stats = get_table_stats()
        print("\nDatabase Statistics:")
        print("=" * 40)
        for table, info in stats.items():
            print(f"\n{table}:")
            print(f"  Rows: {info.get('row_count', 0)}")
            if "sync_stats" in info:
                print(f"  Sync Status:")
                for status, count in info["sync_stats"].items():
                    print(f"    - {status}: {count}")
    else:
        try:
            init_database(reset=args.reset, schema_path=args.schema)
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
