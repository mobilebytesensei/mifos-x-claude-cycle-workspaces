# Project: kmp-project-template

**Created**: 2026-03-27
**Status**: Active
**Type**: Multi-platform App (KMP)

project_type: kmp

---

## Framework Version

| Status | Version | Date |
|--------|:-------:|:----:|
| Generated With | v2.86.0 | 2026-03-27 |
| Last Migrated | v2.86.0 | 2026-03-27 |
| Migration Status | Up to date |

---

## Idea & Purpose

KMP Multi-Module Project Generator — production-ready Kotlin Multiplatform template with comprehensive CI/CD infrastructure spanning 5 platforms and 9 deployment targets. Enables shared business logic and UI components across Android, iOS, Desktop, and Web.

**Target Users**: Kotlin developers building cross-platform applications with shared code.

---

## Repository

| Setting | Value |
|---------|-------|
| GitHub | [openMF/kmp-project-template](https://github.com/openMF/kmp-project-template) |
| Mode | Existing Repository (Import) |
| Default Branch | dev |

---

## Tech Stack

| Component | Choice |
|-----------|--------|
| Language | Kotlin |
| UI Framework | Compose Multiplatform |
| Architecture | MVI (Model-View-Intent) |
| DI | Koin |
| Navigation | Compose Navigation |
| Networking | Ktor |
| Database | Room / SQLDelight |
| DataStore | Multiplatform DataStore |
| CI/CD | GitHub Actions + Fastlane |

---

## Platforms

| Platform | Module | Status |
|----------|--------|:------:|
| Android | cmp-android | ✅ |
| iOS | cmp-ios | ✅ |
| Desktop | cmp-desktop | ✅ |
| Web | cmp-web | ✅ |

---

## Modules

### Feature Modules (3)
- `feature:home` — Home screen
- `feature:profile` — User profile
- `feature:settings` — App settings

### Core Modules (10)
- `core:analytics`, `core:common`, `core:data`, `core:database`
- `core:datastore`, `core:designsystem`, `core:domain`, `core:model`
- `core:network`, `core:ui`

### Core-Base Modules (7)
- `core-base:analytics`, `core-base:common`, `core-base:database`
- `core-base:designsystem`, `core-base:network`, `core-base:platform`, `core-base:ui`

### Platform Modules (5)
- `cmp-android`, `cmp-ios`, `cmp-desktop`, `cmp-web`, `cmp-shared`, `cmp-navigation`

---

## Layers Configuration

| Layer | Status |
|-------|:------:|
| idea-layer | ✅ Enabled |
| design-spec-layer | ✅ Enabled |
| server-layer | ✅ Enabled |
| client-layer | ✅ Enabled |
| feature-layer | ✅ Enabled |
| infrastructure-layer | ✅ Enabled |
| platform-layer | ✅ Enabled |
| testing-layer | ✅ Enabled |
| plan-layer | ✅ Enabled |

### Release Configuration

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Release Configuration
# ═══════════════════════════════════════════════════════════════════════════════
release:
  strategy: kmp-fastlane
  predefined_template: kmp-fastlane
  release_type: beta
  shared_keys: secrets/shared_keys.env  # TODO: add your credentials here
  platforms:
    android:
      enabled: true
      track: production
      secrets: secrets/playStorePublishServiceCredentialsFile.json  # TODO: add your credentials here
      fastlane_lane: deployToPlayStore
    ios_testflight:
      enabled: true
      secrets: secrets/AuthKey.p8  # TODO: add your credentials here
      fastlane_lane: beta
      distribute: testflight
    ios_appstore:
      enabled: false
      secrets: secrets/AuthKey.p8  # TODO: add your credentials here
      fastlane_lane: release
      distribute: appstore
```
