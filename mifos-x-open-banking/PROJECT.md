# mifos-x-open-banking

> Production-ready Kotlin Multiplatform starter from the Mifos Initiative — Android, iOS, Desktop, Web, all from one codebase.

| Attribute | Value |
|-----------|-------|
| **Slug** | `mifos-x-open-banking` |
| **Workspace** | `mifos-x` |
| **Type** | KMP (Compose Multiplatform) |
| **Platforms** | Android · iOS · Desktop · Web |
| **Architecture** | Stream-First (BaseViewModel + ScreenDataStream + Store5) · Koin DI · Ktor/Ktorfit · Room KMP |
| **Backend** | Firebase (Crashlytics + Performance) |
| **Status** | `initialized` — adopted via `/project-import` on 2026-05-20 |
| **Source** | [github.com/openMF/mifos-x-open-banking](https://github.com/openMF/mifos-x-open-banking) |
| **Fork** | [TheKalpeshPawar/mifos-x-open-banking](https://github.com/TheKalpeshPawar/mifos-x-open-banking) (`dev` branch) |
| **Local clone** | `workspaces/mifos-x/mifos-x-open-banking/source/mifos-x-open-banking/` → symlink to `/home/kalpesh/OpenSource/Mifos/mifos-x-open-banking/` (full git history, user-managed) |
| **Current branch** | `feat/sync-workspace-with-template-post-sync` (feature branch; upstream default is `dev`) |

## Module Map

```
cmp-android    cmp-desktop    cmp-ios    cmp-web       ← platform entry points
        ╲          │           │         ╱
              cmp-shared · cmp-navigation                ← composition root
                        │
        ┌──────────────┼──────────────┐
   core/*         core-base/*      feature/*
   (data, db,    (analytics,    (home, profile,
    domain,       common,        settings)
    network,…)    network,…)
                                 [crypto, currency-rates,
                                  emi-calculator scheduled
                                  for removal — template residue]
```

## Layer Status

Empty-slate scaffold (post-template-sync 2026-05-22). Architecture + brand are set; product feature scope is undefined. See `idea-layer/LAYER_STATUS.md` for per-layer detail.

## Next Steps

1. **Remove template residue from source**: `feature/crypto`, `feature/currency-rates`, `feature/emi-calculator` — drop from `settings.gradle.kts` and delete directories.
2. **Define product scope**: run `/idea-plan` to draft vision + features.
3. **Per-feature work**: `/idea add` for each declared feature, then `/idea-enrich` → `/idea export` → `/kmp-implement`.

## Configuration

Machine-readable: `PROJECT_CONFIG.yaml`. Edit via `/project-add --verify` or directly.
