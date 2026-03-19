# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/platform-layer/expect-actual/README.md"
# last_modified: "2026-03-19"

# Expect/Actual Templates Index - mobile-wallet

> Quick reference for platform-specific `expect`/`actual` declarations used in this project.

---

## Overview

The `expect`/`actual` mechanism lets you declare a common API in `commonMain` and provide
platform-specific implementations in each target source set. Templates for the most common
declarations are maintained in the framework.

---

## Template Catalog

> **Full catalog with trigger keywords and auto-detection**: `templates/instructions/platform-layer/EXPECT_ACTUAL_CATALOG.md`

### Core Templates (Complete)

| ID | Category | Template | Module |
|----|----------|----------|--------|
| EA-001 | HTTP Client | `HTTP_CLIENT.md` | `core-base/network` |
| EA-002 | Database Driver | `DATABASE_DRIVER.md` | `core/database` |
| EA-003 | DI Platform Module | `PLATFORM_MODULE.md` | `core/data` |
| EA-004 | Dispatchers | `DISPATCHERS.md` | `core-base/common` |
| EA-005 | Theme / Color Scheme | `THEME_COLOR_SCHEME.md` | `core/designsystem` |
| EA-006 | Share Utils | `SHARE_UTILS.md` | `core-base/ui` |
| EA-007 | File Utils | `FILE_UTILS.md` | `core/common` |
| EA-008 | Clipboard | `CLIPBOARD.md` | `core-base/ui` |
| EA-009 | Platform Detection | `PLATFORM_DETECTION.md` | `feature/settings` |
| EA-010 | Image Loader | `IMAGE_LOADER.md` | `core/ui` |

### Template Location

All templates live in: `templates/instructions/platform-layer/expect-actual/`

---

## Owner Model

| Owner | Meaning | Action During `/implement` |
|-------|---------|---------------------------|
| Template (`core-base/`) | Provided by the KMP project template | Verify exists, do NOT regenerate |
| User (`core/`, `feature/`) | Project-specific, must be created per project | Generate from template if missing |

---

## Source Set Placement

| Declaration | Source Set | Path Pattern |
|-------------|-----------|--------------|
| `expect` | `commonMain` | `{module}/src/commonMain/kotlin/{package}/` |
| `actual` (Android) | `androidMain` | `{module}/src/androidMain/kotlin/{package}/` |
| `actual` (iOS) | `nativeMain` | `{module}/src/nativeMain/kotlin/{package}/` |
| `actual` (Desktop) | `desktopMain` | `{module}/src/desktopMain/kotlin/{package}/` |
| `actual` (Web JS) | `jsMain` | `{module}/src/jsMain/kotlin/{package}/` |
| `actual` (Web Wasm) | `wasmJsMain` | `{module}/src/wasmJsMain/kotlin/{package}/` |

---

## Auto-Detection

During `/implement`, the framework automatically:

1. Scans `SPEC.md` for trigger keywords (e.g., "database", "HTTP", "share")
2. Matches against the catalog
3. Checks if the expect/actual exists in the project source
4. Generates missing declarations from the template
5. Wires DI bindings into the appropriate Koin module

No manual action is required for standard expect/actual declarations.

---

## Project Status

| ID | Category | Generated | Verified |
|----|----------|:---------:|:--------:|
| EA-001 | HTTP Client | -- | -- |
| EA-002 | Database Driver | -- | -- |
| EA-003 | DI Platform Module | -- | -- |
| EA-004 | Dispatchers | -- | -- |
| EA-005 | Theme / Color Scheme | -- | -- |

*Update this table as expect/actual declarations are generated for the project.*
