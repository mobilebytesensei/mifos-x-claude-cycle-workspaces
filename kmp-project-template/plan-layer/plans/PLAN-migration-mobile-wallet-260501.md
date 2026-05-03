# PLAN-migration-mobile-wallet-260501: Room 3 + Store 5 + Security Migration

| Field | Value |
|-------|-------|
| ID | migration-mobile-wallet-260501 |
| Status | Draft |
| Priority | P1 |
| Scope | mobile-wallet (mifos-pay) — full stack migration |
| Created | 2026-05-01 |
| Source Branch | development |
| Upstream Repo | `openMF/mifos-pay` |
| Fork Repo | `therajanmaurya/mifos-pay` |
| Workspace | `workspaces/mifos-x/mobile-wallet/` |
| Source Path | `workspaces/mifos-x/mobile-wallet/source/mobile-wallet/` |
| Remote (origin) | `git@github.com:therajanmaurya/mifos-pay.git` (fork) |
| Remote (upstream) | `git@github.com:openMF/mifos-pay.git` (org) |
| Remote (mbs) | `git@github.com:mobilebytesensei/mifos-pay.git` (team) |
| Consumer Guide | `docs/CONSUMER_APP_MIGRATION_GUIDE.md` (in kmp-project-template) |

---

## Execution Rules (STRICT ENFORCEMENT)

> **MANDATORY**: Execute phases ONE BY ONE in order. Each phase has a GATE that MUST pass before proceeding.
> - Phase 0 (sync-dirs) MUST complete before Phase 1
> - Phase 1 (Gradle) MUST compile build-logic before Phase 2
> - Phase 2 (Security) MUST verify SecurityModule provides FieldEncryptor before Phase 3
> - Phase 3 (Room 3) MUST pass KSP on all platforms before Phase 4
> - Phase 4 (DataStore) MUST verify dual-store reads/writes before Phase 5
> - Phase 5 (Store 5) MUST verify at least one Store compiles before Phase 6
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
| Room | 2.8.4 (abstractions only, no entities) | 3.0.0-alpha03 | Version + entity creation |
| Store 5 | Not present | 5.1.0-alpha08 | Full adoption (24 repositories) |
| Security | Not present | core-base/security | Module + DI wiring |
| DataStore | Mixed: KMP UserPreferencesDataSource + legacy Android PreferencesHelper | Dual-store (plain + secure) | Consolidate + encrypt |
| Kotlin | 2.2.21 | 2.3.20+ | Minor bump |
| Koin | 4.1.1 | 4.1.1 | Already current |
| Entities | 0 (no Room entities defined) | App-specific entities | Create from scratch |
| DAOs | 0 | App-specific DAOs | Create from scratch |
| TypeConverters | Base annotations only | Encrypted converters | Create with FieldEncryptor |
| SecurityGate | Not present | Root composable | Add wrapper |
| KMPRoomConventionPlugin | NOT present | Create/sync from template | Sync via sync-dirs |

### Critical Security Gaps

1. `base64EncodedAuthenticationKey` stored in plain SharedPreferences (base64 = encoding, not encryption)
2. Legacy `PreferencesHelper.kt` stores tokens, email, user ID unencrypted
3. Multiple datastores with no unified encryption strategy
4. No `core-base/security/` module

### Unique Complexity: No Existing Room Entities

Unlike mifos-mobile and field-officer-app, mobile-wallet has **zero Room entities**. The database layer is infrastructure-only (core-base/database has abstractions). This means:
- Room 3 migration is actually **greenfield** — create entities/DAOs fresh
- Decision: Which data from the 24 repositories should be cached locally?
- Lower risk (no migration of existing data) but higher design effort

---

## Migration Tasks

### Phase 0 — sync-dirs (MANDATORY FIRST STEP)
> **CRITICAL**: core-base files are OWNED by kmp-project-template. NEVER edit core-base/ directly in consumer apps.
> sync-dirs delivers: core-base/security, core-base/store, core-base/database (Room 3 with `import androidx.room3.*`), updated build-logic (KMPRoomConventionPlugin, MifosGitHooksConventionPlugin).
> **STRICT ENFORCEMENT**: Do NOT proceed to Phase 1 until sync-dirs completes and all core-base modules verified.

| Task | Description | Blocking? | Verify |
|------|-------------|:---------:|--------|
| T0.1 | Run `./sync-dirs.sh` from source root | Yes | Script exits 0 |
| T0.2 | Verify core-base/security/ exists with SecurityModule, FieldEncryptor, SecureKeyProvider | Yes | `ls core-base/security/src` |
| T0.3 | Verify core-base/store/ exists with StoreFactory, StoreModule | Yes | `ls core-base/store/src` |
| T0.4 | Verify core-base/database/ uses `import androidx.room3.*` (NOT `import androidx.room.*`) | Yes | `grep -r "import androidx.room\." core-base/database/` returns empty |
| T0.5 | Verify build-logic/convention/KMPRoomConventionPlugin uses `androidx.room3` | Yes | `grep "room3" build-logic/convention/src/main/kotlin/KMPRoomConventionPlugin.kt` |
| T0.6 | Commit sync changes to feature branch | Yes | `git diff --stat` shows only sync changes |

### Phase 1 — Gradle Setup
> **GATE**: Phase 0 must be COMPLETE. Verify `core-base/database` has `import androidx.room3.*` before proceeding.
> **NOTE**: KMPRoomConventionPlugin is delivered by sync-dirs. Do NOT edit it manually.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T1.1 | Update `gradle/libs.versions.toml`: room 2.8.4→3.0.0-alpha03 (`androidx.room3:room3-*`), add store 5.1.0-alpha08, bouncycastle, androidxSecurityCrypto, update room plugin ID to `androidx.room3` | `gradle/libs.versions.toml` | `grep "room3" gradle/libs.versions.toml` |
| T1.2 | Create `core/database/build.gradle.kts` with `mifos.kmp.room` plugin, security dependency | NEW: `core/database/build.gradle.kts` | File exists |
| T1.3 | Register `core/database`, `core-base:security`, `core-base:store` in `settings.gradle.kts` | `settings.gradle.kts` | `grep "core-base:security" settings.gradle.kts` |
| T1.4 | Add Store 5 dependency to `core/data/build.gradle.kts` | `core/data/build.gradle.kts` | `grep "store5" core/data/build.gradle.kts` |

### Phase 2 — Security Module Wiring
> **GATE**: Phase 1 must compile build-logic (`./gradlew check -p build-logic`).

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T2.1 | Add `implementation(projects.coreBase.security)` to `cmp-shared/build.gradle.kts` (or `cmp-navigation` if separate) | `cmp-shared/build.gradle.kts` | Gradle sync |
| T2.2 | Add `SecurityModule` as FIRST entry in `KoinModules.allModules` — SecurityModule provides: FieldEncryptor, SecureKeyProvider, SessionManager, BiometricAuthenticator, TamperDetector, SecureWiper, SecurityPolicy, SecureAuthManager, FailedAttemptTracker. It auto-includes `platformSecurityModule` (Android: Keystore-backed, iOS: Keychain, Desktop: OS credential API) | `cmp-shared/.../di/KoinModules.kt` | `import template.core.base.security.di.SecurityModule` compiles |
| T2.3 | Add `implementation(projects.coreBase.security)` to `core/datastore/build.gradle.kts` | `core/datastore/build.gradle.kts` | Gradle sync |
| T2.4 | Add `implementation(projects.coreBase.security)` to `core/database/build.gradle.kts` | `core/database/build.gradle.kts` | Gradle sync |
| T2.5 | Deprecate `PreferencesHelper.kt` (Android legacy) — mark @Deprecated, plan removal | `core/datastore/src/androidMain/.../PreferencesHelper.kt` | Annotation added |
| T2.6 | Verify: `./gradlew :cmp-shared:compileDemoDebugKotlinAndroid` compiles with SecurityModule import | CI | Exit 0 |

### Phase 3 — Room 3 Database (Greenfield)
> **GATE**: Phase 2 must verify SecurityModule compiles.
> **IMPORTANT**: Room 3 changed BOTH artifact coordinates (`androidx.room3:room3-*`) AND Kotlin package namespace (`import androidx.room3.*`).
> After Phase 0 sync-dirs, core-base/database typealiases already use `import androidx.room3.*`.
> Unlike other apps, mobile-wallet has **zero existing entities** — this is greenfield creation.
> Use `template.core.base.database.*` typealiases (recommended for portability across Room versions).

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3.1 | Design entity model — identify cacheable data from 24 repositories. Recommended entities: `AccountEntity`, `BeneficiaryEntity`, `SavingsAccountEntity`, `InvoiceEntity`, `TransactionHistoryEntity`, `RecentPayeeEntity` | Design decision | Document entities + fields |
| T3.2 | Create entities using `template.core.base.database.*` typealiases | NEW: `core/database/src/commonMain/.../entity/*.kt` | KSP compiles |

**T3.2 entity pattern (repeat for each entity):**
```kotlin
import template.core.base.database.ColumnInfo
import template.core.base.database.Entity
import template.core.base.database.PrimaryKey

@Entity(tableName = "accounts")
data class AccountEntity(
    @PrimaryKey val accountId: Long,
    @ColumnInfo(name = "account_no") val accountNo: String,
    @ColumnInfo(name = "product_name") val productName: String,
    @ColumnInfo(name = "account_balance") val accountBalance: Double,
    @ColumnInfo(name = "account_type") val accountType: String,
    @ColumnInfo(name = "status") val status: String,
    @ColumnInfo(name = "client_id") val clientId: Long,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3.3 | Create DAOs using typealiases | NEW: `core/database/src/commonMain/.../dao/*.kt` | KSP compiles |

**T3.3 DAO pattern:**
```kotlin
import template.core.base.database.Dao
import template.core.base.database.Insert
import template.core.base.database.OnConflictStrategy
import template.core.base.database.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface AccountDao {
    @Query("SELECT * FROM accounts WHERE client_id = :clientId")
    fun getAccountsByClientId(clientId: Long): Flow<List<AccountEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(accounts: List<AccountEntity>)

    @Query("DELETE FROM accounts WHERE client_id = :clientId")
    suspend fun deleteByClientId(clientId: Long)

    @Query("DELETE FROM accounts")
    suspend fun deleteAll()
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3.4 | Create `WalletDatabase` with `@ConstructedBy`, `@TypeConverters` | NEW: `core/database/src/commonMain/.../WalletDatabase.kt` | File exists |

**T3.4 implementation:**
```kotlin
import androidx.room3.Database
import androidx.room3.RoomDatabase
import androidx.room3.RoomDatabaseConstructor
import androidx.room3.ConstructedBy
import androidx.room3.TypeConverters

@Database(
    entities = [AccountEntity::class, BeneficiaryEntity::class, SavingsAccountEntity::class,
                InvoiceEntity::class, TransactionHistoryEntity::class, RecentPayeeEntity::class],
    version = 1,
    exportSchema = true,
)
@TypeConverters(WalletTypeConverters::class)
@ConstructedBy(WalletDatabaseConstructor::class)
abstract class WalletDatabase : RoomDatabase() {
    abstract fun accountDao(): AccountDao
    abstract fun beneficiaryDao(): BeneficiaryDao
    abstract fun savingsAccountDao(): SavingsAccountDao
    abstract fun invoiceDao(): InvoiceDao
    abstract fun transactionHistoryDao(): TransactionHistoryDao
    abstract fun recentPayeeDao(): RecentPayeeDao

    companion object {
        const val DATABASE_NAME = "wallet_database"
    }
}

expect object WalletDatabaseConstructor : RoomDatabaseConstructor<WalletDatabase>
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3.5 | Create encrypted TypeConverters with exact pattern: | NEW: `core/database/src/commonMain/.../utils/WalletTypeConverters.kt` | Compiles |

**T3.5 implementation:**
```kotlin
class WalletTypeConverters {
    companion object {
        @kotlin.concurrent.Volatile  // NOT @Volatile (iOS KSP fails)
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
    @TypeConverter fun fromStringList(list: List<String>): String = encrypt(Json.encodeToString(list))
    @TypeConverter fun toStringList(json: String): List<String> = Json.decodeFromString(decrypt(json))
    // ... repeat for all converter methods needed by entities
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3.6 | Create platform DatabaseModule DI — call `WalletTypeConverters.install(get<FieldEncryptor>())` BEFORE `WalletDatabase.build()`: | NEW: `core/database/src/*/di/DatabaseModule.*.kt` | Files exist |

**T3.6 implementation pattern (per platform):**
```kotlin
// In each platform's DatabaseModule:
single {
    WalletTypeConverters.install(get<FieldEncryptor>())  // MUST be before build()
    AppDatabaseFactory(/* platform context */)
        .createDatabase<WalletDatabase>(WalletDatabase.DATABASE_NAME)
        .fallbackToDestructiveMigrationOnDowngrade(false)
        .setDriver(BundledSQLiteDriver())
        .setQueryCoroutineContext(get(named(MifosDispatchers.IO.name)))
        .build()
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3.7 | Create common DatabaseModule exposing DAO singletons | NEW: `core/database/src/commonMain/.../di/DatabaseModule.kt` | File exists |

**T3.7 implementation:**
```kotlin
val DatabaseModule = module {
    includes(platformDatabaseModule)  // Platform-specific WalletDatabase creation
    single { get<WalletDatabase>().accountDao() }
    single { get<WalletDatabase>().beneficiaryDao() }
    single { get<WalletDatabase>().savingsAccountDao() }
    single { get<WalletDatabase>().invoiceDao() }
    single { get<WalletDatabase>().transactionHistoryDao() }
    single { get<WalletDatabase>().recentPayeeDao() }
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3.8 | Verify KSP on ALL platforms | CI | `./gradlew :core:database:kspKotlinIosArm64` exits 0 |

### Phase 4 — DataStore Migration (Consolidate + Encrypt)
> **GATE**: Phase 3 must pass KSP verification.

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
    private val plainSettings: Settings,    // UI prefs: theme, language, server instance
    private val secureSettings: Settings,   // Auth: base64EncodedAuthenticationKey, userId, roles, permissions
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
| T4.4 | Migrate PreferencesHelper callers to UserPreferencesRepository (Android-specific) — find all files importing PreferencesHelper, replace with UserPreferencesRepository injection | Feature modules using PreferencesHelper | `grep -r "PreferencesHelper" feature/` returns 0 |
| T4.5 | Verify dual-store: user data reads from secureSettings, app settings reads from plainSettings | Manual test | Both flows emit correctly |

### Phase 5 — Store 5 Adoption
> **GATE**: Phase 4 must verify dual-store reads/writes.
> Store 5 uses `StoreFactory` from core-base/store. Each repository wraps its API service (Fetcher) + Room DAO (SourceOfTruth).
> The repository returns `Flow<StoreData<T>>` instead of raw `Flow<T>`, giving consumers origin/freshness metadata.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5.1 | Create `AppStoreModule` wrapping `StoreModule` from core-base/store: | NEW: `core/data/.../di/AppStoreModule.kt` | Compiles |

**T5.1 implementation:**
```kotlin
import template.core.base.store.di.StoreModule

val AppStoreModule = module {
    includes(StoreModule)
    // Consumer-specific Store<Key, Output> instances go here
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5.2 | Wrap `AccountRepository` with Store 5 — this is the template pattern for all repos: | `core/data/.../repository/AccountRepositoryImpl.kt` | Compiles + unit test |

**T5.2 implementation pattern (reuse for ALL repositories):**
```kotlin
import template.core.base.store.StoreFactory
import template.core.base.store.StoreData
import template.core.base.store.streamData
import org.mobilenativefoundation.store.store5.Fetcher
import org.mobilenativefoundation.store.store5.SourceOfTruth

class AccountRepositoryImpl(
    private val apiService: AccountService,
    private val accountDao: AccountDao,
) : AccountRepository {

    private val accountStore = StoreFactory.createStore(
        fetcher = Fetcher.of { clientId: Long ->
            apiService.getAccounts(clientId)  // Network call → List<AccountDto>
        },
        sourceOfTruth = SourceOfTruth.of(
            reader = { clientId: Long ->
                accountDao.getAccountsByClientId(clientId)  // Flow<List<AccountEntity>>
                    .map { entities -> entities.map { it.toDomain() } }
            },
            writer = { clientId: Long, accounts: List<AccountDto> ->
                accountDao.insertAll(accounts.map { it.toEntity(clientId) })
            },
            delete = { clientId: Long -> accountDao.deleteByClientId(clientId) },
            deleteAll = { accountDao.deleteAll() },
        ),
        validator = DefaultValidator.withTtl(30.minutes),
    )

    override fun getAccounts(clientId: Long): Flow<StoreData<List<Account>>> =
        accountStore.streamData(key = clientId, refresh = true)

    override fun refreshAccounts(clientId: Long): Flow<StoreData<List<Account>>> =
        accountStore.freshData(key = clientId)
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5.3 | Wrap `BeneficiaryRepository` with Store 5 (same pattern, Fetcher = beneficiary API, SourceOfTruth = BeneficiaryDao) | `core/data/.../repository/BeneficiaryRepositoryImpl.kt` | Compiles |
| T5.4 | Wrap `SavingsAccountRepository` with Store 5 | Similar | Compiles |
| T5.5 | Wrap `InvoiceRepository` with Store 5 | Similar | Compiles |
| T5.6 | Wrap `HistoryRepository`/`RecentPayeeRepository` with Store 5 | Similar | Compiles |
| T5.7 | For repos WITHOUT a local DAO (memory-only caching): | Similar | Compiles |

**T5.7 memory-only pattern (for repos without a local DAO):**
```kotlin
private val transferStore = StoreFactory.createMemoryStore(
    fetcher = Fetcher.of { accountId: Long -> apiService.getTransferTemplate(accountId).toDomain() }
)
override fun getTransferTemplate(accountId: Long): Flow<StoreData<TransferTemplate>> =
    transferStore.streamData(key = accountId, refresh = true)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5.8 | Batch remaining ~18 repositories (lower priority — can be incremental). Use `createMemoryStore` for repos without DAOs, `createStore` for repos with DAOs | All remaining repos | Each compiles |
| T5.9 | Update ViewModel consumers: change `Flow<T>` to `Flow<StoreData<T>>`, use `.data` to unwrap, use `.origin` for cache indicators, use `.isRefreshing` for loading state | Feature ViewModels consuming updated repos | UI works |
| T5.10 | Add `AppStoreModule` to `KoinModules.allModules` (after DatabaseModule, before featureModules) | `cmp-shared/.../di/KoinModules.kt` | Koin resolves |

### Phase 6 — DI Wiring (Final Order)
> **GATE**: Phase 5 must verify at least one Store compiles and returns data.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T6.1 | Enforce final module order in `KoinModules.allModules`: | `cmp-shared/.../di/KoinModules.kt` | App starts without Koin errors |

**T6.1 exact order:**
```kotlin
val allModules = listOf(
    SecurityModule,        // 1. Security first — provides FieldEncryptor for all downstream
    DatabaseModule,        // 2. Database — needs FieldEncryptor for TypeConverter.install()
    commonModules,         // 3. Dispatchers
    coreDataStoreModules,  // 4. Datastore — includes DatastoreBaseModule, needs FieldEncryptor
    networkModules,        // 5. Network — API services
    AppStoreModule,        // 6. Store — needs API services + DAOs
    dataModules,           // 7. Repositories — may use Store instances
    domainModules,         // 8. Domain use cases
    featureModules,        // 9. Features — ViewModels consuming repositories
    sharedModule,          // 10. Navigation ViewModels
    LibraryModule,         // 11. Libraries (passcode, etc.)
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T6.2 | Remove duplicate dispatcher modules if any exist | Same file | No duplicate Koin bindings |

### Phase 7 — SecurityGate
> **GATE**: Phase 6 must verify app starts without Koin errors.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T7.1 | Wrap root App composable with `SecurityGate { ... }` — the SecurityGate composable auto-wires: tamper detection at startup, session timeout check on app resume, session touch on pointer input, biometric re-auth on session expiry. It provides `LocalSecurityState` to the composable tree. | App root composable | App starts with SecurityGate wrapping |

**T7.1 implementation:**
```kotlin
import template.core.base.security.SecurityGate

@Composable
fun ComposeApp(...) {
    // ... state collection, theme detection ...
    SecurityGate {
        MifosPayTheme(darkTheme = uiState.darkTheme, ...) {
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
| T7.2 | Override `SecurityPolicy` in DI for wallet-specific timeout (financial app = shorter timeout for security): | DI override in KoinModules | Policy applied |

**T7.2 implementation:**
```kotlin
// In sharedModule or a securityOverrideModule:
single { SecurityPolicy(sessionTimeoutMinutes = 10, requireBiometricForSensitiveOps = true) }
// Wallet app handles money — use 10 min timeout (shorter than the 30 min default)
```

### Phase 8 — Verification
> **GATE**: Phase 7 must verify SecurityGate wraps the app correctly.

| Task | Description | Command | Verify |
|------|-------------|---------|--------|
| T8.1 | Build demo debug APK | `./gradlew :cmp-android:assembleDemoDebug` | Exit 0 |
| T8.2 | Static analysis | `./gradlew spotlessCheck detekt` | Exit 0 |
| T8.3 | iOS KSP (verifies TypeConverters with `@kotlin.concurrent.Volatile`) | `./gradlew :core:database:kspKotlinIosArm64` | Exit 0 |
| T8.4 | iOS framework link | `./gradlew :cmp-shared:linkDebugFrameworkIosArm64` | Exit 0 |
| T8.5 | Desktop build | `./gradlew :cmp-desktop:jar` | Exit 0 |
| T8.6 | Encryption roundtrip test: encrypt a TypeConverter value, read it back, verify `ENC:` prefix and correct decryption | Manual test or unit test | Values match |
| T8.7 | DataStore migration test: verify existing users' plain-stored userData migrates to secure store on first launch | Manual test | Init block runs migration |
| T8.8 | Store 5 test: verify at least one repository returns `StoreData` with `origin = NETWORK` on fresh fetch, `origin = CACHE` on subsequent reads | Manual or unit test | Origins correct |
| T8.9 | Legacy PreferencesHelper fully deprecated — no callers remain | `grep -r "PreferencesHelper" feature/` | Returns 0 matches |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Greenfield Room 3 (no existing entities) | Medium | Design entities based on repository contracts |
| Legacy PreferencesHelper migration | High | Gradual deprecation, migrate callers one by one |
| 24 repositories to wrap with Store 5 | High | Start with 6 high-value, batch rest incrementally |
| Financial app security requirements | Critical | Shorter session timeout, stronger encryption policy |
| Missing KMPRoomConventionPlugin | Medium | sync-dirs should deliver it; create manually if not |

## Estimated Effort

| Phase | Effort |
|-------|--------|
| Phase 0 (sync-dirs) | 15 min |
| Phase 1 (Gradle) | 45 min |
| Phase 2 (Security) | 30 min |
| Phase 3 (Room 3 — greenfield) | 3-4 hours |
| Phase 4 (DataStore + legacy) | 2 hours |
| Phase 5 (Store 5) | 3-4 hours |
| Phase 6 (DI) | 15 min |
| Phase 7 (SecurityGate) | 15 min |
| Phase 8 (Verification) | 30 min |
| **Total** | **~10-12 hours** |

---

## Session Strategy

Execute in a **dedicated session** per phase group:
- **Session 1**: Phase 0-2 (infrastructure + security + legacy audit)
- **Session 2**: Phase 3 (Room 3 entity design + creation — largest phase)
- **Session 3**: Phase 4-5 (DataStore consolidation + Store 5)
- **Session 4**: Phase 6-8 (DI + SecurityGate + verification)
