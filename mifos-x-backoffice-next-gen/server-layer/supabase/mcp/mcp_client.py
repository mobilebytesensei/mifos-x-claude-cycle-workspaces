"""
Supabase MCP Client

Unified client for all Supabase operations via MCP (Model Context Protocol).
Used by both supabase-backend (schema) and supabase-engine (data).

Rule Reference: RULE-SERVER-MCP-001
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Optional
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


@dataclass
class TableSchema:
    """Schema definition for table creation."""
    name: str
    columns: list[dict]
    primary_key: str = "id"
    rls_enabled: bool = True
    indexes: list[dict] = None
    policies: list[dict] = None

    def to_sql(self) -> str:
        """Generate CREATE TABLE SQL."""
        cols = []
        for col in self.columns:
            col_def = f"{col['name']} {col['type']}"
            if col.get('primary_key'):
                col_def += " PRIMARY KEY"
            if col.get('default'):
                col_def += f" DEFAULT {col['default']}"
            if not col.get('nullable', True):
                col_def += " NOT NULL"
            cols.append(col_def)

        sql = f"""
CREATE TABLE IF NOT EXISTS public.{self.name} (
    {','.join(cols)},
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
"""
        if self.rls_enabled:
            sql += f"\nALTER TABLE public.{self.name} ENABLE ROW LEVEL SECURITY;"

        return sql


@dataclass
class RPCFunction:
    """RPC function definition."""
    name: str
    params: list[dict]
    returns: str
    body: str
    security: str = "DEFINER"
    language: str = "plpgsql"

    def to_sql(self) -> str:
        """Generate CREATE FUNCTION SQL."""
        param_list = ", ".join([
            f"{p['name']} {p['type']}" + (f" DEFAULT {p['default']}" if p.get('default') else "")
            for p in self.params
        ])

        return f"""
CREATE OR REPLACE FUNCTION public.{self.name}({param_list})
RETURNS {self.returns}
LANGUAGE {self.language}
SECURITY {self.security}
AS $$
BEGIN
    {self.body}
END;
$$;
"""


@dataclass
class SyncResult:
    """Result of sync operation."""
    synced: int
    errors: int
    error_messages: list[str] = None


class SupabaseMCPClient:
    """
    Unified MCP client for Supabase operations.

    Used by:
    - supabase-backend: Schema operations (tables, functions, policies)
    - supabase-engine: Data operations (sync, seed, query)
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize MCP client.

        Args:
            config_path: Path to config file. If None, uses defaults.
        """
        self.config = self._load_config(config_path)
        self._mcp = None  # MCP connection (injected by framework)

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file or use defaults."""
        defaults = {
            "timeout_ms": 30000,
            "retry_count": 3,
            "retry_delay_ms": 1000,
            "batch_size": 1000,
            "log_operations": True,
        }

        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                file_config = yaml.safe_load(f)
                return {**defaults, **file_config.get("mcp_client", {})}

        return defaults

    # =========================================================================
    # SCHEMA OPERATIONS (supabase-backend)
    # =========================================================================

    async def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists in Supabase.

        Args:
            table_name: Name of table to check

        Returns:
            True if table exists, False otherwise
        """
        result = await self._call_mcp("list_tables")
        tables = [t["name"] for t in result.get("tables", [])]
        exists = table_name in tables

        self._log("table_exists", table_name, "EXISTS" if exists else "NOT_FOUND")
        return exists

    async def create_table(self, schema: TableSchema) -> bool:
        """
        Create table via MCP.

        Args:
            schema: TableSchema definition

        Returns:
            True if created successfully
        """
        sql = schema.to_sql()
        await self._execute_sql(sql)
        self._log("create_table", schema.name, "CREATED")
        return True

    async def create_rpc(self, function: RPCFunction) -> bool:
        """
        Create RPC function via MCP.

        Args:
            function: RPCFunction definition

        Returns:
            True if created successfully
        """
        sql = function.to_sql()
        await self._execute_sql(sql)
        self._log("create_rpc", function.name, "CREATED")
        return True

    async def function_exists(self, function_name: str) -> bool:
        """
        Check if RPC function exists.

        Args:
            function_name: Name of function to check

        Returns:
            True if function exists
        """
        sql = f"""
        SELECT EXISTS (
            SELECT FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname = 'public'
            AND p.proname = '{function_name}'
        );
        """
        result = await self._execute_sql(sql)
        exists = result.get("data", [[False]])[0][0]

        self._log("function_exists", function_name, "EXISTS" if exists else "NOT_FOUND")
        return exists

    async def deploy_edge_function(
        self,
        name: str,
        code: str,
        verify_jwt: bool = True
    ) -> bool:
        """
        Deploy edge function via MCP.

        Args:
            name: Function name
            code: TypeScript code
            verify_jwt: Whether to verify JWT

        Returns:
            True if deployed successfully
        """
        await self._call_mcp("deploy_function", {
            "name": name,
            "code": code,
            "verify_jwt": verify_jwt
        })
        self._log("deploy_edge_function", name, "DEPLOYED")
        return True

    async def edge_function_exists(self, name: str) -> bool:
        """
        Check if edge function exists.

        Args:
            name: Function name

        Returns:
            True if function exists
        """
        result = await self._call_mcp("list_functions")
        functions = [f["name"] for f in result.get("functions", [])]
        exists = name in functions

        self._log("edge_function_exists", name, "EXISTS" if exists else "NOT_FOUND")
        return exists

    # =========================================================================
    # DATA OPERATIONS (supabase-engine)
    # =========================================================================

    async def upsert_batch(
        self,
        table: str,
        rows: list[dict],
        on_conflict: str = "id",
        chunk_size: Optional[int] = None
    ) -> int:
        """
        Batch upsert with chunking.

        Args:
            table: Table name
            rows: Rows to upsert
            on_conflict: Conflict column for upsert
            chunk_size: Rows per batch (default from config)

        Returns:
            Number of rows upserted
        """
        chunk_size = chunk_size or self.config["batch_size"]
        total = 0

        for i in range(0, len(rows), chunk_size):
            chunk = rows[i:i + chunk_size]
            await self._call_mcp("upsert_rows", {
                "table": table,
                "rows": chunk,
                "on_conflict": on_conflict
            })
            total += len(chunk)

        self._log("upsert_batch", table, f"{total} rows")
        return total

    async def sync_dirty_rows(
        self,
        table: str,
        dirty_rows: list[dict],
        tracking_columns: list[str] = None
    ) -> SyncResult:
        """
        Sync only dirty rows (incremental sync).

        Args:
            table: Table name
            dirty_rows: Rows marked as dirty
            tracking_columns: Columns to strip before sync (local-only)

        Returns:
            SyncResult with counts
        """
        tracking_columns = tracking_columns or [
            "sync_status", "synced_at", "local_updated_at", "sync_error"
        ]

        # Strip tracking columns
        sync_data = []
        for row in dirty_rows:
            clean_row = {k: v for k, v in row.items() if k not in tracking_columns}
            sync_data.append(clean_row)

        synced = 0
        errors = 0
        error_messages = []

        try:
            synced = await self.upsert_batch(table, sync_data)
        except Exception as e:
            errors = len(sync_data)
            error_messages.append(str(e))

        result = SyncResult(synced=synced, errors=errors, error_messages=error_messages)
        self._log("sync_dirty_rows", table, f"{synced} synced, {errors} errors")
        return result

    async def query(
        self,
        table: str,
        select: str = "*",
        filters: dict = None,
        limit: int = 100,
        order_by: str = None
    ) -> list[dict]:
        """
        Query data from table.

        Args:
            table: Table name
            select: Columns to select
            filters: Filter conditions
            limit: Max rows
            order_by: Order column

        Returns:
            List of rows
        """
        result = await self._call_mcp("select_rows", {
            "table": table,
            "select": select,
            "filters": filters or {},
            "limit": limit,
            "order_by": order_by
        })

        rows = result.get("data", [])
        self._log("query", table, f"{len(rows)} rows")
        return rows

    async def delete_rows(
        self,
        table: str,
        filters: dict
    ) -> int:
        """
        Delete rows matching filters.

        Args:
            table: Table name
            filters: Filter conditions

        Returns:
            Number of rows deleted
        """
        result = await self._call_mcp("delete_rows", {
            "table": table,
            "filters": filters
        })

        count = result.get("count", 0)
        self._log("delete_rows", table, f"{count} deleted")
        return count

    # =========================================================================
    # INTERNAL METHODS
    # =========================================================================

    async def _call_mcp(self, tool: str, params: dict = None) -> dict:
        """
        Call MCP tool with retry logic.

        Args:
            tool: MCP tool name
            params: Tool parameters

        Returns:
            Tool result
        """
        return await self._execute_with_retry(
            lambda: self._mcp_call(tool, params or {})
        )

    async def _mcp_call(self, tool: str, params: dict) -> dict:
        """
        Execute MCP tool call.

        Note: In actual implementation, this connects to the MCP server.
        The framework injects the MCP connection.
        """
        # This is a placeholder - actual implementation depends on MCP SDK
        # In Claude Code, MCP calls are made through the framework
        raise NotImplementedError(
            "MCP connection must be provided by framework. "
            "Use client.set_mcp_connection(mcp) to inject."
        )

    def set_mcp_connection(self, mcp: Any):
        """Inject MCP connection from framework."""
        self._mcp = mcp

    async def _execute_sql(self, sql: str) -> dict:
        """Execute raw SQL via MCP."""
        return await self._call_mcp("execute_sql", {"sql": sql})

    async def _execute_with_retry(self, operation) -> Any:
        """Execute operation with exponential backoff retry."""
        max_retries = self.config["retry_count"]
        base_delay = self.config["retry_delay_ms"] / 1000

        for attempt in range(max_retries):
            try:
                return await operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                if self._is_retriable(e):
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    raise

    def _is_retriable(self, error: Exception) -> bool:
        """Check if error is retriable."""
        retriable_types = (
            ConnectionError,
            TimeoutError,
            # Add other retriable error types
        )
        return isinstance(error, retriable_types)

    def _log(self, operation: str, target: str, result: str):
        """Log operation if logging enabled."""
        if self.config["log_operations"]:
            logger.info(f"[MCP] {operation} | {target} | {result}")
