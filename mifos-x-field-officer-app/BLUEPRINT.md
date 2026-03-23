# template_meta
# template_version: "2.86.5"
# template_path: "templates/blueprints/workspace-project/BLUEPRINT.md"
# last_modified: "2026-03-20"

# Workspace Project Blueprint

> Default full-stack workspace project scaffold with all 8 layers.

---

## Metadata

```yaml
id: workspace-project
name: "Full-Stack Workspace Project"
type: blueprint
version: "2.0.0"
layers:
  - design-spec-layer
  - server-layer
  - client-layer
  - feature-layer
  - infrastructure-layer
  - platform-layer
  - testing-layer
  - plan-layer
project_types: [kmp, web, backend]
files: 45+
description: "Complete project scaffold with all layers and server variants"
```

---

## Structure

```
workspace-project/
├── BLUEPRINT.md              # This file
├── PROJECT.md                # Project metadata template
├── PROJECT_TYPES.md          # Type-specific configurations
├── LAYER_APPLICABILITY.md    # Layer applicability matrix
├── CURRENT_WORK.md           # Current work tracking template
│
├── design-spec-layer/        # Design & specification
├── server-layer/             # Server (generic)
├── server-layer-supabase/    # Server (Supabase variant)
├── server-layer-rest/        # Server (REST variant)
├── client-layer/             # API clients
├── feature-layer/            # UI features
├── infrastructure-layer/     # Build config, DI
├── platform-layer/           # Platform-specific
├── testing-layer/            # Tests
└── plan-layer/               # Planning
```

---

## Server Variants

| Variant | Directory | Default |
|---------|-----------|:-------:|
| Generic | `server-layer/` | ✅ |
| Supabase | `server-layer-supabase/` | - |
| REST | `server-layer-rest/` | - |

---

## Usage

```bash
/project-add --type kmp      # Creates from this blueprint
/project-add --type web      # Creates from this blueprint
/project-add --type backend  # Creates from this blueprint
```

---

## Layer Applicability by Type

| Layer | KMP | Web | Backend |
|-------|:---:|:---:|:-------:|
| design-spec | ✅ | ✅ | ✅ |
| server | ✅ | ✅ | ✅ |
| client | ✅ | ✅ | - |
| feature | ✅ | ✅ | - |
| infrastructure | ✅ | - | - |
| platform | ✅ | - | - |
| testing | ✅ | ✅ | ✅ |
| plan | ✅ | ✅ | ✅ |
