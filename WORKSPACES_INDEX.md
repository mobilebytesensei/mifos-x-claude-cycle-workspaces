# Workspaces Index - O(1) Lookup

> Per-project workspace directory for claude-product-cycle

**Last Updated**: 2026-05-09

---

## Registered Workspaces

| # | Project | Type | Status | Progress | Workspace Path |
|:-:|---------|------|:------:|:--------:|----------------|
| 1 | mifos-mobile | Self-Service Banking | Active | 79% | `workspaces/mifos-mobile/` |
| 2 | mifos-x-group-banking | Group Banking (KMP) | Active | 45% | `workspaces/mifos-x/mifos-x-group-banking/` |
| 3 | mifos-x-field-officer-app | Field Officer App (KMP) | Planning | 10% | `workspaces/mifos-x/mifos-x-field-officer-app/` |
| 4 | kmp-project-template | KMP Project Template | Active | 80% | `workspaces/mifos-x/kmp-project-template/` |
| 5 | mcp-mifosx | Mifos X MCP Server | Active | 60% | `workspaces/mifos-x/mcp-mifosx/` |
| 6 | mobile-wallet | Mobile Wallet (KMP) | Planning | 5% | `workspaces/mifos-x/mobile-wallet/` |

---

## Workspace Structure

Each project workspace contains:

```
workspaces/[project]/
├── PROJECT.md           # Project configuration & context
├── CURRENT_WORK.md      # Active work tracking
├── design-spec-layer/   # Design specifications & mockups
│   ├── STATUS.md
│   ├── FEATURES_INDEX.md
│   └── features/
├── server-layer/        # API documentation
│   ├── SERVER_CONFIG.md
│   └── API_INDEX.md
├── client-layer/        # Network & data layer tracking
│   ├── LAYER_STATUS.md
│   └── FEATURE_MAP.md
├── feature-layer/       # UI layer tracking
│   ├── LAYER_STATUS.md
│   ├── MODULES_INDEX.md
│   └── SCREENS_INDEX.md
├── platform-layer/      # Platform-specific tracking
│   ├── android/
│   ├── ios/
│   ├── desktop/
│   └── web/
└── testing-layer/       # Test coverage tracking
    ├── LAYER_STATUS.md
    └── TEST_TAGS_INDEX.md
```

---

## Commands

```bash
# Set active project (reads from this workspace)
/project-set [name]

# List all projects
/project-list

# Add new project (creates workspace)
/project-add [name]

# Check active project status
/gap-analysis
```

---

## O(1) Access Pattern

```bash
# Access workspace
workspaces/[project-name]/

# Access layer
workspaces/[project-name]/[layer]-layer/

# Access feature design
workspaces/[project-name]/design-spec-layer/features/[feature]/
```

---

## Migration Complete

All mifos-mobile layers have been migrated to `workspaces/mifos-mobile/`.

Commands now use workspace paths automatically based on `ACTIVE_PROJECT`.
