# Room 2 → Room 3 Migration Guide (Consumer Projects)

**Applies to**: `mobile-wallet` (mifos-pay), `mifos-mobile`, `mifos-x-field-officer-app`
**Last Updated**: 2026-04-30
**Executor**: Claude Code (automated migration via `/gap-implement-project`)

---

## Pre-Migration Audit (Per-Project Baseline)

| Project | Current Room | Current Kotlin | Current KSP | Current Compose | DB Class | Entities | DAOs | TypeConverters |
|---------|:------------:|:--------------:|:-----------:|:---------------:|----------|:--------:|:----:|:--------------:|
| **mobile-wallet** | 2.8.4 | 2.2.21 | 2.2.21-2.0.4 | 1.9.3 | N/A (base only) | 0 | 0 | 0 |
| **mifos-mobile** | **2.7.2** | **2.1.20** | **2.1.20-2.0.1** | **1.8.2** | `AppDatabase` | 2 | 2 | 12 methods |
| **field-officer** | 2.8.4 | 2.2.21 | 2.2.21-2.0.4 | 1.9.3 | **`MifosDatabase`** | **56** | **10** | **100+ methods** |

> **CRITICAL**: All three projects need different version jumps. mifos-mobile is TWO major Kotlin versions behind (2.1.20 → 2.3.20).

---

## What sync-dirs.sh Propagates Automatically (FREE)

After the template merges Room 3 to `dev`, the next `sync-dirs.sh` run propagates:

| Directory | What Changes | Action Required |
|-----------|-------------|:---------------:|
| `core-base/database/` | New `AppDatabaseFactory` (reified generics, no `findAndInstantiateDatabaseImpl`/`findDatabaseConstructorAndInitDatabaseImpl`), deleted `Room.kt`+`Room.nonJsCommon.kt`+`Room.js.kt`+`Room.wasmJs.kt` abstraction layer, new JS/WasmJS factories | **None** |
| `build-logic/convention/` | `KMPRoomConventionPlugin` rewritten for `androidx.room3` plugin + `kspJs`/`kspWasmJs` targets, removed `room.generateKotlin` KSP arg | **None** |
| `cmp-desktop/` | ProGuard rule updated to `androidx.room3.RoomDatabase` | **None** |
| `cmp-web/` | `core.database` dependency added | **None** |
| `.github/` | CI workflows | **None** |

## What You Must Migrate Manually

| Not Synced | Why | Effort |
|-----------|-----|:------:|
| `gradle/libs.versions.toml` | Project-specific versions | Low |
| `core/database/` (all source sets) | Project-specific entities, DAOs, DI, database class | **High** |
| ProGuard (if project-specific rules) | Project-specific obfuscation | Low |
| Tests (`*Test/`, `*UnitTest/`) | Project-specific test code | Medium |

---

## Step 0: Pre-Flight Checks

Before ANY code changes, verify the starting state:

```bash
# 1. Confirm sync-dirs.sh has already run (core-base should have Room 3 factories)
grep "room3" core-base/database/src/androidMain/kotlin/template/core/base/database/AppDatabaseFactory.kt
# Expected: "import androidx.room3.Room" — if not found, run sync-dirs.sh first

# 2. Confirm convention plugin is Room 3
grep "androidx.room3" build-logic/convention/src/main/kotlin/KMPRoomConventionPlugin.kt
# Expected: pluginManager.apply("androidx.room3")

# 3. Count files to migrate (scope check)
grep -rl "template\.core\.base\.database\." core/database/src/ | wc -l
grep -rl "import androidx\.room\." core/database/src/ | wc -l
```

**If sync-dirs.sh has NOT run yet**: Run it first, then return to Step 1.

---

## Step 1: Version Catalog (`gradle/libs.versions.toml`)

### 1a. Update Core Versions

These MUST all be updated together (klib compiler version lock):

```toml
# ---- FIND AND REPLACE these version values ----
# Kotlin: any 2.x.x → 2.3.20
kotlin = "2.3.20"

# KSP: any 2.x.x-y.y.y → 2.3.6  (KSP2, decoupled from Kotlin)
ksp = "2.3.6"

# Compose Multiplatform: any 1.x.x → 1.10.3
compose-plugin = "1.10.3"   # may also be named "composeJB" or "composeCMP"

# Room: any 2.x.x → 3.0.0-alpha03
room = "3.0.0-alpha03"

# SQLite Bundled: any 2.x.x → 2.6.2  (if present)
sqliteBundled = "2.6.2"
```

### 1b. Update Room Library Coordinates

```toml
# ---- BEFORE ----
androidx-room-gradle-plugin = { module = "androidx.room:room-gradle-plugin", version.ref = "room" }
androidx-room-compiler = { module = "androidx.room:room-compiler", version.ref = "room" }
androidx-room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }
androidx-room-ktx = { module = "androidx.room:room-ktx", version.ref = "room" }

[plugins]
room = { id = "androidx.room", version.ref = "room" }

# ---- AFTER ----
androidx-room-gradle-plugin = { module = "androidx.room3:room3-gradle-plugin", version.ref = "room" }
androidx-room-compiler = { module = "androidx.room3:room3-compiler", version.ref = "room" }
androidx-room-runtime = { module = "androidx.room3:room3-runtime", version.ref = "room" }
# DELETE: androidx-room-ktx (merged into room3-runtime)

[plugins]
room = { id = "androidx.room3", version.ref = "room" }
```

### 1c. Add sqlite-web (for JS/WasmJS support)

```toml
[libraries]
# ADD this new entry:
androidx-sqlite-web = { module = "androidx.sqlite:sqlite-web", version.ref = "sqliteBundled" }
```

### 1d. Remove Obsolete Entries

```toml
# DELETE these lines if present:
# androidx-room-ktx (merged into runtime)
# room-paging (update to room3 coordinates if needed)
# androidx-room-testing (update to room3 coordinates if needed)
```

### Per-Project Notes

| Project | Extra Version Changes |
|---------|----------------------|
| **mifos-mobile** | SQLite bundled `2.5.0-alpha12` → `2.6.2`. Also has `uiBackhandler` version tied to Compose — update to `1.10.3` |
| **field-officer** | `room-paging` entry exists — update to `androidx.room3:room3-paging` if still needed |
| **mobile-wallet** | Room plugin declared but NOT applied (no convention plugin) — sync will add it |

**Verify**: `./gradlew :build-logic:convention:build` — convention plugin must resolve new artifacts.

---

## Step 2: Import Migration (`core/database/src/**/*.kt`)

Two categories of imports need replacing:

### 2a. Replace `template.core.base.database.*` Imports

The old `core-base/database` abstraction layer (`Room.kt`, `Room.nonJsCommon.kt`) re-exported Room annotations as `template.core.base.database.*`. Room 3 annotations work directly in commonMain — use them directly.

```bash
# Run from project root:
find core/database/src -name "*.kt" -exec sed -i '' 's/import template\.core\.base\.database\./import androidx.room3./g' {} +
```

**Complete mapping**:

| Old Import | New Import |
|-----------|-----------|
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

### 2b. Replace Direct `androidx.room.*` Imports

AppDatabase actual files and some DI modules import `androidx.room` directly:

```bash
find core/database/src -name "*.kt" -exec sed -i '' 's/import androidx\.room\./import androidx.room3./g' {} +
```

### 2c. Replace `template.core.base.database.AppDatabaseFactory` Import

The factory import stays the same (core-base is synced), but verify it exists:

```bash
# This import should still work after sync (core-base factories keep the same package):
grep -r "import template.core.base.database.AppDatabaseFactory" core/database/src/
# Expected: matches in each platform DI module
```

### Per-Project Notes

| Project | Import Specifics |
|---------|-----------------|
| **mifos-mobile** | DAOs use `template.core.base.database.*`, AppDatabase actuals use `androidx.room.*` directly — both sed commands needed |
| **field-officer** | 56 entities + 10 DAOs + 100+ TypeConverters all use `template.core.base.database.*` — the sed command handles all of them |
| **mobile-wallet** | No `core/database` files — skip this step |

**Verify**: Both grep commands return zero matches:
```bash
grep -r "template\.core\.base\.database\." core/database/ | grep -v "AppDatabaseFactory"
grep -r "import androidx\.room\." core/database/ | grep -v room3
```

---

## Step 3: Unify Database Class to commonMain

Currently each project has an expect/actual pattern:
- `commonMain`: `expect abstract class XxxDatabase { abstract val xxxDao: XxxDao }`
- `androidMain`/`desktopMain`: `@Database(...) actual abstract class XxxDatabase : RoomDatabase()`
- `nativeMain`: Same + `@ConstructedBy(XxxDatabaseConstructor::class)`
- `jsMain`/`wasmJsMain`: Empty stub (`actual abstract class XxxDatabase { ... }`)

Room 3 unifies this into a single `commonMain` class.

### 3a. Identify Your Database Class Name

| Project | Class Name | Package |
|---------|-----------|---------|
| **mifos-mobile** | `AppDatabase` | `org.mifos.mobile.core.database` |
| **field-officer** | `MifosDatabase` | `com.mifos.room` |
| **mobile-wallet** | N/A | N/A |

### 3b. Rewrite the commonMain Database Class

Replace the `expect abstract class` with a fully-annotated concrete class:

```kotlin
package <YOUR_PACKAGE>  // keep your existing package

import androidx.room3.ConstructedBy
import androidx.room3.Database
import androidx.room3.RoomDatabase
import androidx.room3.RoomDatabaseConstructor
import androidx.room3.TypeConverters

// KSP generates the actual object on each platform automatically
@Suppress("NO_ACTUAL_FOR_EXPECT")
expect object <YourDB>Constructor : RoomDatabaseConstructor<<YourDB>>

@Database(
    entities = [
        // COPY the full entity list from your Android/Desktop actual
        // e.g., ChargeEntity::class, MifosNotificationEntity::class, ...
    ],
    version = <YourDB>.VERSION,
    exportSchema = true,  // Room 3 recommends true for schema tracking
)
@TypeConverters(<YourTypeConverters>::class)
@ConstructedBy(<YourDB>Constructor::class)
abstract class <YourDB> : RoomDatabase() {
    // COPY all abstract DAO properties from the old expect class
    abstract val chargeDao: ChargeDao
    // ...

    companion object {
        const val VERSION = 1  // keep your current version
        const val DATABASE_NAME = "your_database.db"  // keep your current name
    }
}
```

### Per-Project Entity Lists

**mifos-mobile** (2 entities — copy this exact list):
```kotlin
@Database(
    entities = [
        ChargeEntity::class,
        MifosNotificationEntity::class,
    ],
    version = AppDatabase.VERSION,
    exportSchema = true,
)
@TypeConverters(ChargeTypeConverters::class)
@ConstructedBy(AppDatabaseConstructor::class)
abstract class AppDatabase : RoomDatabase() {
    abstract val mifosNotificationDao: MifosNotificationDao
    abstract val chargeDao: ChargeDao

    companion object {
        const val VERSION = 1
        const val DATABASE_NAME = "mifos_database.db"
    }
}
```

**field-officer** (56 entities — copy from androidMain/desktopMain actual):
```kotlin
@Database(
    entities = [
        // Loans (9)
        ActualDisbursementDateEntity::class, LoanAccountEntity::class,
        LoanRepaymentRequestEntity::class, LoanRepaymentResponseEntity::class,
        LoanStatusEntity::class, LoanTimelineEntity::class, LoanTypeEntity::class,
        LoanWithAssociationsEntity::class, LoansAccountSummaryEntity::class,
        // Savings (11)
        SavingAccountCurrencyEntity::class, SavingAccountDepositTypeEntity::class,
        SavingsAccountEntity::class, SavingsAccountStatusEntity::class,
        SavingsAccountSummaryEntity::class, SavingsAccountTransactionEntity::class,
        SavingsAccountTransactionRequestEntity::class, SavingsAccountTransactionTemplateEntity::class,
        SavingsAccountWithAssociationsEntity::class, SavingsTransactionDateEntity::class,
        SavingsTransactionTypeEntity::class,
        // Clients (13)
        ChargeCalculationTypeEntity::class, ChargesEntity::class, ChargeTimeTypeEntity::class,
        ClientAddressEntity::class, ClientChargeCurrencyEntity::class,
        ClientClassificationEntity::class, ClientDateEntity::class, ClientEntity::class,
        ClientGenderEntity::class, ClientIdentifierEntity::class, ClientPayloadEntity::class,
        ClientStatusEntity::class, ClientTypeEntity::class,
        // Groups (5)
        CenterDateEntity::class, CenterEntity::class, GroupDateEntity::class,
        GroupEntity::class, GroupPayloadEntity::class,
        // Organization (3)
        OfficeEntity::class, OfficeOpeningDateEntity::class, StaffEntity::class,
        // Center (1)
        CenterPayloadEntity::class,
        // Data Tables (1)
        DataTableEntity::class,
        // Notes (1)
        NoteEntity::class,
        // Survey (4)
        ComponentDatasEntity::class, QuestionDatasEntity::class,
        ResponseDatasEntity::class, SurveyEntity::class,
        // Templates (7)
        ClientsTemplateEntity::class, InterestTypeEntity::class, OfficeOptionsEntity::class,
        OptionsEntity::class, SavingProductOptionsEntity::class, StaffOptionsEntity::class,
        LoanRepaymentTemplateEntity::class,
        // Misc (1)
        PaymentTypeOptionEntity::class,
    ],
    version = MifosDatabase.VERSION,
    exportSchema = true,  // Changed from false → true (recommended for Room 3)
)
@TypeConverters(CustomTypeConverters::class)
@ConstructedBy(MifosDatabaseConstructor::class)
abstract class MifosDatabase : RoomDatabase() {
    abstract val centerDao: CenterDao
    abstract val chargeDao: ChargeDao
    abstract val clientDao: ClientDao
    abstract val columnValueDao: ColumnValueDao
    abstract val groupsDao: GroupsDao
    abstract val loanDao: LoanDao
    abstract val officeDao: OfficeDao
    abstract val savingsDao: SavingsDao
    abstract val staffDao: StaffDao
    abstract val surveyDao: SurveyDao

    companion object {
        const val VERSION = 1
        const val DATABASE_NAME = "mifos_database.db"
    }
}
```

### 3c. DELETE Platform-Specific Database Actuals

```bash
# Delete ALL platform AppDatabase/MifosDatabase actual files:
rm core/database/src/androidMain/kotlin/.../<YourDB>.kt         # or AppDatabase.android.kt
rm core/database/src/desktopMain/kotlin/.../<YourDB>.kt         # or AppDatabase.desktop.kt
rm core/database/src/nativeMain/kotlin/.../<YourDB>.kt          # or AppDatabase.native.kt
rm core/database/src/jsMain/kotlin/.../<YourDB>.js.kt           # stub
rm core/database/src/wasmJsMain/kotlin/.../<YourDB>.wasmJs.kt   # stub
```

> **WARNING**: Do NOT delete DI modules (`DatabaseModule.*.kt`) — only delete the database class files.

### 3d. Clean Up Verbose @Entity Annotations

All three projects have entities with verbose default parameters that should be simplified:

```kotlin
# BEFORE (all projects have this pattern):
@Entity(
    tableName = "charges",
    indices = [],
    inheritSuperIndices = false,
    primaryKeys = [],
    foreignKeys = [],
    ignoredColumns = [],
)

# AFTER:
@Entity(tableName = "charges")
```

Only keep non-default parameters (e.g., `foreignKeys = [...]` if actually used).

**field-officer**: Many entities DO have real `foreignKeys` — preserve those, only remove empty defaults.

---

## Step 4: Update DI Modules

### 4a. Android (`DatabaseModule.android.kt`)

```kotlin
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import kotlinx.coroutines.Dispatchers
import org.koin.android.ext.koin.androidApplication
import org.koin.core.module.Module
import org.koin.dsl.module
import template.core.base.database.AppDatabaseFactory

actual val platformModule: Module = module {
    single {
        AppDatabaseFactory(androidApplication())
            .createDatabase<<YourDB>>(
                databaseName = <YourDB>.DATABASE_NAME,
            )
            .fallbackToDestructiveMigrationOnDowngrade(false)
            .setDriver(BundledSQLiteDriver())
            .setQueryCoroutineContext(Dispatchers.IO)
            .build()
    }
}
```

**Key changes from current code**:
- `createDatabase(AppDatabase::class.java, name)` → `createDatabase<AppDatabase>(databaseName = name)` (reified, no Class param)
- `get(named(MifosDispatchers.IO.name))` → `Dispatchers.IO` (direct dispatcher, no Koin qualifier needed)
- `BundledSQLiteDriver()` is now **mandatory** (Room 3 has no implicit default)

### 4b. Desktop (`DatabaseModule.desktop.kt`)

```kotlin
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import kotlinx.coroutines.Dispatchers
import org.koin.core.module.Module
import org.koin.dsl.module
import template.core.base.database.AppDatabaseFactory

actual val platformModule: Module = module {
    single {
        AppDatabaseFactory()
            .createDatabase<<YourDB>>(
                databaseName = <YourDB>.DATABASE_NAME,
            )
            .fallbackToDestructiveMigrationOnDowngrade(false)
            .setDriver(BundledSQLiteDriver())
            .setQueryCoroutineContext(Dispatchers.IO)
            .build()
    }
}
```

### 4c. Native/iOS (`DatabaseModule.native.kt`)

```kotlin
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import kotlinx.coroutines.Dispatchers
import org.koin.core.module.Module
import org.koin.dsl.module
import template.core.base.database.AppDatabaseFactory

actual val platformModule: Module = module {
    single {
        AppDatabaseFactory()
            .createDatabase<<YourDB>>(
                databaseName = <YourDB>.DATABASE_NAME,
            )
            .fallbackToDestructiveMigrationOnDowngrade(false)
            .setDriver(BundledSQLiteDriver())
            .setQueryCoroutineContext(Dispatchers.Default)  // IO is internal on Native
            .build()
    }
}
```

> **CRITICAL**: Use `Dispatchers.Default` on Native — `Dispatchers.IO` is `internal` in Kotlin/Native.

### 4d. JS (`DatabaseModule.js.kt`) — NEW (was stub/TODO)

```kotlin
import kotlinx.coroutines.Dispatchers
import org.koin.core.module.Module
import org.koin.dsl.module
import template.core.base.database.AppDatabaseFactory

actual val platformModule: Module = module {
    single {
        AppDatabaseFactory()
            .createDatabase<<YourDB>>(
                databaseName = <YourDB>.DATABASE_NAME,
            )
            .setQueryCoroutineContext(Dispatchers.Default)
            .build()
    }
}
```

### 4e. WasmJS (`DatabaseModule.wasmJs.kt`) — NEW (was stub/TODO)

Same as JS above.

### Per-Project DI Notes

| Project | Current Pattern | Change Needed |
|---------|----------------|---------------|
| **mifos-mobile** | Uses `get(named(MifosDispatchers.IO.name))` | Replace with `Dispatchers.IO` directly |
| **field-officer** | Uses `get(named(MifosDispatchers.IO.name))` | Replace with `Dispatchers.IO` directly |
| **mifos-mobile** | Android uses `createDatabase(AppDatabase::class.java, name)` | Change to `createDatabase<AppDatabase>(databaseName = name)` |
| **All** | JS/WasmJS are `TODO("Not yet implemented")` | Replace with real implementations above |

---

## Step 5: Update `core/database/build.gradle.kts`

### 5a. Remove Redundant Room Dependencies

The convention plugin (`mifos.kmp.room`) now adds `room3-runtime` automatically. Remove duplicates:

```kotlin
# REMOVE these platform-specific Room deps (convention plugin handles them):
androidMain.dependencies {
    // REMOVE: implementation(libs.androidx.room.runtime)
    // REMOVE: implementation(libs.androidx.sqlite.bundled)
    implementation(libs.koin.android)  // KEEP
}

desktopMain.dependencies {
    // REMOVE: implementation(libs.androidx.room.runtime)
    // REMOVE: implementation(libs.androidx.sqlite.bundled)
}

nativeMain.dependencies {
    // REMOVE: implementation(libs.androidx.room.runtime)
    // REMOVE: implementation(libs.androidx.sqlite.bundled)
}
```

### 5b. Remove `room-ktx` References

```kotlin
# REMOVE any reference to room-ktx:
# implementation(libs.androidx.room.ktx)  ← DELETE
```

### 5c. Add Test Dependencies (if not present)

```kotlin
commonTest.dependencies {
    implementation(libs.kotlin.test)
    implementation(libs.kotlinx.coroutines.test)
    implementation(libs.turbine)      // for Flow testing
    implementation(libs.koin.test)    // for DI testing
}
```

### 5d. Remove `room.generateKotlin` KSP Arg

If your project's convention plugin had this (mifos-mobile and field-officer do):
```kotlin
// REMOVE from KMPRoomConventionPlugin.kt (synced, but verify):
// ksp { arg("room.generateKotlin", "true") }
// Room 3 ALWAYS generates Kotlin — this arg is removed.
```

---

## Step 6: Update Test Modules

### 6a. Update Existing Test DI Modules

Replace Room 2 in-memory builder with Room 3 context-free builder:

```kotlin
// BEFORE (Room 2):
Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
    .build()

// AFTER (Room 3 — context-free, reified):
Room.inMemoryDatabaseBuilder<AppDatabase>()
    .setDriver(BundledSQLiteDriver())
    .setQueryCoroutineContext(Dispatchers.IO)  // or Dispatchers.Default on Native
    .build()
```

### 6b. Update Test Imports

```bash
find core/database/src -path "*/test*" -name "*.kt" -exec sed -i '' \
  's/import androidx\.room\.Room/import androidx.room3.Room/g' {} +
```

### 6c. Create JS/WasmJS Test Modules (NEW)

```kotlin
// core/database/src/jsTest/kotlin/.../di/TestDatabaseModule.js.kt
actual val testPlatformModule: Module = module {
    factory<<YourDB>> {
        Room.inMemoryDatabaseBuilder<<YourDB>>()
            .setQueryCoroutineContext(Dispatchers.Default)
            .build()
    }
}

// core/database/src/wasmJsTest/kotlin/.../di/TestDatabaseModule.wasmJs.kt
// Same as JS
```

### Per-Project Test Notes

| Project | Test Status | Action |
|---------|------------|--------|
| **mifos-mobile** | Has test modules for Android/Desktop/Native | Update imports + builder API |
| **field-officer** | **No TestDatabaseModule** | Create test modules from scratch |
| **mobile-wallet** | No core/database | Skip |

---

## Step 7: ProGuard + Verification

### 7a. Update ProGuard Rules

Check `cmp-desktop/compose-desktop.pro` and any `proguard-rules.pro`:

```proguard
# BEFORE:
-keep class * extends androidx.room.RoomDatabase { <init>(); }

# AFTER:
-keep class * extends androidx.room3.RoomDatabase { <init>(); }
```

### 7b. Wire DatabaseModule (if not already wired)

Check `cmp-navigation/.../di/KoinModules.kt` — ensure `DatabaseModule` is in the module list:

```kotlin
import <your.package>.database.di.DatabaseModule

// Add to allModules list if missing:
val allModules = listOf(
    // ...
    DatabaseModule,
)
```

Also add `core:database` to `cmp-navigation/build.gradle.kts` and `cmp-web/build.gradle.kts`:
```kotlin
commonMain.dependencies {
    implementation(projects.core.database)
}
```

### 7c. Verification Checklist

Run ALL of these from the project root:

```bash
# Build all platforms:
./gradlew :core:database:build

# Run tests:
./gradlew :core:database:desktopTest

# Zero-match checks (ALL must return 0 results):
grep -r "template\.core\.base\.database\." core/database/     # old abstraction imports
grep -r "import androidx\.room\." core/database/ | grep -v room3  # old Room 2 imports
grep -r "findAndInstantiateDatabaseImpl" core/database/        # old desktop factory
grep -r "findDatabaseConstructorAndInitDatabaseImpl" core/     # old native factory
grep -r "room\.generateKotlin" build-logic/                    # old KSP arg
grep -r "room-ktx" gradle/libs.versions.toml                   # old ktx artifact
grep -r "AppDatabase::class\.java" core/database/              # old Class<T> factory API
grep -r "TODO.*Not yet implemented" core/database/             # remaining stubs
```

Room 3 reads Room 2 database files — **existing user data is preserved** with no schema migration needed.

---

## Per-Project Execution Checklist

### mobile-wallet (mifos-pay)

- [ ] Step 0: Run `sync-dirs.sh` (this project has NO Room convention plugin — sync creates it)
- [ ] Step 1: Update `libs.versions.toml` (Kotlin 2.2.21→2.3.20, KSP→2.3.6, Compose→1.10.3, Room→3.0.0-alpha03)
- [ ] Step 1c: Add `sqlite-web` entry
- [ ] Step 1d: Remove `room-ktx` entry
- [ ] Steps 2-6: **SKIP** — this project has no `core/database` module
- [ ] Step 7c: Build verification
- [ ] **Total effort**: ~30 minutes

### mifos-mobile

- [ ] Step 0: Run `sync-dirs.sh`
- [ ] Step 1: Update `libs.versions.toml` (Kotlin **2.1.20→2.3.20**, KSP **2.1.20-2.0.1→2.3.6**, Compose **1.8.2→1.10.3**, Room **2.7.2→3.0.0-alpha03**, SQLite **2.5.0-alpha12→2.6.2**)
- [ ] Step 2: Replace imports (2 DAOs, 2 entities, TypeConverters, 5 AppDatabase actuals, 4 DI modules)
- [ ] Step 3: Unify `AppDatabase` to commonMain (2 entities, 2 DAOs)
- [ ] Step 3c: Delete 5 platform actual files
- [ ] Step 3d: Clean up `ChargeEntity` and `MifosNotificationEntity` verbose annotations
- [ ] Step 4: Update 4 DI modules (Android, Desktop, Native + create JS, WasmJS)
- [ ] Step 4 note: Replace `get(named(MifosDispatchers.IO.name))` → `Dispatchers.IO`
- [ ] Step 4 note: Replace `createDatabase(AppDatabase::class.java, name)` → `createDatabase<AppDatabase>(databaseName = name)`
- [ ] Step 5: Remove redundant deps from `build.gradle.kts`
- [ ] Step 6: Update test modules + create JS/WasmJS tests
- [ ] Step 7: ProGuard + verification
- [ ] **Total effort**: ~2 hours

### field-officer (mifos-x-field-officer-app)

- [ ] Step 0: Run `sync-dirs.sh`
- [ ] Step 1: Update `libs.versions.toml` (Kotlin 2.2.21→2.3.20, KSP→2.3.6, Compose→1.10.3, Room 2.8.4→3.0.0-alpha03)
- [ ] Step 1 note: Update `room-paging` to `androidx.room3:room3-paging` if used
- [ ] Step 2: Replace imports (**56 entities, 10 DAOs, 100+ TypeConverter methods** — all use `template.core.base.database.*`)
- [ ] Step 3: Unify `MifosDatabase` to commonMain (**56 entities, 10 DAOs** — copy exact entity list from androidMain actual)
- [ ] Step 3 note: Change `exportSchema = false` → `exportSchema = true`
- [ ] Step 3c: Delete 5 platform actual files
- [ ] Step 3d: Clean up verbose @Entity annotations — BUT preserve real `foreignKeys` (many entities use CASCADE)
- [ ] Step 4: Update DI modules (same pattern as mifos-mobile)
- [ ] Step 4 note: Replace `get(named(MifosDispatchers.IO.name))` → `Dispatchers.IO`
- [ ] Step 5: Remove redundant deps
- [ ] Step 6: **Create TestDatabaseModule from scratch** (none exists currently) + JS/WasmJS test modules
- [ ] Step 7: ProGuard + verification
- [ ] Step 7 note: Blocking DAO queries (getClientsTemplate, getColumnValue, getAllTransactions) — Room 3 may warn; convert to `suspend` or `Flow` if compiler errors occur
- [ ] **Total effort**: ~3-4 hours (large entity count)

---

## Quick Reference

| What | Room 2 | Room 3 |
|------|--------|--------|
| Maven group | `androidx.room` | `androidx.room3` |
| Gradle plugin | `androidx.room` | `androidx.room3` |
| Package | `androidx.room.*` | `androidx.room3.*` |
| KSP targets | Android, Desktop, Native | + **JS, WasmJS** |
| `room-ktx` | Separate artifact | Merged into `room3-runtime` |
| `room.generateKotlin` KSP arg | Required for KMP | **Removed** (always Kotlin) |
| SQLiteDriver | Optional (Android default) | **Mandatory** on all platforms |
| `inMemoryDatabaseBuilder` | Needs `Context` on Android | Context-free (reified) |
| `@ConstructedBy` | Required only on Native | Still required (**commonMain** now) |
| `AppDatabaseFactory.createDatabase` | `Class<T>` param on Android | **Reified `<T>`** on all platforms |
| `findAndInstantiateDatabaseImpl` | Used on Desktop | **Removed** (KSP generates constructor) |
| `findDatabaseConstructorAndInitDatabaseImpl` | Used on Native | **Removed** (KSP generates constructor) |
| `Dispatchers.IO` on Native | Works | **Internal** — use `Dispatchers.Default` |
| Web support | Stub only (`TODO`) | Full (OPFS persistence via sqlite-web) |
| Data migration | N/A | **Automatic** — Room 3 reads Room 2 schema files |
