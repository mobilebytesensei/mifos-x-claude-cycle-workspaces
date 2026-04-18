# template_meta
# template_version: "2.86.5"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/PROJECT.md"
# last_modified: "2026-03-20"

# Project: mifos-x-field-officer-app

**Created**: 2026-03-04
**Project Type**: kmp (kmp-app)
**Status**: Active - Onboarding Complete

---

## Overview

Field officer mobile app for Mifos X - A KMP mobile application enabling field officers to manage clients, loans, collections, and centers in the field with offline support.

---

## Configuration

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Project Identity
# ═══════════════════════════════════════════════════════════════════════════════
project:
  name: mifos-x-field-officer-app
  workspace: mifos-x
  version: 0.1.0

# ═══════════════════════════════════════════════════════════════════════════════
# Project Type (What you're building)
# ═══════════════════════════════════════════════════════════════════════════════
project_type: kmp

project_subtype: kmp-app

# ═══════════════════════════════════════════════════════════════════════════════
# Deployment Targets (Where code runs)
# ═══════════════════════════════════════════════════════════════════════════════
targets:
  - android
  - ios
  - desktop
  - web-wasm

# ═══════════════════════════════════════════════════════════════════════════════
# Project URLs & Links
# ═══════════════════════════════════════════════════════════════════════════════
urls:
  # Repository
  github: "https://github.com/openMF/mifos-x-field-officer-app"

  # Backend
  server_base: "https://demo.mifos.io"
  api_docs: "https://demo.mifos.io/fineract-provider/api/docs"

  # Documentation
  documentation: "https://mifos.gitbook.io/docs/"
  wiki: "https://github.com/openMF/mifos-x-field-officer-app/wiki"

  # DevOps
  ci_cd: "https://github.com/openMF/mifos-x-field-officer-app/actions"
  dashboard: null

  # Design
  design: null

# ═══════════════════════════════════════════════════════════════════════════════
# Backend Configuration
# ═══════════════════════════════════════════════════════════════════════════════
backend:
  provider: fineract
  api_base: "https://demo.mifos.io/fineract-provider/api/v1"
  features:
    - authentication
    - clients
    - loans
    - savings
    - groups
    - centers
    - collections

# ═══════════════════════════════════════════════════════════════════════════════
# Technology Stack
# ═══════════════════════════════════════════════════════════════════════════════
stack:
  language: kotlin
  ui: compose
  state: mvi
  di: koin
  http: ktor

# ═══════════════════════════════════════════════════════════════════════════════
# Layers (Enabled/Disabled)
# ═══════════════════════════════════════════════════════════════════════════════
layers:
  design: enabled
  plan: enabled
  server: enabled
  client: enabled
  feature: enabled
  testing: enabled
  platform: enabled
  infrastructure: enabled

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

# ═══════════════════════════════════════════════════════════════════════════════
# Agent Configuration
# ═══════════════════════════════════════════════════════════════════════════════
agents:
  enabled: true
  auto_review: true
  auto_security: true
  auto_tests: true
  auto_fix_build: true
  block_on_security: true
  security_block_level: high
  review_threshold: 70
  coverage_threshold: 60
  verbose: false
  interactive: false

# ═══════════════════════════════════════════════════════════════════════════════
# Ticket Management Configuration
# ═══════════════════════════════════════════════════════════════════════════════
ticket_management:
  default_platform: github
  github:
    repo: "openMF/mifos-x-field-officer-app"
    labels:
      - "flow-generated"
      - "design"
  mapping:
    screen_to_story: true
    decision_to_task: true
    api_endpoint_to_task: true
  auto_update_on_implement: true

# ═══════════════════════════════════════════════════════════════════════════════
# User Flows (Penpot Integration)
# ═══════════════════════════════════════════════════════════════════════════════
flow:
  type: penpot
  fallback: headless
  penpot:
    project_id: "28716f1a-b249-8049-8007-aea28203c4a3"
    project_name: "mifos-x-field-officer"
    project_url: "https://design.penpot.app/view/28716f1a-b249-8049-8007-aea28203c4a3"
    flows_file_id: "28716f1a-b249-8049-8007-aea28203c4a3"
    created_at: "2026-03-08"
    created_by: "/design flow generate --from-features"
    pages:
      - id: "28716f1a-b249-8049-8007-aea28203c4a4"
        name: "Authentication Flow"
      - id: "2c915ee0-8071-8051-8007-aec00e2cc0c7"
        name: "Client Management Flow"
      - id: "2c915ee0-8071-8051-8007-aec00e2e732b"
        name: "Financial Operations Flow"
      - id: "2c915ee0-8071-8051-8007-aec00e2e96cd"
        name: "Field Operations Flow"
      - id: "2c915ee0-8071-8051-8007-aec00e2ef3c3"
        name: "Admin Utilities Flow"
      - id: "2c915ee0-8071-8051-8007-aec00e2f4f9a"
        name: "Data Table Flow"

# ═══════════════════════════════════════════════════════════════════════════════
# Feature Progress
# ═══════════════════════════════════════════════════════════════════════════════
features:
  total: 20
  done: 0
  spec_ready: 0
  planned: 20
```

---

## Layers

| Layer | Status | Index |
|-------|--------|-------|
| Design | Active | [FEATURES_INDEX](design-spec-layer/FEATURES_INDEX.md) |
| Plan | Active | [PLANS_INDEX](plan-layer/PLANS_INDEX.md) |
| Server | Active | [API_INDEX](server-layer/API_INDEX.md) |
| Client | Active | [SERVICES_INDEX](client-layer/SERVICES_INDEX.md) |
| Feature | Active | [MODULES_INDEX](feature-layer/MODULES_INDEX.md) |
| Testing | Active | [LAYER_STATUS](testing-layer/LAYER_STATUS.md) |
| Platform | Active | [LAYER_STATUS](platform-layer/LAYER_STATUS.md) |
| Infrastructure | Active | [LAYER_STATUS](infrastructure-layer/LAYER_STATUS.md) |

---

## Source Discovery Summary

| Category | Count |
|----------|-------|
| Feature Modules | 20 |
| UI Screens | 97 |
| ViewModels | 91 |
| API Services | 27 |
| Repositories | 64 |
| Platforms | 4 (Android, iOS, Desktop, Web) |

---

## Features Discovered

| # | Feature | Screens | VMs | Status |
|:-:|---------|:-------:|:---:|--------|
| 1 | about | 1 | 0 | Implemented |
| 2 | activate | 1 | 1 | Implemented |
| 3 | auth | 1 | 1 | Implemented |
| 4 | center | 5 | 5 | Implemented |
| 5 | checker-inbox-task | 2 | 2 | Implemented |
| 6 | client | 38 | 31 | Implemented |
| 7 | collectionSheet | 5 | 5 | Implemented |
| 8 | data-table | 4 | 4 | Implemented |
| 9 | document | 2 | 2 | Implemented |
| 10 | groups | 4 | 4 | Implemented |
| 11 | loan | 11 | 12 | Implemented |
| 12 | note | 2 | 2 | Implemented |
| 13 | offline | 5 | 6 | Implemented |
| 14 | path-tracking | 1 | 1 | Implemented |
| 15 | recurringDeposit | 1 | 1 | Implemented |
| 16 | report | 3 | 2 | Implemented |
| 17 | savings | 7 | 7 | Implemented |
| 18 | search | 1 | 1 | Implemented |
| 19 | search-record | 1 | 1 | Implemented |
| 20 | settings | 2 | 3 | Implemented |

---

## Quick Links

### Design
- [Features Index](design-spec-layer/FEATURES_INDEX.md)
- [User Flows](design-spec-layer/user-flows/USER_FLOWS_INDEX.md)

### Implementation
- [Services Index](client-layer/SERVICES_INDEX.md)
- [Modules Index](feature-layer/MODULES_INDEX.md)

### Server
- [API Index](server-layer/API_INDEX.md)

---

## Next Priority

1. **auth** - Authentication feature (login/logout)
2. **client** - Client management (largest feature module)
3. **loan** - Loan management
4. **savings** - Savings account management

---

## Tech Stack Summary

| Category | Technology |
|----------|------------|
| Project Type | kmp (kmp-app) |
| Targets | Android, iOS, Desktop, Web |
| Language | Kotlin |
| UI | Compose Multiplatform |
| State | MVI |
| DI | Koin |
| HTTP | Ktor Client |
| Backend | Fineract REST API |

---

## Repository

- **Source**: `source/mifos-x-field-officer-app/`
- **Origin**: https://github.com/therajanmaurya/mifos-x-field-officer-app
- **Upstream**: https://github.com/openMF/mifos-x-field-officer-app
