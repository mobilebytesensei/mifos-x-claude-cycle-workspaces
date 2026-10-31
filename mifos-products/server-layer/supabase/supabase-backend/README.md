# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/server-layer/supabase/supabase-backend/README.md"
# last_modified: "2026-03-19"

# Supabase Backend

**Project**: mifos-products
**Purpose**: API implementation using Supabase

---

## Structure

```
supabase-backend/
├── config.toml                 # Supabase CLI configuration
├── seed.sql                    # Initial seed data
├── migrations/                 # Schema migrations
│   └── YYYYMMDDHHMMSS_*.sql   # Timestamped SQL files
└── functions/                  # Edge Functions
    ├── _shared/               # Shared utilities
    │   ├── cors.ts            # CORS headers
    │   ├── supabase.ts        # Supabase client
    │   └── response.ts        # Response helpers
    └── {function-name}/       # Individual functions
        └── index.ts           # Function entry point
```

---

## Quick Start

```bash
# Link to Supabase project
supabase link --project-ref YOUR_PROJECT_REF

# Start local development
supabase start

# Apply migrations and seed
supabase db reset

# Deploy to production
supabase db push
supabase functions deploy
```

---

## Development Workflow

### Creating a Migration

```bash
# Option 1: Write SQL directly
# Create: migrations/YYYYMMDDHHMMSS_description.sql

# Option 2: Generate from Dashboard changes
supabase db diff -f migration_name

# Apply migration locally
supabase db reset
```

### Creating an Edge Function

```bash
# Create function directory
mkdir -p functions/my-function

# Create index.ts (see _shared/ for utilities)
# Test locally
supabase functions serve my-function

# Deploy
supabase functions deploy my-function
```

---

## CLI Commands

| Command | Purpose |
|---------|---------|
| `supabase start` | Start local Supabase stack |
| `supabase stop` | Stop local stack |
| `supabase status` | Check status |
| `supabase db reset` | Reset + migrate + seed |
| `supabase db diff -f name` | Generate migration from changes |
| `supabase db push` | Push migrations to remote |
| `supabase functions serve` | Run functions locally |
| `supabase functions deploy` | Deploy functions to production |
| `supabase link` | Link to remote project |

---

## Configuration

### config.toml

Key sections:
- `[api]` - API settings
- `[auth]` - Authentication configuration
- `[auth.external.*]` - OAuth providers
- `[storage.buckets.*]` - Storage bucket settings

### Environment Variables

Secrets for Edge Functions are set via:
```bash
supabase secrets set KEY=value
```

Access in functions via:
```typescript
Deno.env.get('KEY')
```

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| Framework `BACKEND.md` | Complete pattern reference |
| `../idea-layer/exports/*/API.md` | API specifications |
| [Supabase Docs](https://supabase.com/docs) | Official documentation |
