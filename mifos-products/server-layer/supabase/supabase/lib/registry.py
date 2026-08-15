"""
API Registry module for Supabase CRUD Engine.
Parses API.md files and determines implementation approach.

Implementation types are determined by API.md specifications:
- table: Direct table access via selectAsFlow (simple CRUD)
- rpc: RPC function (complex queries, aggregations)
- realtime: Realtime subscriptions
- auth: Supabase Auth API
- storage: Supabase Storage API
"""

import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from .config import Config
from .db import Database


@dataclass
class APIEndpoint:
    """Represents an API endpoint from design layer."""
    method: str  # GET, POST, PUT, DELETE
    path: str  # /api/v1/items/:id
    description: str
    feature: str
    impl_type: str = 'table'  # table, rpc, realtime, auth, storage
    realtime: bool = False
    request_dto: Optional[str] = None
    response_dto: Optional[str] = None
    status: str = 'planned'  # planned, implemented, deprecated


@dataclass
class ServerRequirement:
    """Definition for what needs to exist on server."""
    name: str
    table_name: str
    impl_type: str  # table, rpc, realtime, auth, storage
    operation: str  # list, get, create, update, delete, custom
    parameters: list[tuple[str, str]] = field(default_factory=list)
    returns: str = 'json'
    feature: str = ''
    realtime: bool = False


# Backwards compatibility alias
RPCDefinition = ServerRequirement


class RPCRegistry:
    """Registry for managing RPCs and generating migrations."""

    def __init__(self, config: Config, db: Database):
        self.config = config
        self.db = db

    def parse_api_md(self, api_path: Path, feature: str) -> list[APIEndpoint]:
        """Parse an API.md file and extract endpoints."""
        if not api_path.exists():
            return []

        content = api_path.read_text()
        endpoints = []

        # Pattern to match endpoint definitions
        # Matches: | GET | /api/v1/items | List all items | ItemListResponse |
        table_pattern = r'\|\s*(GET|POST|PUT|DELETE|PATCH)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'

        for match in re.finditer(table_pattern, content):
            method = match.group(1).strip()
            path = match.group(2).strip()
            description = match.group(3).strip()

            endpoints.append(APIEndpoint(
                method=method,
                path=path,
                description=description,
                feature=feature
            ))

        return endpoints

    def endpoint_to_rpc(self, endpoint: APIEndpoint) -> Optional[RPCDefinition]:
        """Convert an API endpoint to an RPC definition."""

        # Extract resource name from path
        # /api/v1/movies -> movies
        # /api/v1/movies/:id -> movies
        path_parts = endpoint.path.strip('/').split('/')
        resource = None
        for part in reversed(path_parts):
            if not part.startswith(':') and part not in ['api', 'v1', 'v2']:
                resource = part
                break

        if not resource:
            return None

        # Determine operation and RPC name
        has_id = ':id' in endpoint.path or '/{id}' in endpoint.path

        if endpoint.method == 'GET':
            if has_id:
                return RPCDefinition(
                    name=f'rpc_get_{self._singularize(resource)}_by_id',
                    table_name=resource,
                    operation='get',
                    parameters=[('p_id', 'uuid')],
                    returns='json',
                    feature=endpoint.feature
                )
            else:
                return RPCDefinition(
                    name=f'rpc_get_{resource}',
                    table_name=resource,
                    operation='list',
                    parameters=[('p_limit', 'integer'), ('p_offset', 'integer')],
                    returns='json',
                    feature=endpoint.feature
                )

        elif endpoint.method == 'POST':
            return RPCDefinition(
                name=f'rpc_create_{self._singularize(resource)}',
                table_name=resource,
                operation='create',
                parameters=[('p_data', 'json')],
                returns='uuid',
                feature=endpoint.feature
            )

        elif endpoint.method in ['PUT', 'PATCH']:
            return RPCDefinition(
                name=f'rpc_update_{self._singularize(resource)}',
                table_name=resource,
                operation='update',
                parameters=[('p_id', 'uuid'), ('p_data', 'json')],
                returns='boolean',
                feature=endpoint.feature
            )

        elif endpoint.method == 'DELETE':
            return RPCDefinition(
                name=f'rpc_delete_{self._singularize(resource)}',
                table_name=resource,
                operation='delete',
                parameters=[('p_id', 'uuid')],
                returns='boolean',
                feature=endpoint.feature
            )

        return None

    def _singularize(self, word: str) -> str:
        """Simple singularization (movies -> movie)."""
        if word.endswith('ies'):
            return word[:-3] + 'y'
        elif word.endswith('es'):
            return word[:-2]
        elif word.endswith('s') and not word.endswith('ss'):
            return word[:-1]
        return word

    def get_required_rpcs(self) -> list[RPCDefinition]:
        """Get all RPCs required by design layer APIs."""
        rpcs = []
        seen_names = set()

        for feature_path in self.config.get_all_feature_paths():
            api_path = feature_path / 'API.md'
            feature_name = feature_path.name

            endpoints = self.parse_api_md(api_path, feature_name)

            for endpoint in endpoints:
                rpc = self.endpoint_to_rpc(endpoint)
                if rpc and rpc.name not in seen_names:
                    rpcs.append(rpc)
                    seen_names.add(rpc.name)

        return rpcs

    def get_missing_rpcs(self) -> list[RPCDefinition]:
        """Get RPCs that are required but not deployed."""
        required = self.get_required_rpcs()
        deployed = self.db.get_rpc_names()

        return [rpc for rpc in required if rpc.name not in deployed]

    def generate_rpc_sql(self, rpc: RPCDefinition) -> str:
        """Generate SQL for a single RPC."""

        params_sql = ', '.join([f'{name} {dtype}' for name, dtype in rpc.parameters])

        if rpc.operation == 'list':
            return f"""
-- RPC: {rpc.name}
-- Feature: {rpc.feature}
-- Generated by claude-product-cycle CRUD engine

CREATE OR REPLACE FUNCTION {rpc.name}({params_sql})
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result json;
BEGIN
    SELECT json_agg(row_to_json(t))
    INTO result
    FROM (
        SELECT *
        FROM {rpc.table_name}
        ORDER BY created_at DESC
        LIMIT p_limit
        OFFSET p_offset
    ) t;

    RETURN COALESCE(result, '[]'::json);
END;
$$;

GRANT EXECUTE ON FUNCTION {rpc.name}({', '.join([dtype for _, dtype in rpc.parameters])}) TO authenticated;
GRANT EXECUTE ON FUNCTION {rpc.name}({', '.join([dtype for _, dtype in rpc.parameters])}) TO anon;
"""

        elif rpc.operation == 'get':
            return f"""
-- RPC: {rpc.name}
-- Feature: {rpc.feature}
-- Generated by claude-product-cycle CRUD engine

CREATE OR REPLACE FUNCTION {rpc.name}({params_sql})
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result json;
BEGIN
    SELECT row_to_json(t)
    INTO result
    FROM {rpc.table_name} t
    WHERE id = p_id;

    RETURN result;
END;
$$;

GRANT EXECUTE ON FUNCTION {rpc.name}({', '.join([dtype for _, dtype in rpc.parameters])}) TO authenticated;
"""

        elif rpc.operation == 'create':
            return f"""
-- RPC: {rpc.name}
-- Feature: {rpc.feature}
-- Generated by claude-product-cycle CRUD engine

CREATE OR REPLACE FUNCTION {rpc.name}({params_sql})
RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    new_id uuid;
BEGIN
    INSERT INTO {rpc.table_name}
    SELECT * FROM json_populate_record(null::{rpc.table_name}, p_data)
    RETURNING id INTO new_id;

    RETURN new_id;
END;
$$;

GRANT EXECUTE ON FUNCTION {rpc.name}({', '.join([dtype for _, dtype in rpc.parameters])}) TO authenticated;
"""

        elif rpc.operation == 'update':
            return f"""
-- RPC: {rpc.name}
-- Feature: {rpc.feature}
-- Generated by claude-product-cycle CRUD engine

CREATE OR REPLACE FUNCTION {rpc.name}({params_sql})
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    UPDATE {rpc.table_name}
    SET
        updated_at = now()
        -- Add field updates from p_data as needed
    WHERE id = p_id;

    RETURN FOUND;
END;
$$;

GRANT EXECUTE ON FUNCTION {rpc.name}({', '.join([dtype for _, dtype in rpc.parameters])}) TO authenticated;
"""

        elif rpc.operation == 'delete':
            return f"""
-- RPC: {rpc.name}
-- Feature: {rpc.feature}
-- Generated by claude-product-cycle CRUD engine

CREATE OR REPLACE FUNCTION {rpc.name}({params_sql})
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    DELETE FROM {rpc.table_name}
    WHERE id = p_id;

    RETURN FOUND;
END;
$$;

GRANT EXECUTE ON FUNCTION {rpc.name}({', '.join([dtype for _, dtype in rpc.parameters])}) TO authenticated;
"""

        return ''

    def generate_migration_file(self, rpcs: list[RPCDefinition], feature: str) -> Optional[Path]:
        """Generate a migration file for a set of RPCs."""
        if not rpcs:
            return None

        # Create migration filename
        timestamp = datetime.now().strftime('%Y%m%d')
        existing = list(self.config.migrations_path.glob(f'{timestamp}_*.sql'))
        sequence = len(existing) + 1

        filename = f"{timestamp}_{sequence:03d}_rpcs_{feature}.sql"
        filepath = self.config.migrations_path / filename

        # Generate SQL content
        header = f"""-- Migration: {filename}
-- Feature: {feature}
-- Generated: {datetime.now().isoformat()}
-- RPCs: {len(rpcs)}
--
-- This migration was auto-generated by the claude-product-cycle CRUD engine.
-- Review before applying to production.

BEGIN;

"""

        footer = """
COMMIT;
"""

        sql_parts = [self.generate_rpc_sql(rpc) for rpc in rpcs]
        content = header + '\n'.join(sql_parts) + footer

        # Write file
        self.config.migrations_path.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)

        return filepath

    def sync_apis(self) -> dict[str, list[Path]]:
        """Sync all APIs and generate migrations. Returns dict of feature -> migration files."""
        result = {}

        # Group missing RPCs by feature
        missing = self.get_missing_rpcs()
        by_feature: dict[str, list[RPCDefinition]] = {}

        for rpc in missing:
            if rpc.feature not in by_feature:
                by_feature[rpc.feature] = []
            by_feature[rpc.feature].append(rpc)

        # Generate migration for each feature
        for feature, rpcs in by_feature.items():
            migration_path = self.generate_migration_file(rpcs, feature)
            if migration_path:
                result[feature] = [migration_path]

        return result
