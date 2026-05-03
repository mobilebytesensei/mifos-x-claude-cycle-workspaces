# PLAN: Room 2.8.4 → Room 3.0 Migration (In-Place, Clean Architecture)

**ID**: PLAN-room3-migration-260429
**Created**: 2026-04-29
**Updated**: 2026-04-30 (v6 — Kotlin 2.3.20 + Compose 1.10.3 + KSP2 version alignment)
**Status**: In Progress
**Priority**: P1
**Project**: mifos-x/kmp-project-template
**Scope**: core-base/database + core/database + build-logic + version catalog + consumer projects (via sync)
**Goal**: Full KMP platform support (Android, iOS, Desktop, JS, WasmJS) via Room 3.0 with clean architecture

### Critical Discovery (v6): Kotlin Version Alignment Required

Room 3.0-alpha03 klibs were compiled with `compiler_version=2.3.20` (confirmed from klib manifest). Kotlin Native and JS klibs require **exact compiler version match**. The project's Kotlin 2.2.21 cannot consume Room 3 klibs for iOS/Native/JS/WasmJS (JVM/Desktop works because JARs have backward compatibility).

**Required version upgrades**:

| Dependency | Before | After | Why |
|-----------|--------|-------|-----|
| Kotlin | 2.2.21 | **2.3.20** | Room 3 klibs compiled with 2.3.20 |
| KSP | 2.2.21-2.0.4 | **2.3.6** | KSP2 (decoupled from Kotlin version) |
| Compose Multiplatform | 1.9.3 | **1.10.3** | Matching version for Kotlin 2.3.20 |

---

## Context

Room 2.8.4 supports Android, iOS, and Desktop but leaves JS/WasmJS with empty stub modules. Room 3.0 (March 2026) adds native JS/WasmJS support and eliminates the need for most platform-specific database code.

### Sync Mechanism (Critical Discovery)

Consumer projects (`mifos-pay`, `mifos-mobile`, `mifos-x-field-officer-app`) do NOT depend on this template's source code directly. Instead:

1. **`sync-dirs.sh`** + **`.github/workflows/sync-dirs.yaml`** automatically copy `core-base/`, `build-logic/`, and other shared directories from this upstream template to each consumer
2. Sync runs on **weekly cron** (Monday midnight) + **manual dispatch**
3. Synced directories: `core-base/`, `build-logic/`, `cmp-desktop/`, `cmp-web/`, `cmp-shared/`, `fastlane/`, `scripts/`, `config/`, `.github/`, `.run/`
4. Consumer projects customize only their own `core/database/` (entities, DAOs, DI)

**Implication**: We migrate **in-place** in the template. Consumer projects receive changes automatically via the next sync. No parallel module needed.

---

## Architecture Decision (Revised v3)

### Decision 1: In-place migration (not parallel module)

**Rationale**:
- `sync-dirs.sh` propagates `core-base/` and `build-logic/` changes automatically
- Parallel module adds unnecessary complexity (consumers would need to switch module references manually)
- In-place is cleaner — one atomic migration in the template, consumers sync and adapt their `core/database/` layer

### Decision 2: REMOVE `core-base/database` abstraction layer — use Room 3 directly

**Why the abstraction existed (Room 2.8.4)**:
- Room 2 did NOT support JS/WasmJS at all
- To use Room annotations in `commonMain`, we needed `@OptionalExpectation expect annotation class` declarations
- A `nonJsCommonMain` intermediate source set provided `actual typealias` mappings to real `androidx.room.*`
- JS/WasmJS needed dummy stub `actual annotation class` implementations (just to compile)
- **Total: ~1,100 lines across 4 files just to re-export Room annotations**

**Why the abstraction is NOW dead weight (Room 3.0)**:
- Room 3 annotations (`@Dao`, `@Entity`, `@Query`, etc.) work directly in `commonMain` on ALL platforms
- No `@OptionalExpectation` needed — Room 3 ships multiplatform artifacts
- No intermediate source set needed — `commonMain` is the true common
- No dummy stubs needed — JS/WasmJS are first-class targets
- The "stable import path" argument is invalid — consumers already write Room-specific SQL in `@Query`; they ARE coupled to Room regardless of import path
- Room annotation APIs haven't changed since Room 1.0 — a typealias shim adds zero future-proofing value

**What this means for consumer projects**:
- Consumer DAOs change: `import template.core.base.database.Dao` → `import androidx.room3.Dao`
- Consumer entities change: `import template.core.base.database.Entity` → `import androidx.room3.Entity`
- **This is a find-and-replace operation** — no logic changes, no behavior changes
- Constants (`OnConflictStrategy.REPLACE`) → use `androidx.room3.OnConflictStrategy.REPLACE` directly

**Impact assessment**:

| What | Before (Room 2) | After (Room 3) |
|------|-----------------|----------------|
| `core-base/database/Room.kt` | 841 lines (expect annotations) | **DELETE** |
| `core-base/database/Room.nonJsCommon.kt` | 177 lines (actual typealiases) | **DELETE** |
| `core-base/database/Room.js.kt` | 39 lines (dummy stubs) | **DELETE** |
| `core-base/database/Room.wasmJs.kt` | 39 lines (dummy stubs) | **DELETE** |
| `nonJsCommonMain` source set | Exists (hack) | **REMOVE** from build.gradle.kts |
| Consumer imports | `template.core.base.database.*` | `androidx.room3.*` |
| AppDatabaseFactory files | KEEP (platform-specific DB paths) | KEEP (simplified) |
| Total lines removed | — | **~1,100 lines** |

### Key Architectural Simplification (combined):
- **DELETE entire `core-base/database` annotation abstraction** (~1,100 lines)
- `@Database` class moves to `commonMain` (eliminate 3 platform actuals)
- Context-free database builders (no Android Context needed)
- Only `SQLiteDriver` + file path remains platform-specific (via AppDatabaseFactory)
- Remove `@ConstructedBy` / `RoomDatabaseConstructor` pattern (simplified in Room 3)
- Remove `findAndInstantiateDatabaseImpl` / `findDatabaseConstructorAndInitDatabaseImpl` calls
- **~80% reduction in platform-specific database code** (up from 60% in v2)

---

## Gaps Found in Original Plan (v1)

| # | Gap | Severity | Fix in v2 |
|:-:|-----|:--------:|-----------|
| G1 | **Wrong strategy**: Parallel module approach ignores sync-dirs mechanism | HIGH | Changed to in-place migration |
| G2 | **Phase 4 unnecessary**: Consumer projects don't need manual migration — sync-dirs handles `core-base/` + `build-logic/` | HIGH | Replaced with sync trigger + consumer `core/database/` migration guide |
| G3 | **Missing**: `nonJsCommonMain` source set removal not planned | MED | Added task to remove this intermediate source set |
| G4 | **Missing**: `build-logic/convention/build.gradle.kts` line 32 `compileOnly(libs.androidx.room.gradle.plugin)` needs updating | MED | Added task |
| G5 | **Missing**: ProGuard rules in `cmp-android/proguard-rules.pro` + `cmp-desktop/compose-desktop.pro` reference `androidx.room.RoomDatabase` | MED | Added task to update keep rules |
| G6 | **Missing**: Schema JSON at `core/database/schemas/org.mifos.core.database.AppDatabase/1.json` — package path changes | MED | Added schema migration task |
| G7 | **Missing**: `room-ktx` artifact removed in Room 3 (merged into runtime) — convention plugin adds it | LOW | Remove ktx dependency |
| G8 | **Missing**: `Room.kt` in core-base has `@ConstructedBy` and `@RoomDatabaseConstructor` expect declarations — these are unnecessary in Room 3 | LOW | Remove from annotations |
| G9 | **Missing**: `jsMain/Room.js.kt` and `wasmJsMain/Room.wasmJs.kt` have dummy implementations — need real ones or removal | MED | Remove entirely (Room 3 annotations work on all platforms) |
| G10 | **Missing**: Convention plugin `room.generateKotlin=true` KSP arg — Room 3 is Kotlin-only, arg doesn't exist | LOW | Remove KSP arg |
| G11 | **Missing**: `settings.gradle.kts` may need update if module paths change | LOW | Added verification task |
| G12 | **v2 assumed typealiases stay** — `SampleEntity.kt` imports `template.core.base.database.Entity`. v3 decision: abstraction removed, imports change to `androidx.room3.Entity` | MED | Consumer import find-and-replace added to Phase 3 + Phase 4 checklist |
| G13 | **Missing**: Web platform needs `sqlite-wasm` worker JS file bundled | HIGH | Added WebWorker setup task |
| G14 | **Missing**: `cmp-web/` module Webpack/resource config for SQLite WASM worker | MED | Added web build config task |
| G15 | **Missing**: Android `DatabaseModule.android.kt` uses `androidApplication()` Koin — not available in commonMain | LOW | Keep Android DI module for Koin context, simplify to driver-only |
| G16 | **Missing**: Test modules need JS/WasmJS variants | MED | Added test module tasks |
| G17 | **Missing**: `core.common` module's `AppDispatchers` used in nativeMain DI — verify it works on JS/WasmJS | LOW | Added verification |
| G18 | **Missing**: Consumer project `core/database/` has MORE entities/DAOs than template — migration guide needed | HIGH | Added consumer migration guide section |
| G19 | **Package name in schema**: Room 3 uses `androidx.room3` package — schema export path changes from `org.mifos.core.database.AppDatabase` | MED | Verify schema backward compat |
| G20 | **Missing**: `@Database` annotation parameter changes — Room 3 may have different `autoMigrations` syntax | LOW | Verify annotation compat |
| G21 | **v2 kept typealiases** — plan v2 proposed shrinking Room.kt from 841→50 lines (typealiases). v3 analysis shows even typealiases add zero value with Room 3 full KMP support | MED | DELETE Room.kt entirely; consumer imports change via find-and-replace |

### Gaps Found in v4 Audit (G22-G41)

| # | Gap | Severity | Fix in v4 |
|:-:|-----|:--------:|-----------|
| G22 | **`nonJsCommonMain` is framework-wide** — defined in `HierarchyTemplate.kt:89`. `core-base/analytics` also uses it. Can't remove hierarchy group. | MED | Remove `nonJsCommonMain.dependencies` from `core-base/database/build.gradle.kts` only. Keep hierarchy group in HierarchyTemplate (analytics needs it). |
| G23 | **Redundant Room deps in `core-base/database/build.gradle.kts`** — `room-runtime` in 4 source sets (androidMain, desktopMain, nativeMain, nonJsCommonMain). Room 3 works in commonMain. | MED | Replace 4 per-platform deps with single `commonMain.dependencies { implementation(libs.androidx.room.runtime) }` |
| G24 | **`DatabaseModule` is DEAD CODE** — never wired into `KoinModules.allModules` in `cmp-navigation/`. The entire `core/database` module is unused at runtime. | HIGH | Add task: wire `DatabaseModule` into `KoinModules.allModules` in Phase 3 |
| G25 | **`cmp-web` has no `core:database` dependency** — Even after adding web DB support, the web app can't use it. | HIGH | Add task in Phase 5: add `implementation(projects.core.database)` to `cmp-web/build.gradle.kts` |
| G26 | **`@Suppress("NO_ACTUAL_FOR_EXPECT")` on `expect abstract class AppDatabase`** — must be removed when AppDatabase moves to commonMain | LOW | Covered by Task 3.2 — made explicit |
| G27 | **`expect object AppDatabaseConstructor : RoomDatabaseConstructor<AppDatabase>`** in nativeMain — has NO actual (generated by KSP). Must be explicitly deleted with `AppDatabase.native.kt`. | MED | Made explicit in Task 3.5 |
| G28 | **Dispatcher inconsistency** — Android/Desktop production use `Dispatchers.IO` directly; Native uses Koin `AppDispatchers.IO`. All tests use `AppDispatchers.IO`. | MED | Standardize: use `Dispatchers.IO` in all production DI, `AppDispatchers.IO` in tests. Added to Task 3.9-3.12. |
| G29 | **`factory` parameter in AppDatabaseFactory** — Desktop/Native factories accept `factory: () -> T` default param calling `findAndInstantiateDatabaseImpl`. Param becomes useless with Room 3. | MED | Remove `factory` parameter entirely. Room 3 handles instantiation internally. Added to Tasks 2.6-2.8. |
| G30 | **Redundant `room-runtime` in `core/database/build.gradle.kts`** — Convention plugin already adds `room-runtime`. Plus `core-base/database` is `api()` dep which also brings it. | MED | Remove explicit `room-runtime` from `core/database/build.gradle.kts`. Convention plugin handles it. |
| G31 | **`sqlite-bundled` in wrong module** — Currently in `core/database` nativeMain+desktopMain. But `BundledSQLiteDriver` is used in AppDatabaseFactory (in `core-base/database`). | MED | Move `sqlite-bundled` to `core-base/database/build.gradle.kts` (desktopMain+nativeMain). Remove from `core/database`. |
| G32 | **`customizer.sh:358` references `nonJsCommonMain`** — Lists source sets for template customization. | LOW | No action — `nonJsCommonMain` stays in hierarchy (analytics uses it). Informational only. |
| G33 | **`val desktopMain by getting`** in `core/database/build.gradle.kts:23` — Gradle anti-pattern. | LOW | Remove — use `desktopMain.dependencies { }` directly. |
| G34 | **`room-ktx` added by convention plugin (line 28)** — Plan says remove but doesn't specify WHERE. It's in `KMPRoomConventionPlugin.kt` line 28 AND `libs.versions.toml` line 161. | MED | Remove BOTH: line 28 of convention plugin AND `androidx-room-ktx` entry from version catalog. |
| G35 | **Unused `import org.jetbrains.compose.compose`** in `core-base/database/build.gradle.kts:10` | LOW | Delete in Task 2.1 |
| G36 | **Duplicate license header** in `core-base/database/build.gradle.kts` (lines 1-9 AND 12-19) | LOW | Fix in Task 2.1 |
| G37 | **Room 3 KSP JS/WasmJS code generation unverified** — `@Database` annotation processor must generate `AppDatabase_Impl` for JS/WasmJS. If KSP doesn't support JS target, build fails. | HIGH | Add verification gate G12: confirm Room 3 KSP generates impl for JS/WasmJS. GO/NO-GO for web DB. |
| G38 | **`ChargeTypeConverters.kt` is misnamed** — Template artifact from real Mifos project. Only converts `List<String>` ↔ `String`. | LOW | Optional rename to `StringListTypeConverters.kt` in Phase 6. Not blocking. |
| G39 | **No `room-testing` dependency** — Tests use `Room.inMemoryDatabaseBuilder` but no `room-testing` artifact exists in catalog. Room 3 may move this API. | MED | Verify `inMemoryDatabaseBuilder` location in Room 3. If moved to `room-testing`, add dependency. |
| G40 | **Android factory API signature inconsistent** — Uses `createDatabase(databaseClass: Class<T>)` (Java Class) while Desktop/Native use `createDatabase<T>()` (reified). | LOW | Unify to `inline fun <reified T : RoomDatabase> createDatabase(name: String)` on all platforms. |
| G41 | **`core-base/database` has ZERO tests** — No test source sets at all. AppDatabaseFactory untested. New web factory will also be untested. | MED | Optional: add smoke tests in Phase 6. Or accept risk (infrastructure code, tested transitively via `core/database` tests). |

### Gaps Found in v4 API Audit (G42-G46) — Room 3 Breaking API Changes

| # | Gap | Severity | Fix in v4 |
|:-:|-----|:--------:|-----------|
| G42 | **Android needs explicit SQLiteDriver** — Room 3 removes implicit default driver. Current Android `DatabaseModule` calls `.build()` without `.setDriver()`. Desktop/Native already have `BundledSQLiteDriver` but Android relies on Room's internal default. Room 3 requires explicit driver everywhere. | HIGH | Add `.setDriver(BundledSQLiteDriver())` to Android DI. Or use `AndroidSQLiteDriver()` if Room 3 provides one. Research in Phase 1. |
| G43 | **`Room.databaseBuilder` API signature may change** — Current Android uses `Room.databaseBuilder(context, Class<T>, name)` (3-arg). Room 3 may use `Room.databaseBuilder<T>(context, name)` (reified, 2-arg) or remove Context entirely. Plan Task 2.6 shows code but doesn't verify actual Room 3 API. | MED | Add verification: check Room 3 `Room.databaseBuilder` overloads before writing factory code. Research in Phase 1. |
| G44 | **`setQueryCoroutineContext` may be renamed/removed** — Used in all 6 production + test DI modules. Room 3 blog mentions coroutine integration changes. If renamed, all DI modules break. | MED | Research in Phase 1. If renamed, update all DI modules. Plan Task 3.9-3.12 code examples should use verified API name. |
| G45 | **`SampleEntity` passes ALL @Entity annotation params explicitly** — `@Entity(tableName, indices=[], inheritSuperIndices=false, primaryKeys=[], foreignKeys=[], ignoredColumns=[])`. Room 3 may change param names or defaults. Verbose usage is fragile. | MED | Simplify to `@Entity(tableName = "samples")` — use defaults for empty arrays. Cleaner AND more Room-3-safe. |
| G46 | **`fallbackToDestructiveMigrationOnDowngrade(false)` API** — Used in all production DI modules. Room 3 may change this method name or behavior. | LOW | Research in Phase 1. Low risk since this is a common builder method. |

---

## Phase 1: Version Catalog + Build Logic

**Effort**: 1 day | **Risk**: LOW | **Breaking**: NO (additive only)

| # | Task | File(s) | Status |
|:-:|------|---------|:------:|
| 1.1 | Add Room 3 version + artifacts to version catalog | `gradle/libs.versions.toml` | ⬜ |
| 1.2 | Remove Room 2 version + artifacts from version catalog | `gradle/libs.versions.toml` | ⬜ |
| 1.3 | Update Room gradle plugin reference | `gradle/libs.versions.toml` | ⬜ |
| 1.4 | Update `compileOnly` in build-logic | `build-logic/convention/build.gradle.kts:32` | ⬜ |
| 1.5 | Rewrite `KMPRoomConventionPlugin.kt` for Room 3 — remove `room.generateKotlin` arg (G10), remove `room-ktx` dep line 28 (G34), add `kspJs`+`kspWasmJs` | `build-logic/convention/src/main/kotlin/KMPRoomConventionPlugin.kt` | ⬜ |
| 1.6 | Remove `androidx-room-ktx` from version catalog (G34) | `gradle/libs.versions.toml:161` | ⬜ |
| 1.7 | **RESEARCH**: Verify WebWorkerSQLiteDriver API in Room 3 alpha03 — GO/NO-GO for web DB (G37) | Research task | ⬜ |
| 1.8 | **RESEARCH**: Verify `Room.inMemoryDatabaseBuilder` still in `room-runtime` (not moved to `room-testing`) (G39) | Research task | ⬜ |
| 1.9 | Build verification: `./gradlew :build-logic:convention:build` | Build check | ⬜ |

### Task 1.1-1.3: Version Catalog Changes

```toml
# REPLACE in gradle/libs.versions.toml

# Versions — REPLACE room with room3
room = "3.0.0-alpha03"      # was "2.8.4"
# sqliteBundled = "2.6.2"   # KEEP — still needed for BundledSQLiteDriver

# Libraries — UPDATE artifact coordinates
androidx-room-gradle-plugin = { module = "androidx.room3:room3-gradle-plugin", version.ref = "room" }
androidx-room-compiler = { module = "androidx.room3:room3-compiler", version.ref = "room" }
androidx-room-runtime = { module = "androidx.room3:room3-runtime", version.ref = "room" }
# REMOVE: androidx-room-ktx (merged into room3-runtime)

# Plugin — UPDATE plugin ID
room = { id = "androidx.room3", version.ref = "room" }
# mifos-kmp-room stays same ID, implementation changes
```

### Task 1.5: Convention Plugin Rewrite

```kotlin
// KMPRoomConventionPlugin.kt — FULL REWRITE
class KMPRoomConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) {
        with(target) {
            pluginManager.apply("androidx.room3")
            pluginManager.apply("com.google.devtools.ksp")

            // Room 3: room3 {} config block (not room {})
            extensions.configure<Room3Extension> {
                schemaDirectory("$projectDir/schemas")
            }

            // Room 3: no room.generateKotlin KSP arg (Kotlin-only by default)
            // Room 3: no room-ktx (merged into runtime)

            dependencies {
                // Room 3 runtime for all platforms
                "implementation"(libs.findLibrary("androidx.room.runtime").get())

                // KSP compiler for ALL platforms (including JS/WasmJS — NEW!)
                listOf(
                    "kspAndroid",
                    "kspDesktop",
                    "kspIosArm64",
                    "kspIosX64",
                    "kspIosSimulatorArm64",
                    "kspJs",              // NEW — Room 3 web support
                    "kspWasmJs",          // NEW — Room 3 web support
                ).forEach { platform ->
                    add(platform, libs.findLibrary("androidx.room.compiler").get())
                }
            }
        }
    }
}
```

**Changes from current plugin**:
- `"androidx.room"` → `"androidx.room3"` plugin
- `RoomExtension` → `Room3Extension` (or whatever Room 3 Gradle plugin exposes)
- Remove `room.generateKotlin` KSP arg
- Remove `room-ktx` dependency
- Add `kspJs` + `kspWasmJs` targets
- Keep same plugin ID (`mifos.kmp.room`) to minimize consumer disruption

---

## Phase 2: Remove core-base/database Annotation Abstraction + Update Factories

**Effort**: 1-2 days | **Risk**: MEDIUM | **Breaking**: YES (consumers rebuild on next sync)

### Why DELETE not rewrite:
The entire `Room.kt` expect/actual pattern existed ONLY because Room 2 didn't support JS/WasmJS. Room 3 ships multiplatform annotations that work directly in `commonMain`. Keeping even typealiases adds:
- An unnecessary indirection layer (consumers write `@Query("SQL")` — they ARE coupled to Room)
- Maintenance burden when Room 3 adds new annotations (e.g., `@Fts5`, `@DaoReturnTypeConverter`)
- Confusion for contributors ("why not just use `@androidx.room3.Entity`?")
- Zero future-proofing value (Room annotation API hasn't changed since 1.0)

| # | Task | File(s) | Status |
|:-:|------|---------|:------:|
| 2.1 | Rewrite `build.gradle.kts` — single `commonMain` room3-runtime dep (G23), remove `nonJsCommonMain.dependencies` block (G22), add `sqlite-bundled` to desktopMain+nativeMain (G31), fix duplicate license header (G36), remove unused compose import (G35) | `core-base/database/build.gradle.kts` | ⬜ |
| 2.2 | **DELETE** `Room.kt` (commonMain) — entire expect annotation abstraction (841 lines) | `src/commonMain/.../Room.kt` **DELETE** | ⬜ |
| 2.3 | **DELETE** `Room.nonJsCommon.kt` — actual typealiases | `src/nonJsCommonMain/` **DELETE entire dir** | ⬜ |
| 2.4 | **DELETE** `Room.js.kt` — dummy stubs | `src/jsMain/.../Room.js.kt` **DELETE** | ⬜ |
| 2.5 | **DELETE** `Room.wasmJs.kt` — dummy stubs | `src/wasmJsMain/.../Room.wasmJs.kt` **DELETE** | ⬜ |
| 2.6 | Rewrite `AppDatabaseFactory.kt` (Android) — Room 3 imports, unified reified API (G40), remove `factory` param (G29) | `src/androidMain/.../AppDatabaseFactory.kt` | ⬜ |
| 2.7 | Rewrite `AppDatabaseFactory.kt` (Desktop) — Room 3 imports, remove `findAndInstantiateDatabaseImpl`, remove `factory` param (G29) | `src/desktopMain/.../AppDatabaseFactory.kt` | ⬜ |
| 2.8 | Rewrite `AppDatabaseFactory.kt` (Native) — Room 3 imports, remove `findDatabaseConstructorAndInitDatabaseImpl`, remove `factory` param (G29) | `src/nativeMain/.../AppDatabaseFactory.kt` | ⬜ |
| 2.9 | **CREATE** `AppDatabaseFactory.kt` (JS) — WebWorkerSQLiteDriver (blocked by Task 1.7 research) | `src/jsMain/.../AppDatabaseFactory.kt` **NEW** | ⬜ |
| 2.10 | **CREATE** `AppDatabaseFactory.kt` (WasmJS) — WebWorkerSQLiteDriver (blocked by Task 1.7 research) | `src/wasmJsMain/.../AppDatabaseFactory.kt` **NEW** | ⬜ |
| 2.11 | Build verification on all platforms | `./gradlew :core-base:database:build` | ⬜ |

### Task 2.1: New build.gradle.kts

```kotlin
// core-base/database/build.gradle.kts — REWRITTEN (was 48 lines with issues)
plugins {
    alias(libs.plugins.kmp.core.base.library.convention)
}

android {
    namespace = "template.core.base.database"
}

kotlin {
    sourceSets {
        // Room 3: single commonMain dep covers all platforms (G23)
        commonMain.dependencies {
            implementation(libs.androidx.room.runtime)
        }

        // BundledSQLiteDriver for platforms that need it (G31 — moved from core/database)
        desktopMain.dependencies {
            implementation(libs.androidx.sqlite.bundled)
        }
        nativeMain.dependencies {
            implementation(libs.androidx.sqlite.bundled)
        }

        // NOTE: nonJsCommonMain.dependencies REMOVED (G22)
        // NOTE: per-platform room-runtime REMOVED (G23 — commonMain covers all)
        // NOTE: jsMain/wasmJsMain get room-runtime transitively from commonMain
    }
}
```

### Task 2.2-2.5: What Gets Deleted (~1,100 lines)

```
DELETE: core-base/database/src/commonMain/kotlin/template/core/base/database/Room.kt
        (841 lines — 17 @OptionalExpectation expect annotations + 3 constant objects)

DELETE: core-base/database/src/nonJsCommonMain/  (ENTIRE DIRECTORY)
        (177 lines — actual typealias = androidx.room.* × 20)

DELETE: core-base/database/src/jsMain/kotlin/template/core/base/database/Room.js.kt
        (39 lines — dummy actual annotation stubs)

DELETE: core-base/database/src/wasmJsMain/kotlin/template/core/base/database/Room.wasmJs.kt
        (39 lines — dummy actual annotation stubs)
```

**What stays in `core-base/database`**: Only the `AppDatabaseFactory` files (platform-specific DB path + driver setup). These have real value — they encapsulate OS-specific file paths and SQLiteDriver creation.

### Task 2.6: Android AppDatabaseFactory (Room 3 — Simplified)

```kotlin
package template.core.base.database

import android.content.Context
import androidx.room3.Room
import androidx.room3.RoomDatabase

class AppDatabaseFactory(private val context: Context) {

    inline fun <reified T : RoomDatabase> createDatabase(
        databaseName: String,
    ): RoomDatabase.Builder<T> {
        return Room.databaseBuilder<T>(
            context = context.applicationContext,
            name = context.getDatabasePath(databaseName).absolutePath,
        )
    }
}
```

**Changes**: Import path `androidx.room` → `androidx.room3`. Context stays required on Android (standard DB location via `getDatabasePath`). Removed `findAndInstantiateDatabaseImpl` calls.

### Task 2.7: Desktop AppDatabaseFactory (Room 3)

```kotlin
package template.core.base.database

import androidx.room3.Room
import androidx.room3.RoomDatabase
import java.io.File

class AppDatabaseFactory {

    inline fun <reified T : RoomDatabase> createDatabase(
        databaseName: String,
    ): RoomDatabase.Builder<T> {
        val dbPath = getDatabasePath(databaseName)
        dbPath.parentFile?.mkdirs()
        return Room.databaseBuilder<T>(name = dbPath.absolutePath)
    }

    private fun getDatabasePath(databaseName: String): File {
        val os = System.getProperty("os.name").lowercase()
        val appDir = when {
            os.contains("win") -> File(System.getenv("APPDATA"), "MifosTemplate")
            os.contains("mac") -> File(System.getProperty("user.home"), "Library/Application Support/MifosTemplate")
            else -> File(System.getProperty("user.home"), ".local/share/MifosTemplate")
        }
        return File(appDir, databaseName)
    }
}
```

**Changes**: Import `androidx.room3.*`, remove `findAndInstantiateDatabaseImpl`, use Room 3 context-free builder.

### Task 2.8: Native AppDatabaseFactory (Room 3)

```kotlin
package template.core.base.database

import androidx.room3.Room
import androidx.room3.RoomDatabase
import platform.Foundation.NSFileManager
import platform.Foundation.NSDocumentDirectory
import platform.Foundation.NSUserDomainMask

class AppDatabaseFactory {

    inline fun <reified T : RoomDatabase> createDatabase(
        databaseName: String,
    ): RoomDatabase.Builder<T> {
        val documentDirectory = NSFileManager.defaultManager.URLForDirectory(
            directory = NSDocumentDirectory,
            inDomain = NSUserDomainMask,
            appropriateForURL = null,
            create = false,
            error = null,
        )!!.path!!
        return Room.databaseBuilder<T>(name = "$documentDirectory/$databaseName")
    }
}
```

**Changes**: Import `androidx.room3.*`, remove `findDatabaseConstructorAndInitDatabaseImpl`, use Room 3 context-free builder.

### Task 2.9-2.10: Web AppDatabaseFactory (JS + WasmJS — NEW!)

```kotlin
package template.core.base.database

import androidx.room3.Room
import androidx.room3.RoomDatabase

class AppDatabaseFactory {

    inline fun <reified T : RoomDatabase> createDatabase(
        databaseName: String,
    ): RoomDatabase.Builder<T> {
        // Room 3: WebWorkerSQLiteDriver with OPFS persistence
        return Room.databaseBuilder<T>(name = databaseName)
            .setDriver(WebWorkerSQLiteDriver())
    }
}
```

**Open Question**: WebWorkerSQLiteDriver requires a Worker instance. The exact API depends on how Room 3 ships the WASM SQLite worker. Options:
1. Room 3 bundles a default worker (simplest — check alpha03 release notes)
2. Manual worker URL configuration (requires webpack/resource config in `cmp-web`)
3. NPM package dependency

**This needs verification before implementation** — see Gate G3.

---

## Phase 3: Migrate core/database (Application Layer)

**Effort**: 1-2 days | **Risk**: MEDIUM | **Breaking**: YES (within template)

| # | Task | File(s) | Status |
|:-:|------|---------|:------:|
| 3.1 | Rewrite `build.gradle.kts` — remove per-platform `room-runtime` (G30), remove `sqlite-bundled` (G31, moved to core-base), remove `val desktopMain by getting` (G33) | `core/database/build.gradle.kts` | ⬜ |
| 3.2 | Rewrite `AppDatabase.kt` (commonMain) — single `@Database` class, no expect/actual, remove `@Suppress("NO_ACTUAL_FOR_EXPECT")` (G26) | `src/commonMain/.../AppDatabase.kt` | ⬜ |
| 3.3 | DELETE `AppDatabase.android.kt` | `src/androidMain/.../AppDatabase.android.kt` DELETE | ⬜ |
| 3.4 | DELETE `AppDatabase.desktop.kt` | `src/desktopMain/.../AppDatabase.desktop.kt` DELETE | ⬜ |
| 3.5 | DELETE `AppDatabase.native.kt` — includes BOTH `actual class AppDatabase` AND `expect object AppDatabaseConstructor : RoomDatabaseConstructor<AppDatabase>` (G27) | `src/nativeMain/.../AppDatabase.native.kt` DELETE | ⬜ |
| 3.6 | Update `SampleDao.kt` — change imports to `androidx.room3.*` | `src/commonMain/.../SampleDao.kt` | ⬜ |
| 3.7 | Update `SampleEntity.kt` — change imports to `androidx.room3.*` | `src/commonMain/.../SampleEntity.kt` | ⬜ |
| 3.8 | Update `ChargeTypeConverters.kt` — change imports to `androidx.room3.*` | `src/commonMain/.../ChargeTypeConverters.kt` | ⬜ |
| 3.9 | Rewrite `DatabaseModule.kt` (commonMain) — DB creation in common, use `Dispatchers.IO` (G28) | `src/commonMain/.../DatabaseModule.kt` | ⬜ |
| 3.10 | Simplify `DatabaseModule.android.kt` — provide AppDatabaseFactory only, use `Dispatchers.IO` (G28) | `src/androidMain/.../DatabaseModule.android.kt` | ⬜ |
| 3.11 | Simplify `DatabaseModule.desktop.kt` — provide AppDatabaseFactory only, use `Dispatchers.IO` (G28) | `src/desktopMain/.../DatabaseModule.desktop.kt` | ⬜ |
| 3.12 | Simplify `DatabaseModule.native.kt` — provide AppDatabaseFactory only, use `Dispatchers.IO` (G28) | `src/nativeMain/.../DatabaseModule.native.kt` | ⬜ |
| 3.13 | Rewrite `DatabaseModule.js.kt` — REAL implementation (was empty) | `src/jsMain/.../DatabaseModule.js.kt` | ⬜ |
| 3.14 | Rewrite `DatabaseModule.wasmJs.kt` — REAL implementation (was empty) | `src/wasmJsMain/.../DatabaseModule.wasmJs.kt` | ⬜ |
| 3.15 | **Wire `DatabaseModule` into `KoinModules.allModules`** (G24 — currently dead code!) | `cmp-navigation/.../di/KoinModules.kt` | ⬜ |
| 3.16 | Update `TestDatabaseModule.android.kt` — Room 3 imports | `src/androidUnitTest/` | ⬜ |
| 3.17 | Update `TestDatabaseModule.desktop.kt` — Room 3 imports | `src/desktopTest/` | ⬜ |
| 3.18 | Update `TestDatabaseModule.native.kt` — Room 3 imports | `src/nativeTest/` | ⬜ |
| 3.19 | CREATE `TestDatabaseModule.js.kt` — NEW | `src/jsTest/` NEW | ⬜ |
| 3.20 | CREATE `TestDatabaseModule.wasmJs.kt` — NEW | `src/wasmJsTest/` NEW | ⬜ |
| 3.21 | Update `TestDatabaseModule.kt` (commonTest) expect — add JS/WasmJS actuals | `src/commonTest/` | ⬜ |
| 3.22 | Update ProGuard: `cmp-android/proguard-rules.pro` | `cmp-android/proguard-rules.pro:6` | ⬜ |
| 3.23 | Update ProGuard: `cmp-desktop/compose-desktop.pro` | `cmp-desktop/compose-desktop.pro:166` | ⬜ |
| 3.24 | Verify/update schema JSON compatibility | `core/database/schemas/` | ⬜ |
| 3.25 | Run full test suite | `./gradlew allTests` | ⬜ |

### Task 3.2: Unified AppDatabase (commonMain — direct Room 3 imports)

```kotlin
// ONE file — replaces 3 platform-specific files + 1 expect declaration
package org.mifos.core.database

import androidx.room3.Database
import androidx.room3.RoomDatabase
import androidx.room3.TypeConverters
import org.mifos.core.database.dao.SampleDao
import org.mifos.core.database.entity.SampleEntity
import org.mifos.core.database.utils.ChargeTypeConverters

@Database(
    entities = [SampleEntity::class],
    version = 1,
    exportSchema = true,
)
@TypeConverters(ChargeTypeConverters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract val sampleDao: SampleDao

    companion object {
        const val VERSION = 1
        const val DATABASE_NAME = "mifos_database.db"
    }
}
```

### Task 3.6: SampleDao (import change only)

```kotlin
// BEFORE:
import template.core.base.database.Dao
import template.core.base.database.Insert
import template.core.base.database.OnConflictStrategy
import template.core.base.database.Query

// AFTER:
import androidx.room3.Dao
import androidx.room3.Insert
import androidx.room3.OnConflictStrategy
import androidx.room3.Query
```

No logic changes — just replace `template.core.base.database.*` → `androidx.room3.*`.

### Task 3.1: Simplified build.gradle.kts

```kotlin
// core/database/build.gradle.kts — SIMPLIFIED
plugins {
    alias(libs.plugins.kmp.library.convention)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.kotlin.parcelize)
    alias(libs.plugins.mifos.kmp.room)  // Convention plugin handles room-runtime + KSP compiler
}

android {
    namespace = "org.mifos.core.database"
}

kotlin {
    sourceSets {
        // REMOVED: val desktopMain by getting (G33)
        // REMOVED: per-platform room-runtime (G30 — convention plugin adds it)
        // REMOVED: sqlite-bundled (G31 — moved to core-base/database)

        androidMain.dependencies {
            implementation(libs.koin.android)
        }

        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            api(projects.core.common)
            api(projects.coreBase.database)
        }
    }
}
```

### Task 3.9: CommonMain DI (Database Creation Moves to Common)

```kotlin
package org.mifos.core.database.di

import kotlinx.coroutines.Dispatchers
import org.koin.core.module.Module
import org.koin.dsl.module
import org.mifos.core.database.AppDatabase
import template.core.base.database.AppDatabaseFactory

// NOTE: Name is `platformModule` (matches existing codebase), not `platformDatabaseModule`
val DatabaseModule = module {
    includes(platformModule)

    single<AppDatabase> {
        get<AppDatabaseFactory>()
            .createDatabase<AppDatabase>(
                databaseName = AppDatabase.DATABASE_NAME,
            )
            .setQueryCoroutineContext(Dispatchers.IO)  // Standardized (G28)
            .fallbackToDestructiveMigrationOnDowngrade(false)
            .build()
    }

    single { get<AppDatabase>().sampleDao }
}

// Platform modules provide ONLY: AppDatabaseFactory
expect val platformModule: Module
```

### Task 3.10: Simplified Android DI

```kotlin
// Before: 15+ lines with Context, AppDatabaseFactory, setQueryCoroutineContext, BundledSQLiteDriver
// After: Just provide the factory (DB creation + query context moved to commonMain)
actual val platformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory(androidApplication()) }
}
```

### Task 3.11-3.12: Simplified Desktop/Native DI

```kotlin
// desktopMain / nativeMain — provide factory only
actual val platformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory() }
}
```

### Task 3.13-3.14: Web DI (NEW — Real Implementation!)

```kotlin
// jsMain / wasmJsMain — was EMPTY, now functional!
actual val platformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory() }
}
```

### Task 3.15: Wire DatabaseModule into app DI (G24 — FIX DEAD CODE)

```kotlin
// cmp-navigation/src/commonMain/.../di/KoinModules.kt
// ADD DatabaseModule to allModules list:
object KoinModules {
    val allModules = listOf(
        dataModule,
        dispatcherModule,
        analyticsModule,
        DatastoreModule,
        featureModule,
        AppModule,
        DatabaseModule,  // <-- ADD THIS (was missing — G24)
    )
}
```

### Task 3.21-3.22: ProGuard Updates

```proguard
# BEFORE:
-keep class * extends androidx.room.RoomDatabase { <init>(); }

# AFTER:
-keep class * extends androidx.room3.RoomDatabase { <init>(); }
```

---

## Phase 4: Consumer Project Migration (Sync + Step-by-Step Guide)

**Effort**: 2-3 days (template work + consumer PRs) | **Risk**: MEDIUM
**Applies to**: `mifos-pay`, `mifos-mobile`, `mifos-x-field-officer-app`
**Migration Guide Location**: `server-layer/ROOM3_MIGRATION_GUIDE.md` (shared via sync reference)

| # | Task | File(s) | Status |
|:-:|------|---------|:------:|
| 4.1 | Trigger sync to consumer projects (or wait for weekly cron) | `sync-dirs.sh` / GitHub Actions | ⬜ |
| 4.2 | Write consumer migration guide | `server-layer/ROOM3_MIGRATION_GUIDE.md` NEW | ⬜ |
| 4.3 | Migrate mifos-pay — version catalog + core/database + tests | Consumer PR | ⬜ |
| 4.4 | Migrate mifos-mobile — version catalog + core/database + tests | Consumer PR | ⬜ |
| 4.5 | Migrate mifos-x-field-officer-app — version catalog + core/database + tests | Consumer PR | ⬜ |
| 4.6 | Verify all consumer builds pass on CI | GitHub Actions | ⬜ |

### What Sync Handles Automatically (ZERO manual work)

After template merges to `dev`, the next `sync-dirs.sh` run (weekly cron Monday midnight OR manual dispatch) propagates:

| Directory | Contains | Auto-Synced? |
|-----------|----------|:------------:|
| `core-base/` (includes `database/`) | Room 3 AppDatabaseFactory (rewritten), deleted abstraction layer | **YES** |
| `build-logic/` (includes convention plugin) | KMPRoomConventionPlugin with Room 3 plugin + kspJs/kspWasmJs | **YES** |
| `cmp-desktop/` | Desktop ProGuard + config | **YES** |
| `cmp-web/` | Web module config | **YES** |
| `.github/` | CI workflows | **YES** |

### What Consumers Must Migrate Manually (7 steps)

These directories are NOT synced — each consumer owns them:

| Not Synced | Why |
|-----------|-----|
| `gradle/libs.versions.toml` | Project-specific dependency versions |
| `core/database/` | Project-specific entities, DAOs, DI, AppDatabase |
| `cmp-android/proguard-rules.pro` | Project-specific ProGuard |
| Tests (`*Test/`, `*UnitTest/`) | Project-specific test code |

---

### Step 1: Version Catalog (`gradle/libs.versions.toml`)

**What**: Update Room coordinates from v2 → v3. This is NOT auto-synced.

```toml
# ──── BEFORE (Room 2.8.4) ────
[versions]
room = "2.8.4"

[libraries]
androidx-room-gradle-plugin = { module = "androidx.room:room-gradle-plugin", version.ref = "room" }
androidx-room-compiler = { module = "androidx.room:room-compiler", version.ref = "room" }
androidx-room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }
androidx-room-ktx = { module = "androidx.room:room-ktx", version.ref = "room" }

[plugins]
room = { id = "androidx.room", version.ref = "room" }

# ──── AFTER (Room 3.0) ────
[versions]
room = "3.0.0-alpha03"

[libraries]
androidx-room-gradle-plugin = { module = "androidx.room3:room3-gradle-plugin", version.ref = "room" }
androidx-room-compiler = { module = "androidx.room3:room3-compiler", version.ref = "room" }
androidx-room-runtime = { module = "androidx.room3:room3-runtime", version.ref = "room" }
# DELETED: androidx-room-ktx (merged into room3-runtime)

[plugins]
room = { id = "androidx.room3", version.ref = "room" }
```

**Verification**: `./gradlew :build-logic:convention:build` — convention plugin must resolve new artifacts.

---

### Step 2: Import Migration (`core/database/src/**/*.kt`)

**What**: Replace ALL `template.core.base.database.*` imports with `androidx.room3.*`.

The old `core-base/database` abstraction layer re-exported Room annotations under the `template.core.base.database` package. Room 3 annotations work directly in `commonMain` — use them directly.

**One-liner** (run from project root):
```bash
find core/database/src -name "*.kt" -exec sed -i '' 's/import template\.core\.base\.database\./import androidx.room3./g' {} +
```

**Import mapping** (complete list):

| Room 2 (via abstraction) | Room 3 (direct) |
|--------------------------|-----------------|
| `template.core.base.database.Dao` | `androidx.room3.Dao` |
| `template.core.base.database.Query` | `androidx.room3.Query` |
| `template.core.base.database.Insert` | `androidx.room3.Insert` |
| `template.core.base.database.Update` | `androidx.room3.Update` |
| `template.core.base.database.Delete` | `androidx.room3.Delete` |
| `template.core.base.database.Upsert` | `androidx.room3.Upsert` |
| `template.core.base.database.Transaction` | `androidx.room3.Transaction` |
| `template.core.base.database.Entity` | `androidx.room3.Entity` |
| `template.core.base.database.PrimaryKey` | `androidx.room3.PrimaryKey` |
| `template.core.base.database.ColumnInfo` | `androidx.room3.ColumnInfo` |
| `template.core.base.database.Embedded` | `androidx.room3.Embedded` |
| `template.core.base.database.Relation` | `androidx.room3.Relation` |
| `template.core.base.database.ForeignKey` | `androidx.room3.ForeignKey` |
| `template.core.base.database.Index` | `androidx.room3.Index` |
| `template.core.base.database.Ignore` | `androidx.room3.Ignore` |
| `template.core.base.database.Database` | `androidx.room3.Database` |
| `template.core.base.database.DatabaseView` | `androidx.room3.DatabaseView` |
| `template.core.base.database.TypeConverter` | `androidx.room3.TypeConverter` |
| `template.core.base.database.TypeConverters` | `androidx.room3.TypeConverters` |
| `template.core.base.database.AutoMigration` | `androidx.room3.AutoMigration` |
| `template.core.base.database.OnConflictStrategy` | `androidx.room3.OnConflictStrategy` |
| `template.core.base.database.RoomDatabase` | `androidx.room3.RoomDatabase` |
| `template.core.base.database.ConstructedBy` | **DELETE** — not needed in Room 3 |
| `template.core.base.database.RoomDatabaseConstructor` | **DELETE** — not needed in Room 3 |

**Also replace** any direct Room 2 imports:
```bash
find core/database/src -name "*.kt" -exec sed -i '' 's/import androidx\.room\./import androidx.room3./g' {} +
```

**Verification**: `grep -r "template\.core\.base\.database" core/database/` should return zero matches.

---

### Step 3: Unify AppDatabase to commonMain

**What**: Consumer `AppDatabase` uses expect/actual pattern (like the template). Move to single commonMain class.

#### 3a. Rewrite `core/database/src/commonMain/.../AppDatabase.kt`

```kotlin
// ──── BEFORE (expect class, no annotations) ────
@Suppress("NO_ACTUAL_FOR_EXPECT")
expect abstract class AppDatabase {
    abstract val chargeDao: ChargeDao
    abstract val notificationDao: MifosNotificationDao
    // ... other DAOs
}

// ──── AFTER (concrete class, fully annotated) ────
package org.mifos.core.database  // keep your existing package

import androidx.room3.Database
import androidx.room3.RoomDatabase
import androidx.room3.TypeConverters

@Database(
    entities = [
        ChargeEntity::class,
        MifosNotificationEntity::class,
        // ... ALL your entities here (copy from old platform actuals)
    ],
    version = AppDatabase.VERSION,
    exportSchema = true,
)
@TypeConverters(YourTypeConverters::class)  // if you have type converters
abstract class AppDatabase : RoomDatabase() {
    abstract val chargeDao: ChargeDao
    abstract val notificationDao: MifosNotificationDao
    // ... other DAOs (same as before, just no 'expect')

    companion object {
        const val VERSION = 1  // keep your current version
        const val DATABASE_NAME = "your_database.db"  // keep your current name
    }
}
```

**Key changes**:
- Remove `expect` keyword
- Remove `@Suppress("NO_ACTUAL_FOR_EXPECT")`
- Add `@Database(entities = [...])` — copy entity list from your Android/Desktop actual
- Add `@TypeConverters(...)` — copy from your Android/Desktop actual
- Add `: RoomDatabase()` superclass
- Add `companion object` with VERSION + DATABASE_NAME

#### 3b. DELETE platform-specific AppDatabase actuals

```bash
# DELETE these files — their content is now in commonMain
rm core/database/src/androidMain/kotlin/.../AppDatabase.android.kt
rm core/database/src/desktopMain/kotlin/.../AppDatabase.desktop.kt
rm core/database/src/nativeMain/kotlin/.../AppDatabase.native.kt
```

**IMPORTANT for nativeMain**: The native actual also contains `expect object AppDatabaseConstructor : RoomDatabaseConstructor<AppDatabase>`. This is a Room 2 pattern — **delete it entirely**. Room 3 handles database instantiation internally.

---

### Step 4: Simplify DI Modules

**What**: Move database creation from platform modules → commonMain. Platform modules provide ONLY `AppDatabaseFactory`.

#### 4a. Rewrite `core/database/src/commonMain/.../di/DatabaseModule.kt`

```kotlin
// ──── BEFORE (delegates to platform) ────
val DatabaseModule = module {
    includes(platformModule)
    single { get<AppDatabase>().chargeDao }
    single { get<AppDatabase>().notificationDao }
}
expect val platformModule: Module

// ──── AFTER (DB creation in common, platform provides factory only) ────
package org.mifos.core.database.di

import kotlinx.coroutines.Dispatchers
import org.koin.core.module.Module
import org.koin.dsl.module
import org.mifos.core.database.AppDatabase
import template.core.base.database.AppDatabaseFactory  // still from core-base (synced)

val DatabaseModule = module {
    includes(platformModule)

    // Database creation — SAME on all platforms (was duplicated 5x)
    single<AppDatabase> {
        get<AppDatabaseFactory>()
            .createDatabase<AppDatabase>(
                databaseName = AppDatabase.DATABASE_NAME,
            )
            .setDriver(get())  // SQLiteDriver provided by platform module
            .setQueryCoroutineContext(Dispatchers.IO)
            .fallbackToDestructiveMigrationOnDowngrade(false)
            .build()
    }

    // DAO singletons — list ALL your DAOs
    single { get<AppDatabase>().chargeDao }
    single { get<AppDatabase>().notificationDao }
    // ... add all your DAOs
}

// Platform modules provide: AppDatabaseFactory + SQLiteDriver
expect val platformModule: Module
```

#### 4b. Simplify platform DI modules

**Android** (`DatabaseModule.android.kt`):
```kotlin
actual val platformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory(androidApplication()) }
    single { BundledSQLiteDriver() as SQLiteDriver }  // Room 3 requires explicit driver
}
```

**Desktop** (`DatabaseModule.desktop.kt`):
```kotlin
actual val platformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory() }
    single { BundledSQLiteDriver() as SQLiteDriver }
}
```

**Native/iOS** (`DatabaseModule.native.kt`):
```kotlin
actual val platformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory() }
    single { BundledSQLiteDriver() as SQLiteDriver }
}
```

**JS** (`DatabaseModule.js.kt`) — was EMPTY, now functional:
```kotlin
actual val platformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory() }
    // WebWorkerSQLiteDriver provided by AppDatabaseFactory (synced from core-base)
}
```

**WasmJS** (`DatabaseModule.wasmJs.kt`) — same as JS:
```kotlin
actual val platformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory() }
}
```

---

### Step 5: Update `core/database/build.gradle.kts`

**What**: Remove redundant Room dependencies. Convention plugin + core-base handle everything.

```kotlin
// ──── REMOVE these blocks (convention plugin adds room-runtime) ────
// DELETE: androidMain.dependencies { implementation(libs.androidx.room.runtime) }
// DELETE: desktopMain.dependencies { implementation(libs.androidx.room.runtime) }
// DELETE: nativeMain.dependencies { implementation(libs.androidx.room.runtime) }
// DELETE: desktopMain.dependencies { implementation(libs.androidx.sqlite.bundled) }
// DELETE: nativeMain.dependencies { implementation(libs.androidx.sqlite.bundled) }
// DELETE: val desktopMain by getting { ... }  (Gradle anti-pattern)

// ──── KEEP ────
commonMain.dependencies {
    implementation(libs.kotlinx.coroutines.core)
    implementation(libs.kotlinx.serialization.json)
    api(projects.core.common)
    api(projects.coreBase.database)  // brings Room 3 runtime transitively
}
androidMain.dependencies {
    implementation(libs.koin.android)
}
```

---

### Step 6: Update Tests

**What**: Update test imports + add web platform test modules.

#### 6a. Update existing test imports

```bash
# Same sed as Step 2, but for test source sets
find core/database/src -path "*/test*" -name "*.kt" -exec sed -i '' \
  's/import androidx\.room\.Room/import androidx.room3.Room/g' {} +
```

**Test DI modules** — same simplification as production:
```kotlin
// TestDatabaseModule.android.kt — BEFORE
Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)

// TestDatabaseModule.android.kt — AFTER
Room.inMemoryDatabaseBuilder<AppDatabase>(context)  // Room 3 reified API
```

#### 6b. CREATE web test modules (NEW)

```kotlin
// core/database/src/jsTest/kotlin/.../di/TestDatabaseModule.js.kt
actual val testPlatformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory() }
}

// core/database/src/wasmJsTest/kotlin/.../di/TestDatabaseModule.wasmJs.kt
actual val testPlatformModule: Module = module {
    single<AppDatabaseFactory> { AppDatabaseFactory() }
}
```

#### 6c. Remove `@Suppress("NO_ACTUAL_FOR_EXPECT")` from TestDatabaseModule.kt (commonTest)

---

### Step 7: ProGuard + Verification

#### 7a. Update ProGuard rules (if project has custom rules)
```proguard
# BEFORE:
-keep class * extends androidx.room.RoomDatabase { <init>(); }

# AFTER:
-keep class * extends androidx.room3.RoomDatabase { <init>(); }
```

#### 7b. Wire DatabaseModule (if not already wired)

Check `cmp-navigation/.../di/KoinModules.kt` — ensure `DatabaseModule` is in `allModules`:
```kotlin
object KoinModules {
    val allModules = listOf(
        // ... existing modules ...
        DatabaseModule,  // ADD if missing
    )
}
```

#### 7c. Verification checklist

```
□ ./gradlew :core:database:build                    — compiles all platforms
□ ./gradlew :core:database:allTests                 — all tests pass
□ ./gradlew :cmp-android:assembleDebug              — Android app builds
□ ./gradlew :cmp-desktop:run                        — Desktop app launches
□ grep -r "template\.core\.base\.database" core/    — ZERO matches
□ grep -r "androidx\.room\." core/ | grep -v room3  — ZERO matches (no Room 2 leftovers)
□ grep -r "findAndInstantiateDatabaseImpl" core/    — ZERO matches
□ grep -r "findDatabaseConstructorAndInitDatabaseImpl" core/ — ZERO matches
□ grep -r "RoomDatabaseConstructor" core/           — ZERO matches
□ grep -r "NO_ACTUAL_FOR_EXPECT" core/database/     — ZERO matches
□ Verify existing database files still readable     — backward compat (Room 3 reads Room 2 schemas)
```

---

### Consumer Migration Summary

| What Changes | Where | How |
|-------------|-------|-----|
| Room version + artifacts | `gradle/libs.versions.toml` | Manual edit (Step 1) |
| All Room imports | `core/database/src/**/*.kt` | `sed` find-and-replace (Step 2) |
| AppDatabase class | `commonMain/AppDatabase.kt` | Rewrite: expect→concrete (Step 3) |
| 3 platform AppDatabase actuals | `androidMain/`, `desktopMain/`, `nativeMain/` | **DELETE** (Step 3b) |
| DI modules (5 platform files) | `*/di/DatabaseModule.*.kt` | Simplify to factory-only (Step 4) |
| build.gradle.kts | `core/database/build.gradle.kts` | Remove redundant deps (Step 5) |
| Tests | `*Test/**/*.kt` | Import update + add web tests (Step 6) |
| ProGuard | `cmp-android/proguard-rules.pro` | Class name update (Step 7) |

**Estimated time per consumer**: 2-4 hours (mostly mechanical find-and-replace + delete)

### Per-Consumer App Notes

#### mifos-mobile
- Has more entities than template (ChargeEntity, MifosNotificationEntity, ClientEntity, etc.)
- Copy ALL entity classes from `@Database(entities = [...])` in the old Android actual → new commonMain AppDatabase
- Has custom TypeConverters — update imports

#### mifos-pay
- Likely has payment-specific entities (TransactionEntity, etc.)
- Same migration pattern — unify AppDatabase to commonMain
- May have additional DAOs — ensure all are listed in commonMain DatabaseModule

#### mifos-x-field-officer-app
- Field-officer-specific entities (LoanEntity, CenterEntity, GroupEntity, etc.)
- Largest entity count — take extra care copying entity list to commonMain
- May have Room migrations (version > 1) — these need `androidx.room` → `androidx.room3` in migration callbacks

---

## Phase 5: Web Platform Verification

**Effort**: 1-2 days | **Risk**: HIGH (new platform, alpha API)

| # | Task | File(s) | Status |
|:-:|------|---------|:------:|
| 5.1 | **Add `core.database` dependency to `cmp-web`** (G25 — currently missing!) | `cmp-web/build.gradle.kts` | ⬜ |
| 5.2 | Verify WebWorkerSQLiteDriver API in Room 3.0-alpha03 (if not done in 1.7) | Research | ⬜ |
| 5.3 | Configure WASM SQLite worker in `cmp-web` (webpack/resource config) | `cmp-web/webpack.config.d/` | ⬜ |
| 5.4 | **Verify KSP generates `AppDatabase_Impl` for JS/WasmJS** (G37 — GO/NO-GO gate) | Build + inspect output | ⬜ |
| 5.5 | Test CRUD operations in browser (Chrome, Firefox, Safari) | Manual test | ⬜ |
| 5.6 | Test OPFS storage persistence across page reloads | Manual test | ⬜ |
| 5.7 | Test in-memory database for web tests | Automated test | ⬜ |
| 5.8 | Verify no SQLite worker bundling needed (if Room 3 ships built-in) | Research | ⬜ |

### Web Platform Open Questions

| Question | Impact | Resolution Needed Before |
|----------|:------:|--------------------------|
| Does Room 3 alpha03 ship a default WebWorker? | HIGH | Phase 2 Task 2.9 |
| What's the minimum browser version for OPFS? | MED | Phase 5 Task 5.3 |
| Can in-memory DB work on web without WebWorker? | MED | Phase 3 Task 3.18 |
| Does `cmp-web` Webpack config need SQLite WASM asset? | HIGH | Phase 5 Task 5.2 |

---

## Phase 6: Cleanup

**Effort**: 0.5 day | **Risk**: LOW

| # | Task | File(s) | Status |
|:-:|------|---------|:------:|
| 6.1 | Verify no remaining `androidx.room` (v2) references in project | `grep -r "androidx.room[^3]"` | ⬜ |
| 6.2 | Verify no remaining `template.core.base.database` imports (abstraction layer fully removed) | `grep -r "template.core.base.database"` | ⬜ |
| 6.3 | Verify no remaining `findAndInstantiateDatabaseImpl` / `findDatabaseConstructorAndInitDatabaseImpl` | grep | ⬜ |
| 6.4 | Update CLAUDE.md — Room entry in Tech Stack | `CLAUDE.md` | ⬜ |
| 6.5 | Update README if Room version mentioned | `README.md` | ⬜ |
| 6.6 | Optional: rename `ChargeTypeConverters.kt` → `StringListTypeConverters.kt` (G38) | `src/commonMain/.../utils/` | ⬜ |
| 6.7 | Optional: add AppDatabaseFactory smoke tests (G41) | `core-base/database/src/commonTest/` | ⬜ |
| 6.8 | Tag release: `v{next}-room3-migration` | Git tag | ⬜ |

---

## Verification Gates

| Gate | Criteria | Phase | Blocking? |
|------|----------|:-----:|:---------:|
| G1 | Convention plugin compiles with Room 3 gradle plugin | 1 | YES |
| G2 | WebWorkerSQLiteDriver API verified + Room 3 `inMemoryDatabaseBuilder` location confirmed | 1 | YES |
| G3 | `core-base/database` builds on all 7 targets (android, desktop, ios×3, js, wasmJs) | 2 | YES |
| G4 | `core/database` builds on all platforms | 3 | YES |
| G5 | All existing tests pass (android, desktop, native) | 3 | YES |
| G6 | Schema JSON generated correctly under `schemas/` | 3 | YES |
| G7 | Existing Room 2 database files readable by Room 3 (backward compat) | 3 | YES |
| G8 | `DatabaseModule` is wired into app DI and app launches without crash | 3 | YES |
| G9 | **Room 3 KSP generates `AppDatabase_Impl` for JS/WasmJS targets** (G37 — GO/NO-GO) | 5 | YES |
| G10 | Web CRUD: insert, query, update, delete work in browser | 5 | YES |
| G11 | OPFS data persists across page reloads | 5 | NO (nice to have) |
| G12 | Consumer sync delivers correct files | 4 | YES |
| G13 | At least 1 consumer project builds after sync + manual changes | 4 | YES |
| G14 | Zero remaining `androidx.room` (v2) or `template.core.base.database` references | 6 | YES |

---

## File Change Summary

### Files DELETED (~1,100 lines removed)

| File | Lines | Reason |
|------|:-----:|--------|
| `core-base/database/src/commonMain/.../Room.kt` | 841 | **Abstraction layer removed** — Room 3 annotations work directly in commonMain |
| `core-base/database/src/nonJsCommonMain/` (entire dir) | 177 | **Abstraction layer removed** — actual typealiases no longer needed |
| `core-base/database/src/jsMain/.../Room.js.kt` | 39 | **Abstraction layer removed** — dummy stubs no longer needed |
| `core-base/database/src/wasmJsMain/.../Room.wasmJs.kt` | 39 | **Abstraction layer removed** — dummy stubs no longer needed |
| `core/database/src/androidMain/.../AppDatabase.android.kt` | ~20 | Unified to commonMain |
| `core/database/src/desktopMain/.../AppDatabase.desktop.kt` | ~20 | Unified to commonMain |
| `core/database/src/nativeMain/.../AppDatabase.native.kt` | ~25 | Unified to commonMain (includes AppDatabaseConstructor) |

### Files CREATED (new)

| File | Reason |
|------|--------|
| `core-base/database/src/jsMain/.../AppDatabaseFactory.kt` | Web database creation (WebWorkerSQLiteDriver) |
| `core-base/database/src/wasmJsMain/.../AppDatabaseFactory.kt` | Web database creation (WebWorkerSQLiteDriver) |
| `core/database/src/jsTest/.../TestDatabaseModule.js.kt` | Web test support |
| `core/database/src/wasmJsTest/.../TestDatabaseModule.wasmJs.kt` | Web test support |
| `docs/ROOM3_MIGRATION_GUIDE.md` | Consumer migration instructions |

### Files REWRITTEN (major changes)

| File | Change Summary |
|------|---------------|
| `gradle/libs.versions.toml` | Room 2→3 coordinates, remove `room-ktx` entry (G34) |
| `build-logic/.../KMPRoomConventionPlugin.kt` | Room 3 plugin, add kspJs/kspWasmJs, remove `room.generateKotlin` (G10), remove `room-ktx` line (G34) |
| `build-logic/convention/build.gradle.kts` | Room 3 gradle plugin compileOnly |
| `core-base/database/build.gradle.kts` | Single commonMain dep (G23), add sqlite-bundled (G31), remove nonJsCommonMain deps (G22), fix duplicate header (G36), remove unused compose import (G35) |
| `core-base/database/src/androidMain/.../AppDatabaseFactory.kt` | Room 3 imports, reified generic API (G40), remove factory param (G29) |
| `core-base/database/src/desktopMain/.../AppDatabaseFactory.kt` | Room 3 imports, remove `findAndInstantiateDatabaseImpl`, remove factory param (G29) |
| `core-base/database/src/nativeMain/.../AppDatabaseFactory.kt` | Room 3 imports, remove `findDatabaseConstructorAndInitDatabaseImpl`, remove factory param (G29) |
| `core/database/build.gradle.kts` | Remove redundant room-runtime (G30), remove sqlite-bundled (G31), remove `val desktopMain by getting` (G33) |
| `core/database/src/commonMain/.../AppDatabase.kt` | Full @Database class (was expect), remove `@Suppress("NO_ACTUAL_FOR_EXPECT")` (G26) |
| `core/database/src/commonMain/.../SampleDao.kt` | Import: `template.core.base.database.*` → `androidx.room3.*` |
| `core/database/src/commonMain/.../SampleEntity.kt` | Import: `template.core.base.database.*` → `androidx.room3.*` |
| `core/database/src/commonMain/.../ChargeTypeConverters.kt` | Import: `template.core.base.database.*` → `androidx.room3.*` |
| `core/database/src/commonMain/.../DatabaseModule.kt` | DB creation in common, standardized `Dispatchers.IO` (G28) |
| `core/database/src/androidMain/.../DatabaseModule.android.kt` | Factory-only, standardized `Dispatchers.IO` (G28) |
| `core/database/src/desktopMain/.../DatabaseModule.desktop.kt` | Factory-only, standardized `Dispatchers.IO` (G28) |
| `core/database/src/nativeMain/.../DatabaseModule.native.kt` | Factory-only, standardized `Dispatchers.IO` (G28) |
| `core/database/src/jsMain/.../DatabaseModule.js.kt` | Real implementation (was empty) |
| `core/database/src/wasmJsMain/.../DatabaseModule.wasmJs.kt` | Real implementation (was empty) |
| `cmp-navigation/.../di/KoinModules.kt` | Wire `DatabaseModule` into `allModules` (G24) |
| `cmp-web/build.gradle.kts` | Add `core.database` dependency (G25) |
| `cmp-android/proguard-rules.pro` | Room 3 class name |
| `cmp-desktop/compose-desktop.pro` | Room 3 class name |
| Test modules (android/desktop/native) | Room 3 imports |

---

## Risk Register

| ID | Risk | Prob | Impact | Mitigation |
|:--:|------|:----:|:------:|------------|
| R1 | Room 3.0 alpha instability | MED | HIGH | Pin alpha03, have rollback plan (git revert) |
| R2 | WebWorkerSQLiteDriver needs manual worker setup | MED | HIGH | Research in Phase 1 (Task 1.7); fallback: empty web DB module with warning |
| R3 | OPFS browser support gaps | MED | MED | Safari 17.4+, Chrome 110+, Firefox 111+ — document minimum versions |
| R4 | KSP version conflict | LOW | HIGH | Use Room 3's bundled KSP version |
| R5 | Consumer projects break on next sync | MED | MED | Migration guide + coordinated PRs + announce on Discord/Slack |
| R6 | `libs.versions.toml` NOT auto-synced | HIGH | HIGH | Include in migration guide; consumers MUST update manually |
| R7 | ProGuard rules in non-synced files | MED | MED | Include in migration guide |
| R8 | Schema path change breaks auto-migrations | LOW | HIGH | Schema path is DB-class-based (`org.mifos.core.database.AppDatabase`), NOT Room package. Likely non-issue. Verify in Phase 3. |
| R9 | `Room3Extension` class name differs from plan | LOW | LOW | Check Room 3 Gradle plugin source for exact class name |
| R10 | **Room 3 KSP doesn't generate JS/WasmJS database impl** (G37) | MED | **CRITICAL** | Verify in Phase 1 research (Task 1.7). If fails: web platform gets empty module (no DB) — same as Room 2 but with documented limitation. |
| R11 | **DatabaseModule is dead code** — wiring it (G24) may expose latent issues (missing Koin providers, circular deps) | MED | MED | Test app launch on all platforms after wiring. Consider keeping unwired if template is intentionally minimal. |
| R12 | `room-testing` artifact may be needed for Room 3 `inMemoryDatabaseBuilder` (G39) | LOW | MED | Research in Phase 1 (Task 1.8). If moved, add to version catalog. |

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-29 | ~~Parallel module~~ → **In-place migration** | sync-dirs.sh propagates core-base/ + build-logic/ to consumers automatically |
| 2026-04-29 | ~~Keep typealiases~~ → **DELETE entire abstraction layer** (v3) | Room 3 annotations work directly in commonMain on all platforms. Typealiases add zero value — consumers write Room-specific SQL, they ARE coupled to Room. ~1,100 lines of dead weight removed |
| 2026-04-29 | Consumer imports change: `template.core.base.database.*` → `androidx.room3.*` | Simple find-and-replace, no logic changes. Consumers already depend on Room semantics |
| 2026-04-29 | Keep same convention plugin ID `mifos.kmp.room` | Consumers don't need to change their `build.gradle.kts` plugin reference |
| 2026-04-29 | Target Room 3.0-alpha03 | Latest with critical bug fixes (code too large, no-arg constructor) |
| 2026-04-29 | Remove nonJsCommonMain source set entirely | Room 3 commonMain covers all platforms — intermediate source set is dead weight |
| 2026-04-29 | Keep Android Context in AppDatabaseFactory | Android needs `getDatabasePath()` for standard DB location; Context stays required |
| 2026-04-29 | Keep AppDatabaseFactory in core-base | Platform-specific DB paths + drivers still have real value (unlike annotation forwarding) |
| 2026-04-30 | Standardize DI dispatchers to `Dispatchers.IO` (G28) | Simpler, no Koin dep for dispatchers. Native was inconsistent with Android/Desktop. |
| 2026-04-30 | Move `sqlite-bundled` to `core-base/database` (G31) | `BundledSQLiteDriver` is used in AppDatabaseFactory (core-base), not in core/database. Dep should follow usage. |
| 2026-04-30 | Wire `DatabaseModule` into app DI (G24) | Template should be functional out-of-the-box. Dead code in a template is a bad signal. |
| 2026-04-30 | Remove `factory` parameter from AppDatabaseFactory (G29) | Room 3 handles instantiation internally. The parameter wrapping `findAndInstantiateDatabaseImpl` has no replacement in Room 3. |
| 2026-04-30 | Unify AppDatabaseFactory to reified generics on all platforms (G40) | Android used Java Class ref (`Class<T>`), others used reified. Room 3 supports reified everywhere. |
| 2026-04-30 | `nonJsCommonMain` hierarchy stays — only remove from database build (G22) | `core-base/analytics` still uses it. Don't break unrelated module. |
| 2026-04-30 | Schema path is DB-class-based, NOT Room-package-based (G19 resolved) | `org.mifos.core.database.AppDatabase` doesn't change — schema export path is safe. |

---

## Timeline (Revised v4)

```
Day 1:    Phase 1 (Version catalog + build-logic + RESEARCH: WebWorkerSQLiteDriver, inMemoryDatabaseBuilder)
          ↳ Gate G1 (convention plugin compiles) + Gate G2 (research results)
Day 2-3:  Phase 2 (core-base/database: delete abstraction, rewrite factories)
          ↳ Gate G3 (core-base builds all 7 targets)
Day 3-5:  Phase 3 (core/database: unify AppDatabase, DI, tests, wire into app)
          ↳ Gate G4 (builds all) + G5 (tests pass) + G6 (schema) + G7 (backward compat) + G8 (app DI works)
Day 5-7:  Phase 5 (Web platform: add cmp-web dep, verify KSP JS, test browser CRUD)
          ↳ Gate G9 (KSP JS impl) + G10 (web CRUD)
Day 7-8:  Phase 4 (Consumer sync + migration PRs)
          ↳ Gate G12 (sync correct) + G13 (consumer builds)
Day 8-9:  Phase 6 (Cleanup + verification sweep)
          ↳ Gate G14 (zero v2 references)

Total: ~1.5 weeks (focused)
       ~2 weeks (with web platform debugging)
```

**Critical path**: Phase 1 research (Task 1.7) determines if web DB is feasible. If Room 3 KSP doesn't generate JS impl → skip web DB tasks, keep empty modules, save 2 days.

---

## References

- [Room 3.0 Blog Post](https://android-developers.googleblog.com/2026/03/room-30-modernizing-room.html)
- [Room 3 Release Notes](https://developer.android.com/jetpack/androidx/releases/room3)
- Sync script: `sync-dirs.sh` (syncs `core-base/` + `build-logic/` to consumers)
- Sync workflow: `.github/workflows/sync-dirs.yaml` (weekly cron + manual)
- Convention plugin: `build-logic/convention/src/main/kotlin/KMPRoomConventionPlugin.kt`
- Current annotations: `core-base/database/src/commonMain/kotlin/template/core/base/database/Room.kt`
- Consumer projects: [mifos-pay](https://github.com/openMF/mifos-pay), [mifos-mobile](https://github.com/openMF/mifos-mobile), [mifos-x-field-officer-app](https://github.com/openMF/mifos-x-field-officer-app)
