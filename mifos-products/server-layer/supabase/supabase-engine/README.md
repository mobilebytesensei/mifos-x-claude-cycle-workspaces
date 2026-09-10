# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/server-layer/supabase/supabase-engine/README.md"
# last_modified: "2026-03-19"

# Supabase Engine - ETL Pipeline

Data pipeline for extracting, transforming, and loading data into Supabase.

**Key Features:**
- 🐘 PostgreSQL-based local storage (Docker)
- ⚡ Fast sync to Supabase (~2,500-4,000 rows/second)
- 🔄 Dirty row sync pattern (incremental updates)
- 🚀 Team-friendly (PostgreSQL vs SQLite)
- 📦 SQLite → PostgreSQL migration tool

## Quick Start

### Option 1: PostgreSQL with Docker (Recommended)

```bash
# 1. Start PostgreSQL container
docker-compose up -d

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Configure environment
cp ../.env.example ../.env
# Edit ../.env with your Supabase credentials

# 4. Initialize database with schema
python db/init_db.py

# 5. Run your extractors/pipeline
python pipeline.py --source api

# 6. Sync to Supabase
python sync/fast_sync.py
```

### Option 2: Migrate from SQLite

If you have existing SQLite data:

```bash
# 1. Start PostgreSQL
docker-compose up -d

# 2. Initialize PostgreSQL schema
python db/init_db.py

# 3. Migrate data from SQLite
python sync/migration.py --source data/staging.db

# 4. Sync to Supabase
python sync/fast_sync.py
```

## Structure

```
supabase-engine/
├── docker-compose.yml    # PostgreSQL container setup
├── docker-compose.template.yml  # Template with placeholders
├── pipeline.py           # Main orchestrator
├── config.py             # Runtime configuration
├── config.template.py    # Configuration template
├── requirements.txt      # Dependencies
├── db/                   # Database setup
│   ├── schema.sql        # PostgreSQL schema with sync tracking
│   ├── SCHEMA_TEMPLATE.sql  # Schema template
│   └── init_db.py        # Database initialization
├── sync/                 # Sync utilities
│   ├── fast_sync.py      # PostgreSQL → Supabase sync
│   └── migration.py      # SQLite → PostgreSQL migration
├── extract/              # Data extraction
│   ├── base.py           # Base extractor
│   └── adapters/         # Source-specific adapters
├── transform/            # Data transformation
│   ├── base.py           # Base transformer
│   └── strategies/       # Transform strategies
├── load/                 # Data loading
│   ├── base.py           # Base loader
│   ├── staging.py        # Local staging
│   └── supabase_sync.py  # Supabase sync
├── validate/             # Data validation
│   └── validators.py     # Validation rules
├── enrich/               # Data enrichment
│   └── enrichers.py      # Enrichment logic
├── data/                 # Data storage
│   └── sources/          # Source configurations
└── tests/                # Pipeline tests
```

## Pipeline Flow

```
Extract → Transform → Validate → Enrich → Load
   │          │          │          │        │
   ▼          ▼          ▼          ▼        ▼
 Source    Clean &    Check      Add      Staging
  Data    Normalize   Rules    Metadata    → Sync
```

## Usage Examples

### Run Full Pipeline

```python
from pipeline import Pipeline

pipeline = Pipeline(config_path="config.py")
pipeline.run(source="api", destination="supabase")
```

### Extract Only

```python
from extract.base import Extractor
from extract.adapters.api_adapter import ApiAdapter

extractor = Extractor(adapter=ApiAdapter(url="https://api.example.com"))
data = extractor.extract()
```

### Transform Data

```python
from transform.base import Transformer
from transform.strategies.cleaner import CleanerStrategy

transformer = Transformer()
transformer.add_strategy(CleanerStrategy())
clean_data = transformer.transform(raw_data)
```

### Load to Supabase

```python
from load.supabase_sync import SupabaseSync

sync = SupabaseSync(table="movies")
sync.upsert(transformed_data)
```

## Adding New Sources

1. Create adapter in `extract/adapters/`:

```python
# extract/adapters/my_source.py
from extract.base import BaseAdapter

class MySourceAdapter(BaseAdapter):
    def fetch(self) -> list[dict]:
        # Implement data fetching
        return [{"id": 1, "name": "Item"}]
```

2. Register in `extract/__init__.py`:

```python
from .adapters.my_source import MySourceAdapter
ADAPTERS["my_source"] = MySourceAdapter
```

3. Use in pipeline:

```python
pipeline.run(source="my_source", destination="supabase")
```

## Configuration

See `config.py` for all options:

```python
CONFIG = {
    "sources": {
        "api": {"url": "...", "api_key": "..."},
    },
    "transforms": ["clean", "normalize", "dedupe"],
    "destination": {
        "type": "supabase",
        "table": "items",
    },
    "sync": {
        "mode": "incremental",  # or "full"
        "batch_size": 100,
    }
}
```

## Testing

```bash
# Run tests
pytest tests/

# Test specific adapter
pytest tests/test_extract.py -k "api_adapter"
```

## PostgreSQL Setup

### Docker Compose Configuration

The `docker-compose.yml` provides:
- PostgreSQL 15 Alpine (lightweight image)
- Persistent data volume
- Auto-initialization from `db/schema.sql`
- Health checks

```yaml
# Example configuration
services:
  postgres:
    image: postgres:15-alpine
    container_name: mood_movies_engine
    environment:
      POSTGRES_DB: mood_movies
      POSTGRES_USER: engine
      POSTGRES_PASSWORD: local_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/schema.sql:/docker-entrypoint-initdb.d/01_schema.sql
```

### Schema with Sync Tracking

Tables include sync tracking columns:

```sql
sync_status TEXT NOT NULL DEFAULT 'pending'
    CHECK (sync_status IN ('pending', 'synced', 'dirty', 'error')),
sync_timestamp TIMESTAMPTZ,
sync_error TEXT
```

**Sync statuses:**
- `pending`: New row, needs initial sync
- `synced`: Successfully synced to Supabase
- `dirty`: Modified since last sync
- `error`: Sync failed (check `sync_error`)

A trigger automatically marks rows as `dirty` when updated:

```sql
CREATE TRIGGER trigger_movies_dirty
    BEFORE UPDATE ON movies
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION mark_movies_dirty();
```

## Sync Operations

### Check Sync Status

```bash
python sync/fast_sync.py --status-only
```

Output:
```
Sync status for movies:
------------------------------
  dirty: 1,234 (5.2%)
  error: 12 (0.1%)
  pending: 2,500 (10.5%)
  synced: 20,000 (84.2%)
------------------------------
  Total: 23,746
```

### Sync Dirty/Pending Rows

```bash
python sync/fast_sync.py
```

### Full Re-sync

```bash
python sync/fast_sync.py --full
```

### Sync Performance

| Batch Size | Speed | 1M Records | Notes |
|------------|-------|------------|-------|
| 100 | ~500/sec | ~33 min | Safe for rate limits |
| 500 | ~1,500/sec | ~11 min | Balanced |
| 1000 | ~2,500-4,000/sec | ~4-7 min | Recommended |
| 2000 | ~4,000-5,000/sec | ~3-5 min | High memory |

## Migration from SQLite

If you have an existing SQLite staging database:

```bash
# List tables in SQLite
python sync/migration.py --source data/staging.db --list-tables

# Migrate all tables
python sync/migration.py --source data/staging.db

# Migrate specific table
python sync/migration.py --source data/staging.db --table movies

# Dry run (see what would happen)
python sync/migration.py --source data/staging.db --dry-run
```

## Environment Variables

Create `.env` file:

```bash
# Local PostgreSQL (Docker)
DATABASE_URL=postgresql://engine:local_dev@localhost:5432/mood_movies
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mood_movies
DB_USER=engine
DB_PASSWORD=local_dev

# Supabase Remote
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key

# Sync Settings
BATCH_SIZE=1000
LOG_LEVEL=INFO
```

## Creating a New Project

1. Copy templates:
   ```bash
   cp docker-compose.template.yml docker-compose.yml
   cp config.template.py config.py
   cp db/SCHEMA_TEMPLATE.sql db/schema.sql
   ```

2. Replace template variables:
   - `{PROJECT_NAME}` → your project name
   - `{CONTAINER_NAME}` → container name
   - `{POSTGRES_USER}` → database user
   - `{POSTGRES_PASSWORD}` → database password
   - `{PRIMARY_TABLE}` → main table name

3. Customize schema for your data model

4. Start Docker and initialize:
   ```bash
   docker-compose up -d
   python db/init_db.py
   ```

## Rules

This module follows these framework rules:
- **RULE-ENGINE-AUTO-001**: Auto-Generate Seeders
- **RULE-ENGINE-AUTO-002**: Auto-Generate Enrichers
- **RULE-ENGINE-SYNC-001**: Dirty Row Synchronization
