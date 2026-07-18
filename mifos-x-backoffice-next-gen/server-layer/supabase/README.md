# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/server-layer/supabase/README.md"
# last_modified: "2026-03-19"

# Server Layer - Supabase

**Project**: mifos-x-backoffice-next-gen
**Server Type**: Supabase (PostgreSQL + Edge Functions + Data Pipeline)
**Last Updated**: 2026-07-17

---

## Architecture

```
server-layer/
├── supabase-backend/          # API Implementation
│   ├── config.toml            # Supabase configuration
│   ├── seed.sql               # Initial data
│   ├── migrations/            # Schema migrations
│   └── functions/             # Edge Functions
│       └── _shared/           # Shared utilities
│
└── supabase-engine/           # Data Pipeline
    ├── pipeline.py            # CLI orchestrator
    ├── extract/               # Data extraction
    ├── transform/             # Data transformation
    ├── load/                  # Data loading & sync
    ├── validate/              # Data validation
    ├── enrich/                # AI/API enrichment
    └── data/                  # Local data storage
```

---

## Quick Start

### Backend Setup

```bash
# 1. Setup credentials
cp .env.example .env
# Edit .env with your Supabase credentials

# 2. Initialize Supabase (if not linked)
cd supabase-backend
supabase link --project-ref YOUR_PROJECT_REF

# 3. Start local development
supabase start

# 4. Apply migrations
supabase db reset  # Resets, migrates, and seeds

# 5. Deploy to production
supabase db push
supabase functions deploy
```

### Pipeline Setup

```bash
# 1. Install dependencies
cd supabase-engine
pip install -r requirements.txt

# 2. Check status
python pipeline.py status

# 3. Run pipeline
python pipeline.py all
```

---

## Environment Variables

Required in `.env`:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database (for direct access)
SUPABASE_DB_URL=postgresql://postgres:password@db.your-project.supabase.co:5432/postgres

# Optional: External APIs
ANTHROPIC_API_KEY=your-claude-api-key
```

---

## Commands Reference

### supabase-backend (Supabase CLI)

| Command | Purpose |
|---------|---------|
| `supabase start` | Start local Supabase |
| `supabase stop` | Stop local Supabase |
| `supabase db reset` | Reset + migrate + seed |
| `supabase db diff -f name` | Generate migration |
| `supabase db push` | Push to remote |
| `supabase functions serve` | Run functions locally |
| `supabase functions deploy` | Deploy functions |

### supabase-engine (Pipeline CLI)

| Command | Purpose |
|---------|---------|
| `python pipeline.py status` | Show pipeline status |
| `python pipeline.py extract` | Run extraction |
| `python pipeline.py transform` | Run transformation |
| `python pipeline.py load` | Load to staging |
| `python pipeline.py validate` | Run validation |
| `python pipeline.py sync` | Sync to Supabase |
| `python pipeline.py all` | Full pipeline |

---

## Development Workflow

### Adding a New API

1. Design API in `idea-layer/exports/{feature}/API.md`
2. Create migration: `supabase db diff -f feature_name`
3. Add RLS policies in migration
4. Test locally: `supabase db reset`
5. Deploy: `supabase db push`

### Adding an Edge Function

1. Create folder: `supabase-backend/functions/{function-name}/`
2. Add `index.ts` with handler
3. Test locally: `supabase functions serve {function-name}`
4. Deploy: `supabase functions deploy {function-name}`

### Adding Data Source

1. Create extractor in `supabase-engine/extract/adapters/`
2. Register in factory
3. Add transform strategies if needed
4. Configure in pipeline.py
5. Test: `python pipeline.py extract --source name`

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `LAYER_STATUS.md` | Implementation tracking |
| `../idea-layer/exports/*/API.md` | API specifications |
| Framework `BACKEND.md` | Backend patterns |
| Framework `ENGINE.md` | Pipeline patterns |

---

## Troubleshooting

### Backend Issues

```bash
# Check Supabase status
supabase status

# View logs
supabase logs

# Reset completely
supabase stop && supabase start
supabase db reset
```

### Pipeline Issues

```bash
# Check staging database
python pipeline.py status

# View dirty records
sqlite3 data/staging.db "SELECT COUNT(*) FROM staged_data WHERE synced=0"

# Force re-sync
sqlite3 data/staging.db "UPDATE staged_data SET synced=0"
python pipeline.py sync
```
