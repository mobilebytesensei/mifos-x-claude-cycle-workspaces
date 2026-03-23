# template_meta
# template_version: "2.86.5"
# template_path: "templates/blueprints/workspace-project/server-layer/api-versions/README.md"
# last_modified: "2026-03-20"

# API Versions - ${PROJECT_NAME}

> Version-specific API documentation for breaking changes

---

## Current Versions

| Version | Status | Introduced | Deprecated | Sunset |
|:-------:|:------:|:----------:|:----------:|:------:|
| v1 | Current | v1.0.0 | - | - |

---

## Version Policy

| Policy | Value |
|--------|-------|
| Deprecation Notice | 2 minor versions before removal |
| Sunset Period | 6 months after deprecation |
| Breaking Changes | Major version bump required |

---

## Directory Structure

```
api-versions/
├── README.md              # This file
├── v1/
│   ├── README.md          # v1 API overview
│   ├── MIGRATION.md       # Migration to v1 (from legacy)
│   └── endpoints/
│       ├── auth.md
│       └── accounts.md
└── v2/                    # When v2 is introduced
    ├── README.md
    ├── MIGRATION.md       # v1 → v2 migration guide
    └── endpoints/
```

---

## When to Create New API Version

| Scenario | Action |
|----------|--------|
| New endpoint | Add to current version |
| Endpoint parameter change (additive) | Add to current version |
| Endpoint parameter change (breaking) | New API version |
| Response format change (breaking) | New API version |
| Endpoint removal | Deprecate first, then new version |
| Authentication change | New API version |

---

## Version Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     API VERSION LIFECYCLE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CURRENT                                                      │
│     └─→ Active development, fully supported                     │
│                                                                  │
│  2. DEPRECATED                                                   │
│     └─→ Still works, but marked for removal                     │
│     └─→ Deprecation warnings in responses                       │
│     └─→ Migration guide available                               │
│                                                                  │
│  3. SUNSET                                                       │
│     └─→ Read-only or limited functionality                      │
│     └─→ Final warning period                                    │
│                                                                  │
│  4. REMOVED                                                      │
│     └─→ Returns 410 Gone                                        │
│     └─→ Documentation archived                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```
