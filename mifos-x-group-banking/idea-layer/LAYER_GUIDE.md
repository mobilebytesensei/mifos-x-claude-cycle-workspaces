---
_blueprint:
  version: "2.88.0"
  date: "2026-05-05"
  layer: "idea-layer"
  project: "mifos-x-group-banking"
  scaffolded_at: "2026-05-05"
---

# Idea Layer Guide — mifos-x-group-banking

> Source of truth for all product intent. Downstream layers are generated from here.

## Structure

```
idea-layer/
├── idea-plan.yaml        # 15-phase plan · quality 98%
├── IDEA.md               # Vision · personas · value props
├── FEATURES.md           # Feature registry (15 features)
├── REQUIREMENTS.md       # FR/NFR requirements
├── design-tokens.yaml    # Design token definitions
├── PROJECT_DEMO_DATA.yaml
├── screens/              # Per-feature screen YAMLs (enrich pending)
├── flows/                # User flow YAMLs (enrich pending)
└── assets/
```

## Commands

| Command | Purpose |
|---------|---------|
| `/idea` | Dashboard |
| `/idea enrich` | Generate screen YAMLs |
| `/idea export` | SPEC.md + API.md per feature |
| `/idea-plan` | Refine planning sections |
