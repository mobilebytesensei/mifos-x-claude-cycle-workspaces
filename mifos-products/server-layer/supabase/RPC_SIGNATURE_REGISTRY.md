# template_meta
# template_version: "2.87.0"
# template_path: "templates/blueprints/workspace-project/server-layer/supabase/RPC_SIGNATURE_REGISTRY.md"
# last_modified: "2026-03-28"

# RPC Signature Registry

> **Purpose**: Single source of truth for all RPC function signatures — prevents overloads, enables drift detection and contract validation.
> **Updated by**: `/server sync-apis`, `/server test contract`, `/server evolve`
> **Consumed by**: RULE-SERVER-CONTRACT-001, RULE-SERVER-DELTA-001

---

## Registry

| Function | Feature | Parameters | Returns | API.md DTO | Contract | Last Verified |
|----------|---------|------------|---------|------------|:--------:|:-------------:|
| `get_featured_movies` | home | `p_limit INT=20, p_offset INT=0` | `TABLE(movie_id UUID, title TEXT, poster_url TEXT, rating DECIMAL, tagline TEXT)` | `FeaturedMovieDto` | ✅ | 2026-03-28 |
| `get_filtered_movies_paged` | home | `p_user_mood_id UUID, p_emotion_ids UUID[], p_genre_ids UUID[], p_limit INT=20, p_offset INT=0` | `TABLE(movie_id UUID, title TEXT, ...)` | `FilteredMovieDto` | ✅ | 2026-03-28 |
| _...add rows as RPC functions are created..._ | | | | | | |

---

## Field Definitions

| Field | Description |
|-------|-------------|
| Function | PostgreSQL function name (must be unique — no overloads) |
| Feature | Which feature this RPC belongs to |
| Parameters | Function signature: `name TYPE=default, ...` |
| Returns | `TABLE(col TYPE, ...)` or `SETOF type` |
| API.md DTO | Kotlin DTO class name from API.md |
| Contract | ✅ validated, ❌ mismatch, ⚠️ untested |
| Last Verified | Date of last contract test run |

---

## Overload Detection

This registry enforces **one signature per function name**. If `pg_proc` shows multiple entries for the same `proname`, it's an error:

```sql
-- DETECT: Find overloaded functions
SELECT proname, COUNT(*) as signatures
FROM pg_proc p JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
GROUP BY proname HAVING COUNT(*) > 1;

-- FIX: Drop all overloads, recreate single canonical version
DROP FUNCTION IF EXISTS public.{name}({old_sig_1});
DROP FUNCTION IF EXISTS public.{name}({old_sig_2});
CREATE OR REPLACE FUNCTION public.{name}({canonical_sig}) ...
```

---

## Delta Detection

Compare this registry against current API.md to detect changes:

| Delta | Detection | Action |
|-------|-----------|--------|
| NEW | In API.md but not in registry | Generate RPC + contract test |
| MODIFIED | In both, signature differs | Generate delta migration + backward-compat check |
| DEPRECATED | Marked `deprecated: true` in API.md | Verify no client usage |
| REMOVED | In registry but not in API.md | Block (must deprecate first) |
| UNCHANGED | Signatures match | Run contract test only |

---

## Backward Compatibility

| Change Type | Safe? | Example |
|-------------|:-----:|---------|
| Add optional param with default | ✅ | `p_genre UUID DEFAULT NULL` |
| Add required param without default | ❌ | `p_genre UUID` (breaks existing callers) |
| Add return column | ✅ | New column ignored by old clients |
| Remove return column | ❌ | Old clients crash on missing field |
| Rename return column | ❌ | Must keep old alias + add new |
| Change param type | ❌ | Requires cast or client update |
