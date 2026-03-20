# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/design-spec-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-20"

# Design Layer Guide - mifos-mobile

> Conventions and patterns for the design specification layer.

---

## Purpose

The design layer contains feature specifications, mockups, and design tokens that serve as the source of truth for implementation.

---

## Directory Structure

```
design-spec-layer/
├── STATUS.md              # Layer status overview
├── FEATURES_INDEX.md      # O(1) feature lookup
├── MOCKUPS_INDEX.md       # Mockup file index
├── DESIGN_TOKENS_INDEX.md # Design tokens reference
├── TESTING_STATUS.md      # Design validation status
├── TOOL_CONFIG.md         # Design tool configuration
├── LAYER_GUIDE.md         # This file
├── _shared/               # Shared components & patterns
│   ├── COMPONENTS.md      # Reusable UI components
│   ├── PATTERNS.md        # Common UI patterns
│   └── API_REFERENCE.md   # Shared API patterns
├── mockup-tools/          # Mockup generation tools
│   └── README.md
└── features/              # Per-feature specs
    └── {feature}/
        ├── SPEC.md        # Feature specification
        ├── API.md         # API requirements
        ├── MOCKUP.md      # Mockup documentation
        ├── STATUS.md      # Feature status
        └── mockups/       # Generated mockups
            ├── PROMPTS_FIGMA.md
            ├── PROMPTS_STITCH.md
            └── *.png
```

---

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. CREATE SPEC                                              │
│     /design [feature] spec → Creates SPEC.md                │
├─────────────────────────────────────────────────────────────┤
│  2. DEFINE API                                               │
│     /design [feature] api → Creates API.md                  │
├─────────────────────────────────────────────────────────────┤
│  3. GENERATE MOCKUPS                                         │
│     /design [feature] mockup → Creates mockups              │
├─────────────────────────────────────────────────────────────┤
│  4. TRACK STATUS                                             │
│     Update STATUS.md as work progresses                     │
└─────────────────────────────────────────────────────────────┘
```

---

## SPEC.md Structure

Every feature spec must include:

1. **Overview** - Brief description
2. **User Stories** - As a [user], I want [action], so that [benefit]
3. **Screens** - List of screens with descriptions
4. **User Flows** - Step-by-step interactions
5. **API Requirements** - Link to API.md
6. **Design Considerations** - Edge cases, accessibility

---

## File Templates

See `templates/features/` for spec and mockup templates:
- `SPEC_TEMPLATE.md` - Feature specification
- `API_TEMPLATE.md` - API documentation
- `STATUS_TEMPLATE.md` - Status tracking
- `MOCKUP_TEMPLATE.md` - Mockup documentation

---

## Status Legend

| Status | Meaning |
|:------:|---------|
| ✅ | Complete (all files present and reviewed) |
| ⚠️ | Partial (missing some files) |
| ❌ | Not started |
| 🔄 | In progress |

---

## Commands

| Command | Purpose |
|---------|---------|
| `/design [feature]` | Full design workflow |
| `/design [feature] spec` | Specification only |
| `/design [feature] mockup` | Generate mockups |
| `/gap-analysis design` | Check design gaps |
| `/enforce-index features` | Validate FEATURES_INDEX |
