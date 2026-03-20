# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/plan-layer/versions/v0.3.0/CHANGELOG.md"
# last_modified: "2026-03-20"

# v0.3.0 Changelog - Mifos Mobile

> Layer-by-layer changes for version 0.3.0

**Release Date**: 2024-12-01
**Previous Version**: -
**Tag**: `v0.3.0`

---

## Summary

Initial KMP release with all 17 core features implemented.

---

## Highlights

- Complete Kotlin Multiplatform migration
- All 17 core features implemented
- Android, iOS, Desktop, Web targets

---

## Layer Changes

### Design Layer

| Change | Features | Type |
|--------|----------|:----:|
| Feature specifications | 17 features | Added |
| API documentation | All endpoints | Added |

**Files Changed:**
- `design-spec-layer/features/*/SPEC.md`
- `design-spec-layer/features/*/API.md`

---

### Server Layer

| Change | Endpoints | Type |
|--------|-----------|:----:|
| Fineract Self-Service API | 50+ endpoints | Added |
| Authentication | OAuth 2.0 | Added |

**API Version**: v1

**Files Changed:**
- `server-layer/API_INDEX.md`

---

### Client Layer

| Change | Components | Type |
|--------|------------|:----:|
| API Services | 12 services | Added |
| Repositories | 10 repositories | Added |
| Models | 30+ models | Added |

**Files Changed:**
- `client-layer/SERVICES_INDEX.md`

---

### Feature Layer

| Change | Modules | Type |
|--------|---------|:----:|
| Feature modules | 17 modules | Added |
| ViewModels | 32 ViewModels | Added |
| Screens | 45+ Screens | Added |

**Stats:**
- ViewModels: +32 / -0
- Screens: +45 / -0

**Files Changed:**
- `feature-layer/MODULES_INDEX.md`

---

### Platform Layer

| Platform | Change | Status |
|----------|--------|:------:|
| Android | Initial implementation | Production |
| iOS | Initial implementation | Beta |
| Desktop | Initial implementation | Alpha |
| Web | Initial implementation | Alpha |

---

### Testing Layer

| Change | Coverage | Type |
|--------|:--------:|:----:|
| Test infrastructure | 35% | Added |
| Fake repositories | - | Added |
| Test fixtures | - | Added |

---

## Breaking Changes

None - Initial release.

---

## Migration Guide

Not applicable - Initial release.

---

## Contributors

- Mifos Mobile Team
- KMP Migration Contributors
