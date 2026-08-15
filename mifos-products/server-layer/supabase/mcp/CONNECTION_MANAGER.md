# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/server-layer/supabase/mcp/CONNECTION_MANAGER.md"
# last_modified: "2026-03-19"

# MCP Connection Manager

**Purpose**: Documentation for the unified MCP client used by both supabase-backend and supabase-engine.

---

## Overview

The Connection Manager provides a single interface for all Supabase operations via MCP. It abstracts the MCP protocol details and provides typed methods for common operations.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  supabase-backend              supabase-engine                       │
│  ├── Schema Generator          ├── Seeder                           │
│  ├── RPC Generator             ├── Enricher                         │
│  └── Edge Function Deployer    └── Syncer                           │
│           │                           │                              │
│           └───────────┬───────────────┘                              │
│                       │                                              │
│                       ▼                                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  SupabaseMCPClient (Connection Manager)                      │   │
│  │  ├── Schema Operations                                       │   │
│  │  │     ├── table_exists()                                    │   │
│  │  │     ├── create_table()                                    │   │
│  │  │     ├── create_rpc()                                      │   │
│  │  │     └── deploy_edge_function()                            │   │
│  │  │                                                           │   │
│  │  └── Data Operations                                         │   │
│  │        ├── upsert_batch()                                    │   │
│  │        ├── sync_dirty_rows()                                 │   │
│  │        └── query()                                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                       │                                              │
│                       ▼                                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  MCP Protocol Layer                                          │   │
│  │  ├── mcp.call("execute_sql", {...})                         │   │
│  │  ├── mcp.call("list_tables", {...})                         │   │
│  │  ├── mcp.call("upsert_rows", {...})                         │   │
│  │  └── ...                                                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                       │                                              │
│                       ▼                                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Supabase Server                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Client Interface

### Initialization

```python
from engine.mcp import SupabaseMCPClient

# Initialize with default config
client = SupabaseMCPClient()

# Initialize with custom config path
client = SupabaseMCPClient(config_path="server-layer/config.yaml")
```

### Schema Operations (supabase-backend)

```python
# Check table existence
exists = await client.table_exists("movies")

# Create table
await client.create_table(TableSchema(
    name="movies",
    columns=[
        Column("id", "UUID", primary_key=True),
        Column("title", "TEXT", nullable=False),
        Column("rating", "DECIMAL"),
    ],
    rls_enabled=True
))

# Create RPC function
await client.create_rpc(RPCFunction(
    name="get_popular_movies",
    params=[Param("limit_count", "INT", default=20)],
    returns="TABLE (id UUID, title TEXT, rating DECIMAL)",
    body="SELECT * FROM movies ORDER BY rating DESC LIMIT limit_count"
))

# Deploy edge function
await client.deploy_edge_function(
    name="process-recommendation",
    code=typescript_code,
    verify_jwt=True
)
```

### Data Operations (supabase-engine)

```python
# Batch upsert
count = await client.upsert_batch(
    table="movies",
    rows=movie_data,
    on_conflict="id",
    chunk_size=1000
)

# Sync dirty rows
result = await client.sync_dirty_rows(
    table="movies",
    dirty_rows=dirty_movie_rows
)

# Query data
movies = await client.query(
    table="movies",
    select="id, title, rating",
    filters={"rating": {"gte": 7.0}},
    limit=100
)
```

---

## Error Handling

### Retry Logic

```python
async def _execute_with_retry(self, operation, max_retries=3):
    """Execute operation with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return await operation()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # 1, 2, 4 seconds
```

### Error Types

| Error | Retriable | Action |
|-------|:---------:|--------|
| `ConnectionError` | Yes | Retry with backoff |
| `TimeoutError` | Yes | Retry with backoff |
| `AuthenticationError` | No | Check credentials |
| `ValidationError` | No | Fix input data |
| `RateLimitError` | Yes | Retry after delay |

---

## Configuration

### Default Configuration

```yaml
mcp_client:
  timeout_ms: 30000
  retry_count: 3
  retry_delay_ms: 1000
  batch_size: 1000
  log_operations: true
```

### Per-Operation Configuration

```python
# Override timeout for specific operation
await client.upsert_batch(
    table="large_table",
    rows=large_dataset,
    timeout_ms=120000  # 2 minutes for large operation
)
```

---

## Logging

All operations are logged for debugging and audit:

```
[MCP] 2026-01-21 10:30:45 | table_exists | movies | 45ms | EXISTS
[MCP] 2026-01-21 10:30:46 | create_table | genres | 120ms | CREATED
[MCP] 2026-01-21 10:30:47 | upsert_batch | movies | 1.2s | 1000 rows
[MCP] 2026-01-21 10:30:48 | sync_dirty_rows | movies | 850ms | 500 synced, 0 errors
```

---

## Thread Safety

The MCP client is thread-safe and can be shared across operations:

```python
# Single client instance
client = SupabaseMCPClient()

# Safe for concurrent use
await asyncio.gather(
    client.upsert_batch("movies", movies),
    client.upsert_batch("genres", genres),
    client.upsert_batch("actors", actors)
)
```

---

## Related Files

| File | Purpose |
|------|---------|
| `mcp_client.py` | Implementation |
| `SUPABASE_MCP_CONFIG.md` | Configuration guide |
| `RULE-SERVER-MCP-001.md` | Usage rules |
