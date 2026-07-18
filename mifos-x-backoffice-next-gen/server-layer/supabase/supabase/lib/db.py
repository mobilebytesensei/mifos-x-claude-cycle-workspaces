"""
Database module for Supabase CRUD Engine.
Handles PostgreSQL connections and RPC queries.
"""

import subprocess
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from .config import Config


@dataclass
class RPCInfo:
    """Information about a deployed RPC."""
    name: str
    arguments: str
    return_type: str
    schema: str = 'public'


class Database:
    """Database operations for Supabase."""

    def __init__(self, config: Config):
        self.config = config

    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            result = subprocess.run(
                ['psql', self.config.db_url, '-c', 'SELECT 1'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def get_deployed_rpcs(self) -> list[RPCInfo]:
        """Get list of all deployed RPCs from Supabase."""
        query = """
        SELECT
            routine_name,
            COALESCE(
                string_agg(
                    parameter_name || ' ' || data_type,
                    ', ' ORDER BY ordinal_position
                ),
                ''
            ) as arguments,
            (SELECT data_type FROM information_schema.routines r
             WHERE r.routine_name = p.routine_name
             AND r.routine_schema = 'public' LIMIT 1) as return_type
        FROM information_schema.routines r
        LEFT JOIN information_schema.parameters p USING (specific_name)
        WHERE r.routine_schema = 'public'
          AND r.routine_type = 'FUNCTION'
          AND r.routine_name LIKE 'rpc_%'
        GROUP BY routine_name
        ORDER BY routine_name;
        """

        try:
            result = subprocess.run(
                ['psql', self.config.db_url, '-t', '-A', '-F', '|', '-c', query],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                print(f"Query failed: {result.stderr}")
                return []

            rpcs = []
            for line in result.stdout.strip().split('\n'):
                if line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        rpcs.append(RPCInfo(
                            name=parts[0],
                            arguments=parts[1],
                            return_type=parts[2] or 'void'
                        ))

            return rpcs

        except Exception as e:
            print(f"Failed to get RPCs: {e}")
            return []

    def get_rpc_names(self) -> set[str]:
        """Get set of deployed RPC names."""
        return {rpc.name for rpc in self.get_deployed_rpcs()}

    def apply_migration(self, migration_path: Path) -> bool:
        """Apply a single migration file."""
        try:
            result = subprocess.run(
                ['psql', self.config.db_url, '-f', str(migration_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"Migration failed: {result.stderr}")
                return False

            return True

        except Exception as e:
            print(f"Migration error: {e}")
            return False

    def apply_all_migrations(self) -> tuple[int, int]:
        """Apply all pending migrations. Returns (applied, failed) counts."""
        migrations = self.config.get_migration_files()
        applied = 0
        failed = 0

        for migration in migrations:
            print(f"  Applying: {migration.name}")
            if self.apply_migration(migration):
                applied += 1
                print(f"    Applied successfully")
            else:
                failed += 1
                print(f"    FAILED")

        return applied, failed

    def execute_query(self, query: str) -> Optional[str]:
        """Execute a raw SQL query and return output."""
        try:
            result = subprocess.run(
                ['psql', self.config.db_url, '-c', query],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout if result.returncode == 0 else None
        except Exception as e:
            print(f"Query failed: {e}")
            return None

    def get_tables(self) -> list[str]:
        """Get list of all tables in public schema."""
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """

        result = subprocess.run(
            ['psql', self.config.db_url, '-t', '-A', '-c', query],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return []

        return [t.strip() for t in result.stdout.strip().split('\n') if t.strip()]

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        return table_name in self.get_tables()
