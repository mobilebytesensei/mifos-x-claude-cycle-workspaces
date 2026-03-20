# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/plan-layer/PLANS_INDEX.md"
# last_modified: "2026-03-20"

# Plans Index - Mifos Mobile

> **Purpose**: O(1) lookup for implementation plans and version roadmap

**Last Updated**: 2025-01-07

---

## Version Planning

See [`versions/VERSION_INDEX.md`](./versions/VERSION_INDEX.md) for version-based planning.

| Version | Status | Focus | Target |
|---------|:------:|-------|--------|
| v0.3.0 | Current | Core features | Complete |
| v0.4.0 | Next | v2.0 UI Redesign | 2025-Q1 |

---

## Quick Overview

| Status | Count | Description |
|:------:|:-----:|-------------|
| 🔄 Active | 0 | Plans in progress |
| ✅ Completed | 1 | Finished plans |
| ⏸️ Paused | 0 | Plans on hold |

---

## Active Plans

| # | Plan | Target | Progress | Current Step | Created |
|:-:|------|--------|:--------:|--------------|---------|
| - | (none) | - | - | - | - |

---

## Completed Plans

| # | Plan | Target | Steps | Completed |
|:-:|------|--------|:-----:|-----------|
| 1 | [design-flow-authentication-260119-001](plans/PLAN-design-flow-authentication-260119-001.md) | User Flow | 3 | 2026-01-19 |

---

## O(1) Path Pattern

```
plan-layer/active/[target]-[type].md     # Active plan
plan-layer/completed/[target]-[type].md  # Completed plan
```

Examples:
- `plan-layer/active/design-mockup.md`
- `plan-layer/active/feature-auth.md`
- `plan-layer/completed/client-layer.md`

---

## Commands

```bash
# Create new plan
/gap-planning [target]         # Creates plan in plan-layer/active/

# Check plan status
/gap-status                    # Shows this index + active plans
/gap-status [plan]             # Shows specific plan progress

# Complete a plan
/gap-status complete [plan]    # Moves to plan-layer/completed/
```
