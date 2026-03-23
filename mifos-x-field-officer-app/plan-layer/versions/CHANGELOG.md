# template_meta
# template_version: "2.86.5"
# template_path: "templates/blueprints/workspace-project/plan-layer/versions/CHANGELOG.md"
# last_modified: "2026-03-20"

# v${VERSION} Changelog - ${PROJECT_NAME}

> Layer-by-layer changes for version ${VERSION}

**Release Date**: ${RELEASE_DATE}
**Previous Version**: v${PREVIOUS_VERSION}
**Tag**: `v${VERSION}`

---

## Summary

${RELEASE_SUMMARY}

---

## Highlights

- ${HIGHLIGHT_1}
- ${HIGHLIGHT_2}
- ${HIGHLIGHT_3}

---

## Layer Changes

### Design Layer

| Change | Features | Type |
|--------|----------|:----:|
| ${CHANGE_DESCRIPTION} | ${FEATURES} | Added/Updated/Removed |

**Files Changed:**
- `design-spec-layer/features/${FEATURE}/SPEC.md`

---

### Server Layer

| Change | Endpoints | Type |
|--------|-----------|:----:|
| ${CHANGE_DESCRIPTION} | ${ENDPOINTS} | Added/Updated/Deprecated |

**API Version**: v${API_VERSION}

**Files Changed:**
- `server-layer/API_INDEX.md`

---

### Client Layer

| Change | Components | Type |
|--------|------------|:----:|
| ${CHANGE_DESCRIPTION} | ${COMPONENTS} | Added/Updated/Removed |

**Files Changed:**
- `client-layer/SERVICES_INDEX.md`

---

### Feature Layer

| Change | Modules | Type |
|--------|---------|:----:|
| ${CHANGE_DESCRIPTION} | ${MODULES} | Added/Updated/Removed |

**Stats:**
- ViewModels: +${VM_ADDED} / -${VM_REMOVED}
- Screens: +${SCREEN_ADDED} / -${SCREEN_REMOVED}

**Files Changed:**
- `feature-layer/MODULES_INDEX.md`

---

### Platform Layer

| Platform | Change | Status |
|----------|--------|:------:|
| Android | ${CHANGE} | ${STATUS} |
| iOS | ${CHANGE} | ${STATUS} |
| Desktop | ${CHANGE} | ${STATUS} |
| Web | ${CHANGE} | ${STATUS} |

---

### Testing Layer

| Change | Coverage | Type |
|--------|:--------:|:----:|
| ${CHANGE_DESCRIPTION} | ${COVERAGE}% | Added/Updated |

---

## Breaking Changes

| Change | Migration |
|--------|-----------|
| ${BREAKING_CHANGE} | ${MIGRATION_STEPS} |

---

## Deprecations

| Deprecated | Replacement | Remove In |
|------------|-------------|:---------:|
| ${DEPRECATED_ITEM} | ${REPLACEMENT} | v${REMOVE_VERSION} |

---

## Migration Guide

### From v${PREVIOUS_VERSION} to v${VERSION}

1. ${MIGRATION_STEP_1}
2. ${MIGRATION_STEP_2}
3. ${MIGRATION_STEP_3}

---

## Contributors

- ${CONTRIBUTOR_1}
- ${CONTRIBUTOR_2}

---

## Full Changelog

See [GitHub Compare](${GITHUB_COMPARE_URL}) for all commits.
