# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/PROJECT.md"
# last_modified: "2026-03-20"

# Project: mifos-mobile

**Created**: 2024 (Migrated to multi-project: 2025-01-06)
**Status**: Active (79% complete)

| Field | Value |
|-------|-------|
| Type | kmp |
| Subtype | kmp-app |

---

## Idea & Purpose

Self-service banking application for end-users to view and transact on their accounts, loans, and transfers through the MifosX platform.

**Type**: Self-Service Banking App
**Target Users**: Bank customers, microfinance clients

---

## Repository

| Setting | Value |
|---------|-------|
| Upstream | [openMF/mifos-mobile](https://github.com/openMF/mifos-mobile) |
| Origin (Fork) | [therajanmaurya/mifos-mobile](https://github.com/therajanmaurya/mifos-mobile) |
| Reference Template | [openMF/kmp-project-template](https://github.com/openMF/kmp-project-template) |

---

## Tech Stack

| Component | Choice |
|-----------|--------|
| Language | Kotlin |
| UI Framework | Compose Multiplatform |
| Architecture | MVI (Model-View-Intent) |
| Platforms | Android, iOS, Desktop, Web |

---

## Layers Configuration

### Design Layer (Enabled)

| Setting | Value |
|---------|-------|
| Enabled | Yes - Full (specs, mockups, tokens) |
| Design Tool | Figma / Google Stitch AI |
| Design System | Material Design 3 |

### Server Layer (Enabled)

| Setting | Value |
|---------|-------|
| Enabled | Yes |
| API Type | Apache Fineract (Self-Service) |
| Base URL | `https://[instance]/fineract-provider/api/v1/self/` |
| Auth Method | JWT (Basic Auth for login) |
| Documentation | OpenAPI / Swagger |

### Client Layer (Enabled)

| Setting | Value |
|---------|-------|
| Enabled | Yes - Full data layer |
| Network | Ktor + Ktorfit |
| Database | Room (KMP) |
| DI | Koin |

### Feature Layer (Enabled)

| Setting | Value |
|---------|-------|
| Enabled | Yes - Full UI layer |
| Module Structure | Multi-module (feature per module) |
| Navigation | Compose Navigation |

### Platform Layer (Enabled)

| Setting | Value |
|---------|-------|
| Enabled | Yes |
| Platforms | Android, iOS, Desktop, Web |

### Testing Layer (Enabled)

| Setting | Value |
|---------|-------|
| Enabled | Yes - Full testing infrastructure |
| Frameworks | JUnit, kotlin-test, Turbine, Compose UI Test, Roborazzi |

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

---

## Features (17)

| # | Feature | Design | Server | Client | Feature | Tests | Status |
|:-:|---------|:------:|:------:|:------:|:-------:|:-----:|:------:|
| 1 | auth | Spec | API | Service | Module | - | Done |
| 2 | home | Spec | API | Service | Module | - | Done |
| 3 | accounts | Spec | API | Service | Module | - | Done |
| 4 | savings-account | Spec | API | Service | Module | - | Done |
| 5 | loan-account | Spec | API | Service | Module | - | Done |
| 6 | share-account | Spec | API | Service | Module | - | Done |
| 7 | beneficiary | Spec | API | Service | Module | - | Done |
| 8 | transfer | Spec | API | Service | Module | - | Done |
| 9 | recent-transaction | Spec | API | Service | Module | - | Done |
| 10 | notification | Spec | API | Service | Module | - | Done |
| 11 | settings | Spec | - | - | Module | - | Done |
| 12 | passcode | Spec | - | - | Lib | - | Done |
| 13 | guarantor | Spec | API | Service | Module | - | Done |
| 14 | qr | Spec | - | - | Module | - | Done |
| 15 | location | Spec | - | - | Module | - | Done |
| 16 | client-charge | Spec | API | Service | Module | - | Done |
| 17 | dashboard | - | - | - | - | - | New |

---

## Current Focus

**v2.0 UI Redesign** - 2025 Fintech Patterns
- Modern UI components
- Improved UX flows
- Mockup generation for all features
- Testing layer implementation

---

## Quick Commands

```bash
/project-set mifos-mobile     # Set as active project
/session-start                # Start working
/gap-analysis                 # Check status
/design [feature]             # Design a feature
/implement [feature]          # Implement a feature
```

---

## Layer Paths

| Layer | Workspace Path |
|-------|----------------|
| Design | `workspaces/mifos-mobile/design-spec-layer/` |
| Server | `workspaces/mifos-mobile/server-layer/` |
| Client | `workspaces/mifos-mobile/client-layer/` |
| Feature | `workspaces/mifos-mobile/feature-layer/` |
| Platform | `workspaces/mifos-mobile/platform-layer/` |
| Testing | `workspaces/mifos-mobile/testing-layer/` |
