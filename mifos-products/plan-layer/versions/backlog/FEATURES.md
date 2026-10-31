# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/plan-layer/versions/backlog/FEATURES.md"
# last_modified: "2026-03-19"

# Feature Backlog - ${PROJECT_NAME}

> **Purpose**: Track future features not yet scheduled for a version

**Last Updated**: ${DATE}

---

## Backlog Overview

| Priority | Count | Description |
|:--------:|:-----:|-------------|
| P0 | 0 | Critical - must have |
| P1 | 0 | High - should have |
| P2 | 0 | Medium - nice to have |
| P3 | 0 | Low - future consideration |

---

## Feature Backlog

| # | Feature | Priority | Complexity | Notes |
|:-:|---------|:--------:|:----------:|-------|
| - | (none) | - | - | - |

---

## Priority Guidelines

| Priority | Criteria |
|----------|----------|
| P0 | Blocks release, critical bug, security issue |
| P1 | High user value, key functionality |
| P2 | Improves UX, polish features |
| P3 | Future ideas, nice to have |

---

## Complexity Guidelines

| Complexity | Effort | Scope |
|------------|--------|-------|
| S | < 1 day | Single file/component |
| M | 1-3 days | Multiple files, one feature |
| L | 3-7 days | Cross-feature, architecture |
| XL | > 1 week | Major feature, multiple layers |

---

## Moving to Version

When scheduling a feature for a version:

1. Create version folder if needed: `versions/vX.X.X/`
2. Add feature to version SCOPE.md
3. Remove from this backlog
4. Update VERSION_INDEX.md
