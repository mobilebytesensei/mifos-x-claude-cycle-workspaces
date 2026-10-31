# template_meta
# template_version: "2.87.0"
# template_path: "templates/blueprints/workspace-project/server-layer/supabase/SERVER_SCHEMA_VERSION_REGISTRY.md"
# last_modified: "2026-03-28"

# Server Schema Version Registry

> **Purpose**: Track which schema objects are deployed where (local vs production) and their test status.
> **Updated by**: `/server deploy`, `/server test`, `/server evolve`
> **Consumed by**: RULE-SERVER-CONTRACT-001, RULE-SERVER-DELTA-001

---

## Schema Objects

| Object | Type | Migration | Version | Local | Production | Last Tested |
|--------|------|-----------|---------|:-----:|:----------:|:-----------:|
| `movies` | TABLE | `20260305000001_initial.sql` | 1.0.0 | ✅ | ✅ | 2026-03-28 |
| `user_moods` | TABLE | `20260305000002_user_tables.sql` | 1.0.0 | ✅ | ✅ | 2026-03-28 |
| `get_featured_movies` | RPC | `20260305000003_home_rpcs.sql` | 1.2.0 | ✅ | ✅ | 2026-03-28 |
| `movies_select_public` | POLICY | `20260305000004_rls_policies.sql` | 1.0.0 | ✅ | ✅ | 2026-03-28 |
| _...add rows as schema objects are created..._ | | | | | | |

---

## Version Legend

| Field | Description |
|-------|-------------|
| Object | Table, RPC function, policy, index, or trigger name |
| Type | TABLE, RPC, POLICY, INDEX, TRIGGER, EDGE_FUNCTION |
| Migration | Migration file that created/last modified this object |
| Version | Semantic version of this object (bumped on modification) |
| Local | ✅ deployed to local Supabase, ❌ not deployed |
| Production | ✅ deployed to production, ❌ not deployed, ⚠️ stale |
| Last Tested | Date of last successful test run |

---

## Drift Detection

Objects where Local ≠ Production indicate drift:

| Drift Type | Meaning | Action |
|------------|---------|--------|
| Local ✅, Prod ❌ | New object not yet deployed to production | Run `/server deploy` |
| Local ❌, Prod ✅ | Object removed locally but still in production | Run migration to remove |
| Local ✅, Prod ⚠️ | Object modified locally, production stale | Run `/server deploy --selective` |

---

## Auto-Update Rules

1. After `/server deploy` → Update Production column to ✅, set Last Tested
2. After `/server test` → Update Last Tested column
3. After migration creation → Add new row or update Version
4. After `/server evolve` → Update Version, set Production to ⚠️ (stale)
