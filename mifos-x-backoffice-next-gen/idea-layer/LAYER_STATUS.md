# template_meta
# template_version: "2.87.0"
# template_path: "templates/blueprints/workspace-project/idea-layer/LAYER_STATUS.md"

# Idea Layer Status — mifos-x-backoffice-next-gen

| Attribute | Value |
|-----------|-------|
| IDEA.md | present (master spec — enriched) |
| REQUIREMENTS.md | 14 requirements (8 FR · 3 NFR · 3 SEC) |
| FEATURES.md | 21 features (4 foundation + 17 modules) |
| ROADMAP.md | phased (P0–P6) |
| APP_FLOW.mmd | not generated (run `/idea-sync`) |
| DEV_STATUS.md | initialized |

---

## Data Flow

| Attribute | Value |
|-----------|-------|
| source_of_truth | idea-layer |
| bootstrapped | false |
| bootstrapped_from | — |
| bootstrapped_at | — |

> When `bootstrapped: true`, idea-layer was reverse-engineered from
> existing sources (one-time). After bootstrap, idea-layer is the
> master and exports/mockups are generated via `/idea export`.

---

## Import State

| Attribute | Value |
|-----------|-------|
| bootstrapped | false |
| bootstrapped_at | — |
| bootstrap_source | — |
| bootstrap_mode | — |
| sources_used | — |

> When `bootstrapped: true`, idea-layer was built via `/idea sync` STATE A bootstrap
> (source scan + Idea Decomposition Engine). Bootstrap is re-runnable (idempotent).
> and supersedes bootstrap data with more comprehensive analysis.
