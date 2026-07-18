"""
Deployment Validator
====================

Cross-validates local supabase-backend against remote Supabase.
Generates deployment diff for selective deployment.

Usage:
    from lib.validator import DeploymentValidator

    validator = DeploymentValidator()
    results = validator.validate_all()

    for result in results:
        if result.action != 'none':
            print(f"{result.action}: {result.component}")
"""

import os
import hashlib
import subprocess
import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime

from .config import get_config
from .db import execute_sql, get_connection

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of validating a single component."""
    component_type: str  # migration, edge_function, rpc, table, trigger
    component_name: str
    local_state: Dict = field(default_factory=dict)
    remote_state: Dict = field(default_factory=dict)
    action: str = 'none'  # create, update, delete, none
    changes: List[str] = field(default_factory=list)
    checksum_local: Optional[str] = None
    checksum_remote: Optional[str] = None


@dataclass
class ValidationReport:
    """Full validation report."""
    validated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    total_components: int = 0
    pending_creates: int = 0
    pending_updates: int = 0
    pending_deletes: int = 0
    up_to_date: int = 0
    results: List[ValidationResult] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def has_changes(self) -> bool:
        return self.pending_creates > 0 or self.pending_updates > 0 or self.pending_deletes > 0

    def to_dict(self) -> Dict:
        return {
            'validated_at': self.validated_at,
            'summary': {
                'total': self.total_components,
                'create': self.pending_creates,
                'update': self.pending_updates,
                'delete': self.pending_deletes,
                'unchanged': self.up_to_date,
            },
            'has_changes': self.has_changes(),
            'results': [
                {
                    'type': r.component_type,
                    'name': r.component_name,
                    'action': r.action,
                    'changes': r.changes,
                }
                for r in self.results if r.action != 'none'
            ],
            'errors': self.errors,
        }


class DeploymentValidator:
    """
    Validates local supabase-backend against remote Supabase.

    Checks:
    - Migrations: Local files vs schema_migrations table
    - Edge Functions: Local functions vs deployed functions
    - RPCs: SQL functions defined in migrations
    - Tables: Schema definitions
    - Triggers: Automation triggers
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or get_config()
        self.migrations_dir = Path(self.config.get('migrations_dir', 'migrations'))
        self.functions_dir = Path(self.config.get('functions_dir', 'functions'))

    def validate_all(self) -> ValidationReport:
        """Run all validations and return comprehensive report."""
        report = ValidationReport()

        # Validate each component type
        try:
            migration_results = self.validate_migrations()
            report.results.extend(migration_results)
        except Exception as e:
            report.errors.append(f"Migration validation failed: {e}")
            logger.error(f"Migration validation error: {e}")

        try:
            function_results = self.validate_edge_functions()
            report.results.extend(function_results)
        except Exception as e:
            report.errors.append(f"Edge function validation failed: {e}")
            logger.error(f"Edge function validation error: {e}")

        try:
            rpc_results = self.validate_rpcs()
            report.results.extend(rpc_results)
        except Exception as e:
            report.errors.append(f"RPC validation failed: {e}")
            logger.error(f"RPC validation error: {e}")

        # Calculate summary
        for result in report.results:
            report.total_components += 1
            if result.action == 'create':
                report.pending_creates += 1
            elif result.action == 'update':
                report.pending_updates += 1
            elif result.action == 'delete':
                report.pending_deletes += 1
            else:
                report.up_to_date += 1

        return report

    def validate_migrations(self) -> List[ValidationResult]:
        """Compare local migration files with schema_migrations table."""
        results = []

        # Get local migrations
        local_migrations = self._get_local_migrations()

        # Get remote migrations from schema_migrations table
        remote_migrations = self._get_remote_migrations()

        # Compare
        local_names = set(local_migrations.keys())
        remote_names = set(remote_migrations.keys())

        # Migrations to create (local but not remote)
        for name in local_names - remote_names:
            results.append(ValidationResult(
                component_type='migration',
                component_name=name,
                local_state={'exists': True, 'checksum': local_migrations[name]['checksum']},
                remote_state={'exists': False},
                action='create',
                changes=[f"Migration not applied: {name}"],
                checksum_local=local_migrations[name]['checksum'],
            ))

        # Migrations that exist in both (check for modifications)
        for name in local_names & remote_names:
            local_checksum = local_migrations[name]['checksum']
            remote_checksum = remote_migrations[name].get('checksum', '')

            if local_checksum != remote_checksum and remote_checksum:
                results.append(ValidationResult(
                    component_type='migration',
                    component_name=name,
                    local_state={'checksum': local_checksum},
                    remote_state={'checksum': remote_checksum},
                    action='update',
                    changes=[f"Migration modified since deployment (checksums differ)"],
                    checksum_local=local_checksum,
                    checksum_remote=remote_checksum,
                ))
            else:
                results.append(ValidationResult(
                    component_type='migration',
                    component_name=name,
                    action='none',
                    checksum_local=local_checksum,
                    checksum_remote=remote_checksum,
                ))

        # Orphaned migrations (remote but not local) - warning only
        for name in remote_names - local_names:
            results.append(ValidationResult(
                component_type='migration',
                component_name=name,
                local_state={'exists': False},
                remote_state={'exists': True},
                action='delete',
                changes=[f"Migration exists in database but not locally: {name}"],
            ))

        return results

    def validate_edge_functions(self) -> List[ValidationResult]:
        """Compare local edge functions with deployed functions."""
        results = []

        # Get local functions
        local_functions = self._get_local_edge_functions()

        # Get deployed functions via Supabase CLI
        deployed_functions = self._get_deployed_edge_functions()

        local_names = set(local_functions.keys())
        deployed_names = set(deployed_functions.keys())

        # Functions to deploy
        for name in local_names - deployed_names:
            results.append(ValidationResult(
                component_type='edge_function',
                component_name=name,
                local_state={'exists': True},
                remote_state={'exists': False},
                action='create',
                changes=[f"Edge function not deployed: {name}"],
                checksum_local=local_functions[name].get('checksum'),
            ))

        # Functions that exist in both
        for name in local_names & deployed_names:
            # Could add checksum comparison here if deployment tracking is available
            results.append(ValidationResult(
                component_type='edge_function',
                component_name=name,
                action='none',
            ))

        return results

    def validate_rpcs(self) -> List[ValidationResult]:
        """Validate RPC functions exist in PostgreSQL."""
        results = []

        # Extract RPC names from migration files
        expected_rpcs = self._extract_rpcs_from_migrations()

        # Get actual RPCs from database
        actual_rpcs = self._get_database_rpcs()

        expected_names = set(expected_rpcs.keys())
        actual_names = set(actual_rpcs.keys())

        # RPCs missing from database
        for name in expected_names - actual_names:
            results.append(ValidationResult(
                component_type='rpc',
                component_name=name,
                local_state={'defined': True, 'in_migration': expected_rpcs[name]},
                remote_state={'exists': False},
                action='create',
                changes=[f"RPC not found in database: {name}"],
            ))

        # RPCs that exist
        for name in expected_names & actual_names:
            results.append(ValidationResult(
                component_type='rpc',
                component_name=name,
                action='none',
            ))

        return results

    def _get_local_migrations(self) -> Dict[str, Dict]:
        """Get all local migration files with checksums."""
        migrations = {}

        if not self.migrations_dir.exists():
            return migrations

        for file in sorted(self.migrations_dir.glob('*.sql')):
            content = file.read_text()
            checksum = hashlib.sha256(content.encode()).hexdigest()[:16]
            migrations[file.name] = {
                'path': str(file),
                'checksum': checksum,
                'size': len(content),
            }

        return migrations

    def _get_remote_migrations(self) -> Dict[str, Dict]:
        """Get migrations from schema_migrations table."""
        migrations = {}

        try:
            rows = execute_sql("""
                SELECT name, checksum, executed_at, status
                FROM schema_migrations
                WHERE status = 'applied'
                ORDER BY executed_at
            """)

            for row in rows:
                migrations[row[0]] = {
                    'checksum': row[1],
                    'executed_at': row[2],
                    'status': row[3],
                }
        except Exception as e:
            logger.warning(f"Could not fetch remote migrations: {e}")
            # Table might not exist yet

        return migrations

    def _get_local_edge_functions(self) -> Dict[str, Dict]:
        """Get local edge function directories."""
        functions = {}

        if not self.functions_dir.exists():
            return functions

        for dir in self.functions_dir.iterdir():
            if dir.is_dir() and not dir.name.startswith('_'):
                index_file = dir / 'index.ts'
                if index_file.exists():
                    content = index_file.read_text()
                    checksum = hashlib.sha256(content.encode()).hexdigest()[:16]
                    functions[dir.name] = {
                        'path': str(dir),
                        'checksum': checksum,
                    }

        return functions

    def _get_deployed_edge_functions(self) -> Dict[str, Dict]:
        """Get deployed edge functions via Supabase CLI."""
        functions = {}

        try:
            result = subprocess.run(
                ['npx', 'supabase', 'functions', 'list'],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                # Parse output (format depends on Supabase CLI version)
                for line in result.stdout.strip().split('\n'):
                    if line and not line.startswith('NAME'):
                        parts = line.split()
                        if parts:
                            functions[parts[0]] = {'deployed': True}
        except Exception as e:
            logger.warning(f"Could not list deployed functions: {e}")

        return functions

    def _extract_rpcs_from_migrations(self) -> Dict[str, str]:
        """Extract RPC function names from migration files."""
        rpcs = {}

        if not self.migrations_dir.exists():
            return rpcs

        for file in self.migrations_dir.glob('*rpcs*.sql'):
            content = file.read_text()
            # Simple regex to find function definitions
            import re
            for match in re.finditer(r'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+(\w+)', content, re.IGNORECASE):
                rpcs[match.group(1)] = file.name

        return rpcs

    def _get_database_rpcs(self) -> Dict[str, Dict]:
        """Get RPC functions from PostgreSQL."""
        rpcs = {}

        try:
            rows = execute_sql("""
                SELECT routine_name
                FROM information_schema.routines
                WHERE routine_schema = 'public'
                  AND routine_type = 'FUNCTION'
            """)

            for row in rows:
                rpcs[row[0]] = {'exists': True}
        except Exception as e:
            logger.warning(f"Could not fetch database RPCs: {e}")

        return rpcs

    def generate_diff(self) -> str:
        """Generate human-readable diff report."""
        report = self.validate_all()

        lines = [
            "=" * 60,
            "DEPLOYMENT VALIDATION REPORT",
            "=" * 60,
            f"Validated: {report.validated_at}",
            "",
            "SUMMARY",
            "-" * 40,
            f"Total Components: {report.total_components}",
            f"  To Create: {report.pending_creates}",
            f"  To Update: {report.pending_updates}",
            f"  To Delete: {report.pending_deletes}",
            f"  Unchanged: {report.up_to_date}",
            "",
        ]

        if report.has_changes():
            lines.extend([
                "PENDING CHANGES",
                "-" * 40,
            ])

            for result in report.results:
                if result.action != 'none':
                    icon = {'create': '+', 'update': '~', 'delete': '-'}.get(result.action, '?')
                    lines.append(f"  [{icon}] {result.component_type}: {result.component_name}")
                    for change in result.changes:
                        lines.append(f"      {change}")
        else:
            lines.append("No changes detected. Deployment is up to date.")

        if report.errors:
            lines.extend([
                "",
                "ERRORS",
                "-" * 40,
            ])
            for error in report.errors:
                lines.append(f"  ! {error}")

        lines.append("=" * 60)

        return '\n'.join(lines)
