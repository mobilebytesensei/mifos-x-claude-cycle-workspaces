# PLAN-migration-field-officer-260501: Room 3 + Store 5 + Security Migration

| Field | Value |
|-------|-------|
| ID | migration-field-officer-260501 |
| Status | Draft |
| Priority | P1 |
| Scope | mifos-x-field-officer-app — full stack migration |
| Created | 2026-05-01 |
| Source Branch | development |
| Upstream Repo | `openMF/mifos-x-field-officer-app` |
| Fork Repo | `therajanmaurya/mifos-x-field-officer-app` |
| Workspace | `workspaces/mifos-x/mifos-x-field-officer-app/` |
| Source Path | `workspaces/mifos-x/mifos-x-field-officer-app/source/mifos-x-field-officer-app/` |
| Remote (origin) | `git@github.com:therajanmaurya/mifos-x-field-officer-app.git` (fork) |
| Remote (upstream) | `https://github.com/openMF/mifos-x-field-officer-app.git` (org) |
| Consumer Guide | `docs/CONSUMER_APP_MIGRATION_GUIDE.md` (in kmp-project-template) |

---

## Execution Rules (STRICT ENFORCEMENT)

> **MANDATORY**: Execute phases ONE BY ONE in order. Each phase has a GATE that MUST pass before proceeding.
> - Phase 0 (sync-dirs) MUST complete before Phase 1
> - Phase 1 (Gradle) MUST compile build-logic before Phase 2
> - Phase 2 (Security) MUST verify SecurityModule provides FieldEncryptor before Phase 3
> - Phase 3A-3E (Room 3) MUST pass KSP on all platforms before Phase 4
> - Phase 4 (DataStore) MUST verify dual-store reads/writes before Phase 5
> - Phase 5A (Store 5 high priority) before 5B (sync repos) before 5C (batch)
> - Phase 6 (DI) MUST verify Koin module order resolves without circular deps before Phase 7
> - Phase 7 (SecurityGate) MUST verify root composable wraps correctly before Phase 8
> - Phase 8 (Verification) = final gate before commit
>
> **NEVER skip a phase.** If a phase fails, fix it before moving forward.
> **NEVER edit core-base/ files** — they are synced from kmp-project-template via sync-dirs.

---

## Audit Summary

| Component | Current State | Target State | Gap |
|-----------|--------------|--------------|-----|
| Room | 2.8.4 | 3.0.0-alpha03 | Version + TypeConverter encryption |
| Store 5 | Not present | 5.1.0-alpha08 | Full adoption (60+ repositories) |
| Security | Not present | core-base/security | Module + DI wiring |
| DataStore | Single-store (plain) | Dual-store (plain + secure) | Split sensitive/non-sensitive |
| Kotlin | 2.2.21 | 2.3.20+ | Minor bump |
| Koin | 4.1.1 | 4.1.1 | Already current |
| Entities | **41+** (largest of all 3 apps) | 41+ with encrypted converters | Add encryption |
| DAOs | 10 | 10 (no change) | None |
| TypeConverters | **10 classes** (plain JSON) | 10 (encrypted JSON) | Add FieldEncryptor |
| SecurityGate | Not present | Root composable | Add wrapper |
| KMPRoomConventionPlugin | Exists | Update to Room 3 | Plugin update |
| Paging 3 | 3.4.0 | Keep (compatible with Store 5) | None |

### Critical Security Gaps

1. Auth token `base64EncodedAuthenticationKey` stored as plain base64 (not encrypted)
2. No encryption on any of 10 TypeConverter classes
3. No `core-base/security/` module
4. No `core-base/datastore/` module (datastore is directly in core/)

### Unique Complexity: Largest Database

This app has the **most complex database** of all 3 consumer apps:
- 41+ entities spanning loans, savings, clients, centers, groups, offices, staff, surveys, datatables
- 10 TypeConverter classes (each needs FieldEncryptor integration)
- 10 DAOs with complex queries
- 60+ repositories — largest Store 5 migration surface
- Uses Paging 3 (must remain compatible with Store 5)
- Offline-first sync repositories already exist (SyncClientPayloads, SyncLoanRepayment, etc.)

---

## Migration Tasks

### Phase 0 — sync-dirs (MANDATORY FIRST STEP)
> **CRITICAL**: core-base files are OWNED by kmp-project-template. NEVER edit core-base/ directly in consumer apps.
> sync-dirs delivers: core-base/security, core-base/store, core-base/database (Room 3 with `import androidx.room3.*`), core-base/datastore, updated build-logic.
> **STRICT ENFORCEMENT**: Do NOT proceed to Phase 1 until sync-dirs completes and all core-base modules verified.

| Task | Description | Blocking? | Verify |
|------|-------------|:---------:|--------|
| T0.1 | Run `./sync-dirs.sh` from source root | Yes | Script exits 0 |
| T0.2 | Verify core-base/security/ exists with SecurityModule, FieldEncryptor, SecureKeyProvider | Yes | `ls core-base/security/src` |
| T0.3 | Verify core-base/store/ exists with StoreFactory, StoreModule | Yes | `ls core-base/store/src` |
| T0.4 | Verify core-base/database/ uses `import androidx.room3.*` (NOT `import androidx.room.*`) | Yes | `grep -r "import androidx.room\." core-base/database/` returns empty |
| T0.5 | Verify core-base/datastore/ exists | Yes | `ls core-base/datastore/src` |
| T0.6 | Verify build-logic/convention/KMPRoomConventionPlugin uses `androidx.room3` | Yes | `grep "room3" build-logic/convention/src/main/kotlin/KMPRoomConventionPlugin.kt` |
| T0.7 | Commit sync changes to feature branch | Yes | `git diff --stat` shows only sync changes |

### Phase 1 — Gradle Setup
> **GATE**: Phase 0 must be COMPLETE. Verify `core-base/database` has `import androidx.room3.*` before proceeding.
> **NOTE**: KMPRoomConventionPlugin is delivered by sync-dirs. Do NOT edit it manually.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T1.1 | Update `gradle/libs.versions.toml`: room 2.8.4→3.0.0-alpha03 (`androidx.room3:room3-*`), add store 5.1.0-alpha08, bouncycastle, androidxSecurityCrypto, update room plugin ID to `androidx.room3` | `gradle/libs.versions.toml` | `grep "room3" gradle/libs.versions.toml` |
| T1.2 | Update `core/database/build.gradle.kts` — add `implementation(projects.coreBase.security)` | `core/database/build.gradle.kts` | `grep "coreBase.security" core/database/build.gradle.kts` |
| T1.3 | Add Store 5 dependency to `core/data/build.gradle.kts` | `core/data/build.gradle.kts` | `grep "store5" core/data/build.gradle.kts` |
| T1.4 | Add `core-base/datastore` dependency to `core/datastore/build.gradle.kts` | `core/datastore/build.gradle.kts` | `grep "coreBase.datastore" core/datastore/build.gradle.kts` |
| T1.5 | Register all core-base modules in `settings.gradle.kts` if not present | `settings.gradle.kts` | `grep "core-base" settings.gradle.kts` |

### Phase 2 — Security Module Wiring
> **GATE**: Phase 1 must compile build-logic (`./gradlew check -p build-logic`).

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T2.1 | Add `implementation(projects.coreBase.security)` to `cmp-navigation/build.gradle.kts` | `cmp-navigation/build.gradle.kts` | Gradle sync |
| T2.2 | Add `SecurityModule` as FIRST entry in `KoinModules.allModules` — SecurityModule provides: FieldEncryptor, SecureKeyProvider, SessionManager, BiometricAuthenticator, TamperDetector, SecureWiper, SecurityPolicy, SecureAuthManager, FailedAttemptTracker. It auto-includes `platformSecurityModule` (Android: Keystore-backed, iOS: Keychain, Desktop: OS credential API) | `cmp-navigation/.../di/KoinModules.kt` | `import template.core.base.security.di.SecurityModule` compiles |
| T2.3 | Add `implementation(projects.coreBase.security)` to `core/datastore/build.gradle.kts` | `core/datastore/build.gradle.kts` | Gradle sync |
| T2.4 | Add `implementation(projects.coreBase.security)` to `core/database/build.gradle.kts` | `core/database/build.gradle.kts` | Gradle sync |
| T2.5 | Verify: `./gradlew :cmp-navigation:compileDemoDebugKotlinAndroid` compiles with SecurityModule import | CI | Exit 0 |

### Phase 3 — Room 3 Database Migration (LARGEST PHASE)
> **GATE**: Phase 2 must verify SecurityModule compiles.
> **IMPORTANT**: Room 3 changed BOTH artifact coordinates (`androidx.room3:room3-*`) AND Kotlin package namespace (`import androidx.room3.*`).
> After Phase 0 sync-dirs, core-base/database typealiases already use `import androidx.room3.*`.
> Consumer code using `template.core.base.database.*` typealiases does NOT need import changes.
> Consumer code directly importing `import androidx.room.*` MUST change to `import androidx.room3.*`.
> 41+ entities, 10 DAOs, 10 TypeConverter classes — this is the LARGEST migration phase across all 3 apps.

#### 3A — Import Migration (batch)
| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3A.1 | Update all 41+ entities: `import androidx.room.*` → `import androidx.room3.*` (skip files using `template.core.base.database.*` typealiases) | `core/database/src/commonMain/.../entities/**/*.kt` | `grep -r "import androidx.room\." core/database/` returns 0 matches |
| T3A.2 | Update all 10 DAO imports | `core/database/src/commonMain/.../dao/*.kt` | Same grep check |
| T3A.3 | Update all 10 TypeConverter imports | `core/database/src/commonMain/.../typeconverters/*.kt` | Same grep check |
| T3A.4 | Update AppDatabase imports on ALL platforms | `core/database/src/{commonMain,androidMain,desktopMain,nativeMain}/.../MifosDatabase.kt` | Same grep check |

#### 3B — Database Class
| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.1 | Update `MifosDatabase`: add `@ConstructedBy(MifosDatabaseConstructor::class)` | `core/database/src/commonMain/.../MifosDatabase.kt` | Compiles |
| T3B.2 | Add `expect object MifosDatabaseConstructor : RoomDatabaseConstructor<MifosDatabase>` in commonMain | Same file | Compiles |
| T3B.3 | Remove Android-specific actual MifosDatabase (KSP auto-generates the constructor) | `core/database/src/androidMain/.../MifosDatabase.kt` | File removed |

**T3B.1-3B.2 implementation:**
```kotlin
import androidx.room3.Database
import androidx.room3.RoomDatabase
import androidx.room3.RoomDatabaseConstructor
import androidx.room3.ConstructedBy
import androidx.room3.TypeConverters

@Database(
    entities = [/* all 41+ existing entity classes */],
    version = 2,  // Bump from 1 — schema changed (encryption + Room 3)
    exportSchema = true,
)
@TypeConverters(
    CustomTypeConverters::class, ListTypeConverters::class, ClientTypeConverters::class,
    GroupTypeConverters::class, LoanTypeConverters::class, SavingsTypeConverters::class,
    CenterTypeConverters::class, ChargeTypeConverter::class, OfficeTypeConverters::class,
    SurveyTypeConverters::class, DueDateConverter::class,
)
@ConstructedBy(MifosDatabaseConstructor::class)
abstract class MifosDatabase : RoomDatabase() {
    abstract fun clientDao(): ClientDao
    abstract fun groupDao(): GroupDao
    abstract fun centerDao(): CenterDao
    abstract fun loanDao(): LoanDao
    abstract fun savingsAccountDao(): SavingsAccountDao
    abstract fun officeDao(): OfficeDao
    abstract fun staffDao(): StaffDao
    abstract fun surveyDao(): SurveyDao
    abstract fun chargeDao(): ChargeDao
    abstract fun datatableDao(): DatatableDao
    // ... all remaining DAOs

    companion object {
        const val DATABASE_NAME = "mifos_database"
    }
}

expect object MifosDatabaseConstructor : RoomDatabaseConstructor<MifosDatabase>
```

#### 3C — TypeConverter Encryption (10 classes)
> Each TypeConverter class gets the same FieldEncryptor pattern. ALL 10 must use `@kotlin.concurrent.Volatile` (NOT `@Volatile`).
> The `ENC:` prefix ensures backward compatibility — unencrypted legacy data is read as-is, new writes are encrypted.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3C.1 | Add `FieldEncryptor` companion + `install()` + encrypt/decrypt to `CustomTypeConverters` | `core/database/.../typeconverters/CustomTypeConverters.kt` | Compiles |

**T3C.1 implementation pattern (apply to ALL 10 TypeConverter classes):**
```kotlin
class CustomTypeConverters {
    companion object {
        @kotlin.concurrent.Volatile  // NOT @Volatile (iOS KSP fails with @Volatile)
        private var encryptor: FieldEncryptor? = null
        fun install(fieldEncryptor: FieldEncryptor) { encryptor = fieldEncryptor }
    }
    private fun encrypt(value: String): String {
        val enc = encryptor ?: return value
        return "ENC:${enc.encrypt(value)}"
    }
    private fun decrypt(value: String): String {
        val enc = encryptor ?: return value
        return if (value.startsWith("ENC:")) enc.decrypt(value.removePrefix("ENC:")) else value
    }
    // Wrap ALL existing @TypeConverter methods with encrypt/decrypt:
    @TypeConverter fun fromStringList(list: List<String>): String = encrypt(Json.encodeToString(list))
    @TypeConverter fun toStringList(json: String): List<String> = Json.decodeFromString(decrypt(json))
    // ... repeat for every existing converter method in this class
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3C.2 | Apply same pattern to `ListTypeConverters` | `.../typeconverters/ListTypeConverters.kt` | Compiles |
| T3C.3 | Apply same pattern to `ClientTypeConverters` | `.../typeconverters/ClientTypeConverters.kt` | Compiles |
| T3C.4 | Apply same pattern to `GroupTypeConverters` | `.../typeconverters/GroupTypeConverters.kt` | Compiles |
| T3C.5 | Apply same pattern to `LoanTypeConverters` | `.../typeconverters/LoanTypeConverters.kt` | Compiles |
| T3C.6 | Apply same pattern to `SavingsTypeConverters` | `.../typeconverters/SavingsTypeConverters.kt` | Compiles |
| T3C.7 | Apply same pattern to `CenterTypeConverters` | `.../typeconverters/CenterTypeConverters.kt` | Compiles |
| T3C.8 | Apply same pattern to `ChargeTypeConverter` | `.../typeconverters/ChargeTypeConverter.kt` | Compiles |
| T3C.9 | Apply same pattern to `OfficeTypeConverters` | `.../typeconverters/OfficeTypeConverters.kt` | Compiles |
| T3C.10 | Apply same pattern to `SurveyTypeConverters` | `.../typeconverters/SurveyTypeConverters.kt` | Compiles |
| T3C.11 | Apply same pattern to `DueDateConverter` | `.../typeconverters/DueDateConverter.kt` | Compiles |
| T3C.12 | Verify ALL 10 classes use `@kotlin.concurrent.Volatile` (NOT `@Volatile`) | All 10 files | `grep -r "@Volatile" core/database/src/commonMain/.../typeconverters/` returns 0 |

#### 3D — Platform DI
> Each platform's DatabaseModule must call `install()` on ALL TypeConverter classes BEFORE `build()`.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3D.1 | Update Android DatabaseModule: install ALL TypeConverters before `build()` | `core/database/src/androidMain/.../di/DatabaseModule.android.kt` | Compiles |

**T3D.1 implementation pattern (per platform):**
```kotlin
// In each platform's DatabaseModule:
single {
    val fieldEncryptor = get<FieldEncryptor>()
    // Install encryptor on ALL TypeConverter classes BEFORE build()
    CustomTypeConverters.install(fieldEncryptor)
    ListTypeConverters.install(fieldEncryptor)
    ClientTypeConverters.install(fieldEncryptor)
    GroupTypeConverters.install(fieldEncryptor)
    LoanTypeConverters.install(fieldEncryptor)
    SavingsTypeConverters.install(fieldEncryptor)
    CenterTypeConverters.install(fieldEncryptor)
    ChargeTypeConverter.install(fieldEncryptor)
    OfficeTypeConverters.install(fieldEncryptor)
    SurveyTypeConverters.install(fieldEncryptor)
    DueDateConverter.install(fieldEncryptor)

    AppDatabaseFactory(/* platform context */)
        .createDatabase<MifosDatabase>(MifosDatabase.DATABASE_NAME)
        .fallbackToDestructiveMigrationOnDowngrade(false)
        .setDriver(BundledSQLiteDriver())
        .setQueryCoroutineContext(get(named(MifosDispatchers.IO.name)))
        .build()
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3D.2 | Create/update Desktop DatabaseModule (same TypeConverter install pattern) | `core/database/src/desktopMain/.../di/DatabaseModule.desktop.kt` | Compiles |
| T3D.3 | Create/update Native DatabaseModule (same pattern) | `core/database/src/nativeMain/.../di/DatabaseModule.native.kt` | Compiles |
| T3D.4 | Create/update JS DatabaseModule (if applicable) | `core/database/src/jsMain/.../di/DatabaseModule.js.kt` | Compiles |
| T3D.5 | Create/update WasmJS DatabaseModule (if applicable) | `core/database/src/wasmJsMain/.../di/DatabaseModule.wasmJs.kt` | Compiles |

#### 3E — Verification
| Task | Description | Command | Verify |
|------|-------------|---------|--------|
| T3E.1 | KSP Android | `./gradlew :core:database:kspKotlinAndroid` | Exit 0 |
| T3E.2 | KSP iOS (critical — validates `@kotlin.concurrent.Volatile` on ALL 10 TypeConverter classes) | `./gradlew :core:database:kspKotlinIosArm64` | Exit 0 |
| T3E.3 | KSP Desktop | `./gradlew :core:database:kspKotlinDesktop` | Exit 0 |

### Phase 4 — DataStore Migration (Single → Dual-Store)
> **GATE**: Phase 3 must pass KSP verification on ALL platforms.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T4.1 | Add `implementation(projects.coreBase.datastore)` to `core/datastore/build.gradle.kts` | `core/datastore/build.gradle.kts` | Gradle sync |
| T4.2 | Update PreferencesModule to include `DatastoreBaseModule` and inject dual Settings: | `core/datastore/.../di/PreferencesModule.kt` | Compiles |

**T4.2 implementation:**
```kotlin
import template.core.base.datastore.di.DatastoreBaseModule

val PreferencesModule = module {
    includes(DatastoreBaseModule)  // Provides Settings(named("plain")) and Settings(named("secure"))
    factory {
        UserPreferencesDataSource(
            plainSettings = get(named("plain")),
            secureSettings = get(named("secure")),
            dispatcher = get(named(MifosDispatchers.IO.name)),
            fieldEncryptor = get(),  // From SecurityModule
        )
    }
    single<UserPreferencesRepository> {
        UserPreferencesRepositoryImpl(
            preferenceManager = get(),
            unconfinedDispatcher = get(named(MifosDispatchers.Unconfined.name)),
        )
    }
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T4.3 | Refactor `UserPreferencesDataSource` constructor to accept dual stores + FieldEncryptor: | `core/datastore/.../UserPreferencesDataSource.kt` | Compiles |

**T4.3 implementation:**
```kotlin
class UserPreferencesDataSource(
    private val plainSettings: Settings,    // UI prefs: theme, language, server URL
    private val secureSettings: Settings,   // Auth: base64EncodedAuthenticationKey, userId, staffId
    private val dispatcher: CoroutineDispatcher,
    private val fieldEncryptor: FieldEncryptor,
) {
    init {
        // Write-before-delete migration: move userData from plain to secure
        val plainUserData = plainSettings.decodeValueOrNull(key = USER_DATA, serializer = UserData.serializer())
        if (plainUserData != null) {
            secureSettings.encodeValue(key = USER_DATA, serializer = UserData.serializer(), value = plainUserData)
            plainSettings.remove(USER_DATA)
        }
    }
    private val _userInfo = MutableStateFlow(
        secureSettings.decodeValue(key = USER_DATA, serializer = UserData.serializer(), defaultValue = UserData.DEFAULT)
    )
    private val _settingsInfo = MutableStateFlow(
        plainSettings.decodeValue(key = APP_SETTINGS, serializer = AppSettings.serializer(), defaultValue = AppSettings.DEFAULT)
    )
    // All user/auth write methods → secureSettings.putUserPreference()
    // All settings write methods → plainSettings.putSettingsPreference()
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T4.4 | Verify dual-store: user data reads from secureSettings, app settings reads from plainSettings | Manual test | Both flows emit correctly |

### Phase 5 — Store 5 Adoption (Prioritized)
> **GATE**: Phase 4 must verify dual-store reads/writes.
> Store 5 uses `StoreFactory` from core-base/store. Each repository wraps its API service (Fetcher) + Room DAO (SourceOfTruth).
> 60+ repositories — prioritize high-value ones with existing offline sync patterns.
> Repos with existing DAOs use `createStore` (full offline cache). Repos without DAOs use `createMemoryStore`.
> Sync repos (offline writes) use `createMutableStore` with Bookkeeper.

#### 5A — High Priority (have existing DAOs = natural Store 5 candidates)

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5A.1 | Create `AppStoreModule` wrapping `StoreModule` from core-base/store: | NEW: `core/data/.../di/AppStoreModule.kt` | Compiles |

**T5A.1 implementation:**
```kotlin
import template.core.base.store.di.StoreModule

val AppStoreModule = module {
    includes(StoreModule)
    // Consumer-specific Store<Key, Output> instances go here
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5A.2 | `ClientListRepository` → Store 5 — this is the template pattern for all read-only repos: | `core/data/.../repository/ClientListRepositoryImpl.kt` | Compiles + unit test |

**T5A.2 implementation pattern (reuse for ALL read-only repositories with DAOs):**
```kotlin
import template.core.base.store.StoreFactory
import template.core.base.store.StoreData
import template.core.base.store.streamData
import org.mobilenativefoundation.store.store5.Fetcher
import org.mobilenativefoundation.store.store5.SourceOfTruth

class ClientListRepositoryImpl(
    private val apiService: ClientService,
    private val clientDao: ClientDao,
) : ClientListRepository {

    private val clientStore = StoreFactory.createStore(
        fetcher = Fetcher.of { officeId: Long ->
            apiService.getClientList(officeId)  // Network call → List<ClientDto>
        },
        sourceOfTruth = SourceOfTruth.of(
            reader = { officeId: Long ->
                clientDao.getClientsByOfficeId(officeId)  // Flow<List<ClientEntity>>
                    .map { entities -> entities.map { it.toDomain() } }
            },
            writer = { officeId: Long, clients: List<ClientDto> ->
                clientDao.insertAll(clients.map { it.toEntity(officeId) })
            },
            delete = { officeId: Long -> clientDao.deleteByOfficeId(officeId) },
            deleteAll = { clientDao.deleteAll() },
        ),
        validator = DefaultValidator.withTtl(30.minutes),
    )

    override fun getClientList(officeId: Long): Flow<StoreData<List<Client>>> =
        clientStore.streamData(key = officeId, refresh = true)

    override fun refreshClients(officeId: Long): Flow<StoreData<List<Client>>> =
        clientStore.freshData(key = officeId)
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5A.3 | `LoanAccountRepository` → Store 5 (same pattern) | Similar | Compiles |
| T5A.4 | `SavingsAccountRepository` → Store 5 | Similar | Compiles |
| T5A.5 | `CenterListRepository` → Store 5 | Similar | Compiles |
| T5A.6 | `GroupListRepository` → Store 5 | Similar | Compiles |

#### 5B — Sync Repositories (already have offline write patterns → MutableStore)
> These repos already implement offline-first write patterns (queue payloads locally, sync later).
> They map naturally to `StoreFactory.createMutableStore` with Bookkeeper for sync tracking.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5B.1 | `SyncClientPayloadsRepository` → MutableStore with Bookkeeper: | `core/data/.../repository/SyncClientPayloadsRepositoryImpl.kt` | Compiles |

**T5B.1 MutableStore pattern (for offline write repos):**
```kotlin
import template.core.base.store.StoreFactory
import template.core.base.store.StoreData
import org.mobilenativefoundation.store.store5.Fetcher
import org.mobilenativefoundation.store.store5.SourceOfTruth
import org.mobilenativefoundation.store.store5.Converter
import org.mobilenativefoundation.store.store5.Updater
import org.mobilenativefoundation.store.store5.Bookkeeper
import template.core.base.store.InMemoryBookkeeper

class SyncClientPayloadsRepositoryImpl(
    private val apiService: ClientPayloadService,
    private val payloadDao: ClientPayloadDao,
) : SyncClientPayloadsRepository {

    private val syncStore = StoreFactory.createMutableStore(
        fetcher = Fetcher.of { _: Unit ->
            payloadDao.getAllPendingPayloads()  // Read local pending payloads
        },
        sourceOfTruth = SourceOfTruth.of(
            reader = { _: Unit -> payloadDao.getAllPendingPayloadsFlow() },
            writer = { _: Unit, payloads: List<ClientPayload> ->
                payloadDao.insertAll(payloads.map { it.toEntity() })
            },
            delete = { _: Unit -> payloadDao.deleteAll() },
            deleteAll = { payloadDao.deleteAll() },
        ),
        converter = Converter.Builder<List<ClientPayload>, List<ClientPayload>, List<ClientPayload>>()
            .fromNetworkToLocal { it }
            .fromOutputToLocal { it }
            .build(),
        updater = Updater.by(
            post = { _: Unit, payloads: List<ClientPayload> ->
                // Push each payload to server, mark as synced
                payloads.forEach { payload ->
                    apiService.createClient(payload.toDto())
                    payloadDao.markSynced(payload.id)
                }
                UpdaterResult.Success.Typed(payloads)
            },
        ),
        bookkeeper = InMemoryBookkeeper(),
    )

    override fun syncPayloads(): Flow<StoreData<List<ClientPayload>>> =
        syncStore.streamData(key = Unit, refresh = true)
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5B.2 | `SyncLoanRepaymentTransactionRepository` → MutableStore (same pattern) | Similar | Compiles |
| T5B.3 | `SyncSavingsAccountTransactionRepository` → MutableStore | Similar | Compiles |
| T5B.4 | `SyncCenterPayloadsRepository` → MutableStore | Similar | Compiles |
| T5B.5 | `SyncGroupPayloadsRepository` → MutableStore | Similar | Compiles |

#### 5C — Remaining (batch — lower priority, can be incremental)

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5C.1 | For repos WITHOUT a local DAO (memory-only caching): | Various | Compiles |

**T5C.1 memory-only pattern (for repos without a local DAO):**
```kotlin
private val officeStore = StoreFactory.createMemoryStore(
    fetcher = Fetcher.of { _: Unit -> apiService.getOfficeList().map { it.toDomain() } }
)
override fun getOfficeList(): Flow<StoreData<List<Office>>> =
    officeStore.streamData(key = Unit, refresh = true)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5C.2 | Batch remaining ~45 repositories. Use `createMemoryStore` for repos without DAOs, `createStore` for repos with DAOs, `createMutableStore` for repos with offline write patterns | All remaining repos | Each compiles |
| T5C.3 | Update ViewModel consumers: change `Flow<T>` to `Flow<StoreData<T>>`, use `.data` to unwrap, use `.origin` for cache indicators, use `.isRefreshing` for loading state | Feature ViewModels consuming updated repos | UI works |
| T5C.4 | Add `AppStoreModule` to `KoinModules.allModules` (after DatabaseModule, before featureModules) | `cmp-navigation/.../di/KoinModules.kt` | Koin resolves |

### Phase 6 — DI Wiring (Final Order)
> **GATE**: Phase 5 must verify at least one Store compiles and returns data.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T6.1 | Enforce final module order in `KoinModules.allModules`: | `cmp-navigation/.../di/KoinModules.kt` | App starts without Koin errors |

**T6.1 exact order:**
```kotlin
val allModules = listOf(
    SecurityModule,        // 1. Security first — provides FieldEncryptor for all downstream
    databaseModules,       // 2. Database — needs FieldEncryptor for TypeConverter.install()
    commonModules,         // 3. Dispatchers
    coreDataStoreModules,  // 4. Datastore — includes DatastoreBaseModule, needs FieldEncryptor
    networkModules,        // 5. Network — API services
    AppStoreModule,        // 6. Store — needs API services + DAOs
    domainModule,          // 7. Domain use cases
    dataModules,           // 8. Repositories — may use Store instances
    featureModules,        // 9. Features — ViewModels consuming repositories
    sharedModule,          // 10. Navigation ViewModels
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T6.2 | Remove duplicate dispatcher modules if any exist | Same file | No duplicate Koin bindings |

### Phase 7 — SecurityGate
> **GATE**: Phase 6 must verify app starts without Koin errors.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T7.1 | Wrap root App composable with `SecurityGate { ... }` — the SecurityGate composable auto-wires: tamper detection at startup, session timeout check on app resume, session touch on pointer input, biometric re-auth on session expiry. It provides `LocalSecurityState` to the composable tree. | `cmp-navigation/.../ComposeApp.kt` | App starts with SecurityGate wrapping |

**T7.1 implementation:**
```kotlin
import template.core.base.security.SecurityGate

@Composable
fun ComposeApp(...) {
    // ... state collection, theme detection ...
    SecurityGate {
        MifosFieldOfficerTheme(darkTheme = uiState.darkTheme, ...) {
            Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.surface)) {
                Column(modifier = modifier.fillMaxSize().statusBarsPadding()) {
                    NetworkBanner(bannerState = uiState.networkBanner)
                    RootNavScreen(onSplashScreenRemoved = onSplashScreenRemoved)
                }
            }
        }
    }
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T7.2 | Override `SecurityPolicy` in DI for field officer context (LONGER timeout — field officers work in remote areas with intermittent connectivity): | DI override in KoinModules | Policy applied |

**T7.2 implementation:**
```kotlin
// In sharedModule or a securityOverrideModule:
single { SecurityPolicy(sessionTimeoutMinutes = 60, requireBiometricForSensitiveOps = false) }
// Field officers need longer sessions — 60 min timeout (vs 30 min default)
// Biometric not required (many field devices lack biometric hardware)
```

### Phase 8 — Verification
> **GATE**: Phase 7 must verify SecurityGate wraps the app correctly.

| Task | Description | Command | Verify |
|------|-------------|---------|--------|
| T8.1 | Build demo debug APK | `./gradlew :cmp-android:assembleDemoDebug` | Exit 0 |
| T8.2 | Static analysis | `./gradlew spotlessCheck detekt` | Exit 0 |
| T8.3 | iOS KSP (verifies `@kotlin.concurrent.Volatile` on ALL 10 TypeConverter classes) | `./gradlew :core:database:kspKotlinIosArm64` | Exit 0 |
| T8.4 | iOS framework link | `./gradlew :cmp-shared:linkDebugFrameworkIosArm64` | Exit 0 |
| T8.5 | Desktop build | `./gradlew :cmp-desktop:jar` | Exit 0 |
| T8.6 | Encryption roundtrip test: encrypt a TypeConverter value in ALL 10 classes, read it back, verify `ENC:` prefix and correct decryption | Manual test or unit test | Values match for all 10 |
| T8.7 | DataStore migration test: verify existing users' plain-stored userData migrates to secure store on first launch | Manual test | Init block runs migration |
| T8.8 | Store 5 test: verify at least one read-only Store returns `StoreData` with `origin = NETWORK` on fresh fetch, `origin = CACHE` on subsequent reads | Manual or unit test | Origins correct |
| T8.9 | MutableStore test: verify at least one sync Store successfully pushes a payload via Updater | Manual or unit test | Payload synced |
| T8.10 | Paging 3 compatibility: verify ClientListRepository with Store 5 + Paging still loads pages correctly | Manual test | Pages load |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| 41+ entities — Room 2→3 import migration | High | Batch with find-replace, verify KSP per platform |
| 10 TypeConverter classes need encryption | High | Template pattern from ChargeTypeConverters, apply to all 10 |
| 60+ repositories — Store 5 surface area | Very High | Prioritize sync repos (already have offline patterns), batch rest |
| Paging 3 + Store 5 compatibility | Medium | Store 5 supports Paging integration via `StoreMulticast` |
| Offline sync repos → MutableStore migration | High | Existing bookkeeping logic maps to Store 5 Bookkeeper |
| Schema migration (existing data) | Medium | `fallbackToDestructiveMigration(true)` for alpha, proper migrations for prod |

## Estimated Effort

| Phase | Effort |
|-------|--------|
| Phase 0 (sync-dirs) | 15 min |
| Phase 1 (Gradle) | 30 min |
| Phase 2 (Security) | 15 min |
| Phase 3 (Room 3 — 41+ entities, 10 converters) | 4-6 hours |
| Phase 4 (DataStore) | 1 hour |
| Phase 5A (Store 5 — high priority, 6 repos) | 2-3 hours |
| Phase 5B (Store 5 — sync repos, 5 MutableStores) | 2-3 hours |
| Phase 5C (Store 5 — remaining 45 repos, batch) | 4-6 hours |
| Phase 6 (DI) | 15 min |
| Phase 7 (SecurityGate) | 15 min |
| Phase 8 (Verification) | 1 hour |
| **Total** | **~16-22 hours** |

**This is the LARGEST migration** of all 3 consumer apps due to 41+ entities and 60+ repositories.

---

## Session Strategy

Execute in a **dedicated session** per phase group:
- **Session 1**: Phase 0-2 (infrastructure + security)
- **Session 2**: Phase 3A-3B (Room 3 imports + database class)
- **Session 3**: Phase 3C-3E (TypeConverter encryption — 10 classes + verification)
- **Session 4**: Phase 4 (DataStore)
- **Session 5**: Phase 5A-5B (Store 5 — high priority + sync repos)
- **Session 6**: Phase 5C + Phase 6-8 (remaining repos + DI + SecurityGate + verification)

---

## Cross-App Migration Order Recommendation

Execute migrations in this order across all 3 consumer apps:

```
1. mifos-mobile        (SMALLEST: 2 entities, 17 repos → ~6-8 hours)
   ↓ learnings feed into...
2. mobile-wallet       (MEDIUM: 0 entities greenfield, 24 repos → ~10-12 hours)
   ↓ patterns established...
3. field-officer-app   (LARGEST: 41+ entities, 60+ repos → ~16-22 hours)
```

Start with mifos-mobile as the **pilot migration** — smallest surface area, fastest feedback loop. Apply lessons learned to the larger apps.
