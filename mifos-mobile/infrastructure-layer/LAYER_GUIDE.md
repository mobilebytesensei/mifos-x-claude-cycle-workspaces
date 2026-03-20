# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/infrastructure-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-20"

# Infrastructure Layer Guide - mifos-mobile

> The glue between feature code and platform runtime.

---

## Purpose

The infrastructure layer provides the build system, dependency injection composition, navigation wiring, and shared application scaffolding that connects feature modules to platform entry points.

---

## Module Overview

| Module | Purpose | Project Path |
|--------|---------|--------------|
| `build-logic` | Convention plugins | `source/mifos-mobile/build-logic/` |
| `cmp-shared` | Root app module | `source/mifos-mobile/cmp-shared/` |
| `cmp-navigation` | Feature wiring | `source/mifos-mobile/cmp-navigation/` |
| Koin composition | DI graph | `cmp-navigation/.../di/KoinModules.kt` |

---

## Key Files Reference

> **Full templates**: `templates/instructions/infrastructure-layer/`

| Template | Purpose |
|----------|---------|
| BUILD_LOGIC_GUIDE.md | Convention plugins, module creation |
| CMP_SHARED_TEMPLATE.md | Root `App()` composable, `initKoin()` |
| CMP_NAVIGATION_TEMPLATE.md | `RootNavGraph`, route registration |
| KOIN_MODULES_TEMPLATE.md | DI module composition |
| SOURCE_SET_HIERARCHY.md | Source set organization |
| GRADLE_CONFIG_GUIDE.md | Version catalog, build configuration |

---

## Quick Tasks

### "I need to add a new feature"

1. Create feature module: `source/mifos-mobile/feature/{name}/`
2. Add route to `RootNavGraph` in `cmp-navigation`
3. Register `{Feature}Module` in `KoinModules.featureModule`

### "I need to add a new platform"

1. Add target in convention plugins (`build-logic/`)
2. Create entry point module (`cmp-{platform}/`)
3. Provide `actual` implementations for all `expect` declarations

### "I need to understand source sets"

Consult `SOURCE_SET_HIERARCHY.md` for the full hierarchy tree and placement rules.

---

## Relationship to Other Layers

| Layer | Infrastructure Provides | Infrastructure Consumes |
|-------|------------------------|------------------------|
| Feature | Navigation routes, DI wiring, build plugins | Feature modules, ViewModels |
| Platform | `initKoin()`, `App()` composable | Platform `actual` implementations |
| Client | Build plugins for network modules | Service/repository definitions |

---

## Project Paths

```
source/mifos-mobile/
├── build-logic/
│   └── convention/src/main/kotlin/org/convention/
│       ├── KmpLibraryConventionPlugin.kt
│       ├── KmpFeatureConventionPlugin.kt
│       └── HierarchyTemplate.kt
├── cmp-shared/src/commonMain/kotlin/.../
│   ├── App.kt
│   └── KoinExt.kt
├── cmp-navigation/src/commonMain/kotlin/.../
│   ├── RootNavGraph.kt
│   └── di/KoinModules.kt
├── cmp-android/     # Android entry point
├── cmp-ios/         # iOS entry point
├── cmp-desktop/     # Desktop entry point
└── cmp-web/         # Web entry point
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/implement [feature]` | Generates feature + wires infrastructure |
| `/gap-analysis` | Check overall project gaps |
