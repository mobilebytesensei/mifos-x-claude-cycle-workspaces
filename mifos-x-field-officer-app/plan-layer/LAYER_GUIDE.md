# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/plan-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-19"

# Plan Layer Guide - mifos-x-field-officer-app

> Conventions for feature planning and version management.

---

## Purpose

The plan layer tracks implementation plans, version releases, and feature backlog management.

---

## Directory Structure

```
plan-layer/
├── LAYER_GUIDE.md        # This file
├── PLANS_INDEX.md        # O(1) plan lookup
├── VERSION_INDEX.md      # Version tracking
├── README.md             # Layer overview
├── active/               # In-progress plans
├── completed/            # Finished plans
├── versions/             # Version-specific plans
│   ├── VERSION_INDEX.md  # Version history
│   ├── CHANGELOG.md      # Version changelog
│   ├── PLAN_TEMPLATE.md  # Plan template
│   └── backlog/          # Feature backlog
│       └── FEATURES.md
└── onboarding/           # Onboarding plans
    └── ONBOARDING_PLAN.md
```

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. CREATE PLAN                                                  │
│     Create feature plan in active/                              │
├─────────────────────────────────────────────────────────────────┤
│  2. IMPLEMENT                                                    │
│     Track progress, update status                               │
├─────────────────────────────────────────────────────────────────┤
│  3. COMPLETE                                                     │
│     Move to completed/ when done                                │
├─────────────────────────────────────────────────────────────────┤
│  4. VERSION                                                      │
│     Tag version when releasing                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Plan Structure

Every plan should include:

1. **Objective** - What we're building
2. **Phases** - Implementation phases
3. **Tasks** - Specific tasks per phase
4. **Dependencies** - What it depends on
5. **Success Criteria** - How to verify completion

---

## Commands

| Command | Purpose |
|---------|---------|
| `/gap-analysis plan` | Check plan gaps |
| `/gap-planning` | Create implementation plan |
