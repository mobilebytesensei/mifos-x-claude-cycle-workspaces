---
_blueprint:
  version: "2.88.0"
  date: "2026-05-05"
  layer: "idea-layer"
  project: "mifos-x-group-banking"
  scaffolded_at: "2026-05-05"
---

# Idea Layer Status — mifos-x-group-banking

| Attribute | Value |
|-----------|-------|
| IDEA.md | ✅ populated |
| REQUIREMENTS.md | 20 requirements |
| FEATURES.md | 15 features |
| idea-plan.yaml | ✅ v1.0 · quality 98% · promoted 2026-05-05 |
| design-tokens.yaml | ✅ present |
| screens/ | ✅ 25 YAMLs enriched (2026-05-05) · avg quality 89% · min 85% |
| flows/ | ✅ 12 YAMLs (9 original 2026-05-05 + 3 added 2026-05-06: member-onboarding, multi-language, field-officer-view) |
| APP_FLOW.mmd | ✅ generated (2026-05-05) |
| TAG_REGISTRY.yaml | ✅ 36 analytics events (2026-05-05) |
| server/ | ✅ api_manifest.yaml + 6 API group files · 42 endpoints (2026-05-05) |
| prototype/ | ✅ index.html — 25-screen browser + 9 flows (2026-05-05) |
| dashboard/ | ✅ DEV_STATUS.md + dev-status.html (2026-05-05) |
| state/ | ✅ PIPELINE_STATE.yaml (2026-05-05) |

**Overall**: ✅ COMPLETE — idea-matrix.md + dashboard/ + APPROVAL_STATUS.md + all siblings present
| CAPABILITY_STATE.yaml | ✅ initialized via /idea init (2026-05-06) — 4 capabilities backfilled |

---

## Data Flow

| Attribute | Value |
|-----------|-------|
| source_of_truth | idea-layer |
| bootstrapped | false |
| creation_mode | wizard → promoted via /idea-plan [P] |
| promoted_at | 2026-05-05 |
| last_sync | 2026-05-05 · /idea sync v1.0.0 |

---

## Commands

| Command | Purpose |
|---------|---------|
| `/idea enrich` | Generate screen YAMLs |
| `/idea export` | Generate SPEC.md + API.md |
| `/idea gap` | Gap analysis |
| `/idea sync` | Full health check |
| `/idea export` | Generate SPEC.md + API.md (next step) |
| `/idea approve --all` | Approve exported features |
| `/implement` | Begin feature implementation |
