# Implementation Plan: kmp-product-flavors integration

## Metadata

| Field | Value |
|---|---|
| Plan ID | `PLAN-kmp-product-flavors-260510-181018` |
| Generated | 2026-05-10 18:10:18 |
| Project | `mifos-x/kmp-project-template` (kmp/template) |
| Status | Ready (rev 2 — pinned to v1.1.0 after upstream release on 2026-05-10) |
| Source gap report | `/gap-analysis-project` 2026-05-10 |
| Library | `io.github.mobilebytelabs.kmpflavors:flavor-plugin:1.1.0` (Maven Central) |
| Plugin id | `io.github.mobilebytelabs.kmp-product-flavors` (Gradle Plugin Portal) |
| Pinned version | `1.1.0` (released 2026-05-10) |
| Reference doc | https://github.com/MobileByteLabs/kmp-product-flavors/blob/development/docs/KMP_PROJECT_TEMPLATE_INTEGRATION.md |
| Upstream changelog | https://github.com/MobileByteLabs/kmp-product-flavors/releases/tag/v1.1.0 |

---

## Scope

Replace the existing Android-only `AndroidApplicationFlavorsConventionPlugin` with the KMP-aware `kmp-product-flavors` library at **v1.1.0**. Introduce three flavor dimensions (`tier` × `model` × `environment`), use the plugin's **native `FlavorConfig` codegen** (no separate BuildKonfig dependency needed — it's built in), expose constants via an `AppVariant` wrapper in `cmp-shared/commonMain`, refactor `AuthenticatedNavigation.kt` for conditional routes, and design a downstream extension hook so consumer projects (clientA, clientB, …) can add flavors **on top of** the synced `demo/prod` baseline without `sync-dirs.sh` overwriting their work.

### Why v1.1.0 specifically

`v1.1.0` shipped on 2026-05-10 and is the **first version that fully supports this integration**. Pinned features used:

| Capability | Plugin version | Used here |
|---|---|---|
| Multi-dimensional flavors + native `FlavorConfig` codegen | v1.0.x | ✅ |
| `bridgeAgpProductFlavors` / `bridgeAgpBuildTypes` (AGP-application bridge) | **v1.1.0** | ✅ replaces hand-written `android { productFlavors {} }` in `cmp-android` |
| Per-flavor test source sets | **v1.1.0** | ✅ `commonDemoTest`, `iosDemoTest`, etc. |
| `matchingFallbacks(...)` AGP propagation | **v1.1.0** | ✅ for cross-module dep resolution |
| `kmpFlavorInit` per-source-set READMEs | **v1.1.0** | ✅ documents flavor source sets in repo |
| iOS SPM `Package.swift` generator | **v1.1.0** | ⚠️ deferred — adopt only if iOS framework distribution is needed; CocoaPods is unsupported |

**Out of scope:**
- Adding new feature modules.
- Migrating Firebase / Crashlytics per-flavor configs (tracked separately).
- Per-flavor `applicationId` rebrand (handled by existing `customizer.sh`).
- **AGP `com.android.library` bridge** — plugin v1.1.0 supports `com.android.application` only; library bridge lands in upstream **v1.2.0** (Phase J of `mbs/kmp-product-flavors/plan-layer/plans/PLAN-gaps-fix-260510-191003.md`). If any KMP-library module here needs propagated flavors, wait for v1.2.0 or hand-write that module's `android { productFlavors {} }` until then.
- **Android resources / signing per flavor** — also v1.2.0 (Phase K).
- **Multi-module variant matching across mismatched dimensions** — v1.2.0 (Phase M). For now, declare consistent dimensions across modules or use `matchingFallbacks(...)`.

---

## Open Questions (resolve before Phase A)

1. **Variant matrix size.** `tier(2) × model(2) × environment(3) = 12` flavor combos × `debug+release = 24`. Confirm whether `environment` should be a flavor dimension (compile-time `BASE_URL`) or runtime (`local.properties` / `BuildConfig` override). **Recommendation:** keep as flavor dimension since the user's Q3 spec explicitly asks for `BuildKonfig BASE_URL` per environment — but be aware of CI lane explosion.
2. **Variant filter.** Should we use AGP `variantFilter` to exclude unreasonable combos (e.g., `demo + prod-environment`)? **Recommendation:** yes — exclude `demo+prod`, `prod+dev`.
3. **Consumer extension surface.** Two options for clientA/clientB extension:
   - (a) Non-synced file `build-logic/convention/src/main/kotlin/local/Flavors.local.kt` excluded by `sync-dirs.sh`.
   - (b) Read flavor list from a non-synced YAML at `config/flavors.local.yaml`.
   **Recommendation:** option (a) — keeps everything in Kotlin, IDE-friendly. Add `EXCLUSIONS["build-logic"]="convention/src/main/kotlin/local:dir"` to `sync-dirs.sh`.

---

## Layers Touched

| Layer | Change kind |
|---|---|
| Idea | new SPEC entry for flavor architecture (RULE-GAP-IDEA-FIRST-001) |
| Plan | this file |
| Server | none |
| Client | `cmp-shared/commonMain` — `AppVariant` wrapper |
| Feature | `cmp-navigation` — conditional `AuthenticatedNavigation` |
| Infrastructure | `build-logic` (rewrite plugin), `gradle/libs.versions.toml`, `sync-dirs.sh`, `.github/workflows/sync-dirs.yaml` |
| Platform | `cmp-android/build.gradle.kts`, all KMP module `build.gradle.kts` files |
| Testing | flavor-aware test source sets |

---

## Phases (ordered, sequential)

### Phase A — Idea + dependencies (foundation)

| # | Task | File(s) |
|---|---|---|
| A1 | `/idea add` → SPEC entry "Multi-dimension flavor architecture" with `tier/model/environment` matrix and conditional-navigation requirement | `idea-layer/exports/flavors/SPEC.md` |
| A2 | Add catalog entries (no BuildKonfig — `FlavorConfig` codegen is built into the plugin):<br>`[versions] kmpProductFlavors = "1.1.0"`<br>`[plugins] kmp-product-flavors = { id = "io.github.mobilebytelabs.kmp-product-flavors", version.ref = "kmpProductFlavors" }`<br>`[libraries] kmp-product-flavors-plugin = { group = "io.github.mobilebytelabs.kmpflavors", name = "flavor-plugin", version.ref = "kmpProductFlavors" }` | `gradle/libs.versions.toml` |
| A3 | Add plugin alias in root build | `build.gradle.kts` (root) |
| A4 | Document flavor architecture, including the `bridgeAgpProductFlavors` / `bridgeAgpBuildTypes` decision and `cmp-android/build.gradle.kts:149` `prodReleaseRuntimeClasspath` configuration update path | `docs/FLAVORS.md` (new) |

**Exit criteria:** `./gradlew help` resolves `id("io.github.mobilebytelabs.kmp-product-flavors") version "1.1.0"` without applying it anywhere.

### Phase B — Convention plugin rewrite

| # | Task | File(s) |
|---|---|---|
| B1 | Replace `AndroidApplicationFlavorsConventionPlugin.kt` with `KmpProductFlavorsConventionPlugin` using `kmpFlavors { … }` DSL — three dimensions + per-flavor `buildConfigField("String", "BASE_URL", "...")` for environment, plus `bridgeAgpProductFlavors.set(true)` and `bridgeAgpBuildTypes.set(true)` so AGP `productFlavors` / `buildTypes` are populated automatically (no parallel `android { productFlavors {} }` block) | `build-logic/convention/src/main/kotlin/KmpProductFlavorsConventionPlugin.kt` |
| B2 | Delete legacy `org/convention/AppFlavor.kt` (enum-based) | — |
| B3 | Update plugin registration block | `build-logic/convention/build.gradle.kts:64` |
| B4 | Add hook for non-synced `local/Flavors.local.kt` consumer extension (apply if file exists) | new `local/.gitkeep` + plugin loader |
| B5 | Add `variantFilter` to exclude impossible combos (e.g. `demo + prod-environment`, `prod + dev-environment`) per `docs/VARIANT_FILTERS.md` recipes | same plugin |
| B6 | (optional) Use `matchingFallbacks(...)` on flavors that downstream library modules don't declare — `bridgeAgpProductFlavors` propagates these into AGP automatically (v1.1.0 G10) | same plugin |

**Exit criteria:** `./gradlew :cmp-android:tasks` lists `assembleDemoBasicDevDebug` (and matching variants).

### Phase C — KMP source-set scaffolding

| # | Task | Modules |
|---|---|---|
| C1 | Create `commonDemoMain/`, `commonProdMain/`, `commonBasicMain/`, `commonAdvancedMain/` empty placeholders | `cmp-shared`, `cmp-navigation`, every `feature/*/`, `core/*/` |
| C2 | Verify each module's `build.gradle.kts` declares the source sets (KMP wiring) | per-module `build.gradle.kts` |
| C3 | Apply `KmpProductFlavorsConventionPlugin` where needed | per-module `build.gradle.kts` |

**Exit criteria:** `./gradlew :cmp-shared:compileCommonMainKotlinMetadata` succeeds for all variant combinations.

### Phase D — Typed `AppVariant` wrapper

| # | Task | File(s) |
|---|---|---|
| D1 | Create `AppVariant` object in commonMain wrapping `FlavorConfig.IS_DEMO`, `IS_PROD`, `IS_BASIC`, `IS_ADVANCED`, `BASE_URL` | `cmp-shared/src/commonMain/kotlin/cmp/shared/variant/AppVariant.kt` |
| D2 | Unit tests asserting wrapper resolves correctly per source set | `cmp-shared/src/commonTest/...` |

**Exit criteria:** `AppVariant.IS_ADVANCED` compiles in commonMain; `:cmp-shared:allTests` green.

### Phase E — Conditional navigation refactor

| # | Task | File(s) |
|---|---|---|
| E1 | Refactor `AuthenticatedNavigation.kt` — gate `cryptoGraph`, `currencyRatesGraph`, `emiCalculatorDestination` behind `AppVariant.IS_ADVANCED`; route to `UpgradeScreen` from locked targets when `IS_DEMO` | `cmp-navigation/src/commonMain/kotlin/cmp/navigation/authenticated/AuthenticatedNavigation.kt` |
| E2 | Create stub `UpgradeScreen` (commonMain) | `cmp-navigation/.../upgrade/UpgradeScreen.kt` (new) |
| E3 | Drawer / bottom-bar item filter using `AppVariant` | wherever drawer is built (locate during impl) |
| E4 | Use `expect/actual` in commonBasic/commonAdvanced for divergent graphs (only if drawer/bar diverges materially — defer if simple branching suffices) | optional |

**Exit criteria:** `:cmp-android:assembleDemoBasicDevDebug` builds; `:cmp-android:assembleProdAdvancedProdRelease` builds; demo APK does not contain Premium classes (verify via APK inspection).

### Phase F — sync-dirs + CI

| # | Task | File(s) |
|---|---|---|
| F1 | Add `EXCLUSIONS["build-logic"]="convention/src/main/kotlin/local:dir"` so consumer-local flavors survive sync | `sync-dirs.sh` |
| F2 | Update GH workflow to mirror exclusion | `.github/workflows/sync-dirs.yaml` |
| F3 | Update fastlane lanes for new variant names | `fastlane/Fastfile`, `fastlane-config/` |
| F4 | Update `.run/` IDE run configs | `.run/*.xml` |
| F5 | Update CI workflow matrix (or pick representative subset) | `.github/workflows/build.yml` (or equivalent) |

**Exit criteria:** dry-run `./sync-dirs.sh --dry-run` from a synthetic consumer shows `convention/src/main/kotlin/local/` is preserved.

### Phase G — Verification + commit

| # | Task |
|---|---|
| G1 | `/verify` against new SPEC |
| G2 | `:cmp-android:assemble` for at least 4 representative variants (demo+basic+dev+debug, demo+basic+staging+release, prod+advanced+prod+release, prod+basic+dev+debug) |
| G3 | iOS / desktop / web smoke build |
| G4 | One commit at end of plan (per stored feedback) — branch already feature-scoped |

---

## Cross-Cutting Dependencies

```
Phase A ──▶ Phase B ──▶ Phase C ──▶ Phase D ──▶ Phase E
                    │                       │
                    └──▶ Phase F (parallel-safe after B)
                                            │
                                            ▼
                                          Phase G
```

Phase F can begin once Phase B is complete; everything else is strictly serial.

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| 12-variant explosion blows up CI duration | `variantFilter` (Phase B5) + CI matrix subset (Phase F5) |
| `sync-dirs.sh` regressions wipe consumer flavors | Add unit-style test: synthetic consumer with `local/Flavors.local.kt`, run `--dry-run`, assert preservation (Phase F) |
| `applicationIdSuffix=".demo"` regression | Phase B explicitly carries this over per-flavor in DSL; Phase G verifies in installed APK metadata |
| iOS / desktop / web builds break from new common source sets | Phase C creates empty placeholders; Phase G smoke-builds all targets |
| ~~Library is pre-1.0 / API churn~~ | ✅ resolved — pinned to **`v1.1.0`** (released 2026-05-10, Maven Central + Plugin Portal). API surface stable. |
| Plugin scope: v1.1.0 supports `com.android.application` only | KMP-library bridge is upstream **Phase J / v1.2.0**. If `cmp-shared` / `core/*` need propagated flavors, hand-write `productFlavors {}` for those modules until v1.2.0 ships, or treat them as flavor-agnostic (preferred — they consume `FlavorConfig` constants from `commonMain`). |
| Existing `cmp-android/src/{prod,demoRelease,prodRelease}` orphaned | Phase E3 audits and migrates content into new source-set layout |
| Downstream `cmp-android/build.gradle.kts:149` `prodReleaseRuntimeClasspath` string ref breaks | Phase E updates to new variant name; if many such refs exist, introduce a helper |

---

## Effort Estimate

| Phase | Effort |
|---|---|
| A | S (2–3h) |
| B | M (4–6h) |
| C | M (4–6h, mechanical but spread across many modules) |
| D | S (1–2h) |
| E | M (3–5h, navigation refactor + Upgrade screen) |
| F | S (2–3h) |
| G | S (1–2h) |
| **Total** | **~17–27h** |

---

## Execution Log

(updated by `/gap-implement-project plan PLAN-kmp-product-flavors-260510-181018`)

| Phase | Status | Started | Finished | Notes |
|---|---|---|---|---|
| A | Pending | — | — | — |
| B | Pending | — | — | — |
| C | Pending | — | — | — |
| D | Pending | — | — | — |
| E | Pending | — | — | — |
| F | Pending | — | — | — |
| G | Pending | — | — | — |

---

## What's Next

1. **Library v1.1.0 is published** (Maven Central + Gradle Plugin Portal as of 2026-05-10) — no upstream blockers remain for Phases A–G. Verify resolution: `./gradlew help` after Phase A2 should show no errors fetching `kmp-product-flavors:1.1.0`.
2. **Resolve open questions 1–3** above (variant matrix size, variantFilter exclusions, extension surface).
3. **Switch session binding** to `mifos-x/kmp-project-template` if not already bound: `/context-start mifos-x-kmp-project-template`.
4. Run: `/gap-implement-project plan PLAN-kmp-product-flavors-260510-181018` — executes Phases A → G sequentially with one commit at the end.
5. **For modules outside `cmp-android`** (KMP libraries: `cmp-shared`, `cmp-navigation`, `core/*`, `feature/*`): treat them as flavor-agnostic in v1.1.0 — they consume `FlavorConfig` constants from `commonMain` but don't declare AGP product flavors of their own. The library-side AGP bridge lands in upstream **v1.2.0**; revisit those modules then if you need divergent variants per library.

## Upstream changelog reference

- v1.1.0 release notes: https://github.com/MobileByteLabs/kmp-product-flavors/releases/tag/v1.1.0
- v1.2.0 plan (universal adoption — AGP-library bridge, Android resources/signing, library publishing, multi-module matching, iOS resources): `mbs/kmp-product-flavors/plan-layer/plans/PLAN-gaps-fix-260510-191003.md` Phases J–R
