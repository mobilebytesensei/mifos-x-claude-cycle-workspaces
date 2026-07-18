# template_meta
# template_version: "2.86.0"
# template_path: "core/blueprints/workspace-project/idea-layer/REGISTRY_COVERAGE.md"
# generated_by: "/project-add layer scaffold (derived-scan over idea-layer/screens/ inventory; TAG_REGISTRY.yaml not yet generated)"

# Registry Coverage — mifos-x-backoffice-next-gen

> **Version**: 1.0
> **Last Updated**: 2026-07-17
> **Status**: Draft — derived-scan over `screens/` inventory; regenerated on screen/tag change.
> **Source of truth**: `idea-layer/TAG_REGISTRY.yaml` (not yet generated) + `idea-layer/screens/` inventory

---

## Coverage Summary

21 screen/feature module directories are materialized under `idea-layer/screens/` (4 foundation + 17 back-office modules). `TAG_REGISTRY.yaml` has **not** been generated yet, so analytics-tag coverage is 0/21 — the single biggest coverage gap. Run `/idea-sync` to derive the tag registry and per-screen tag emitters. Per-feature sibling artifacts (`ui.yaml`, `flow.yaml`, `docs.yaml`, `preview/`) are enriched incrementally by `/idea-feature-enrich` + `/idea-sync`.

| Metric | Value | Target |
|--------|-------|--------|
| Screens with ≥1 tag | 0 / 21 | 100% |
| Tags with ≥1 emitter | 0 / 0 (registry not yet generated) | 100% |

---

## Per-Registry Coverage

> Analytics tags are derived by `/idea-sync` from screen definitions into `TAG_REGISTRY.yaml`.

### Tag Coverage

| Tag | Emitting screen(s) | Event type |
|-----|--------------------|------------|
| — | _(TAG_REGISTRY.yaml not yet generated — run `/idea-sync`)_ | — |

### Screen Inventory

> The 21 module directories present under `idea-layer/screens/`.

| Screen / Feature module | Status |
|-------------------------|--------|
| permission-capability-engine (foundation) | scaffolded |
| offline-sync-engine (foundation) | scaffolded |
| dynamic-template-forms (foundation) | scaffolded |
| needs-attention-inbox (foundation) | scaffolded |
| m01-dashboard | scaffolded |
| m02-clients | scaffolded |
| m03-groups-centers | scaffolded |
| m04-loan-portfolio | scaffolded |
| m05-savings-deposits-shares | scaffolded |
| m06-collections | scaffolded |
| m07-accounting | scaffolded |
| m08-products-charges | scaffolded |
| m09-organization | scaffolded |
| m10-users-roles-permissions | scaffolded |
| m11-tellers-cash | scaffolded |
| m12-datatables-config | scaffolded |
| m13-scheduler-jobs | scaffolded |
| m14-reports-search-audit | scaffolded |
| m15-approvals-makerchecker | scaffolded |
| m16-communications | scaffolded |
| m17-sync-settings | scaffolded |

### Coverage Gaps

- `TAG_REGISTRY.yaml` not yet generated → 0/21 screens carry analytics tags. Run `/idea-sync` to derive it.
- Per-feature sibling artifacts (`ui.yaml`/`flow.yaml`/`docs.yaml`/`preview/`) are enriched incrementally — track via `/idea-sync` and `idea-layer/state/PIPELINE_STATE.yaml`.
