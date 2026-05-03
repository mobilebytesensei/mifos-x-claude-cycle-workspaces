# PLAN-migration-mifos-mobile-260501: Room 3 + Store 5 + Security Migration

| Field | Value |
|-------|-------|
| ID | migration-mifos-mobile-260501 |
| Status | Draft |
| Priority | P1 |
| Scope | mifos-mobile — full stack migration |
| Created | 2026-05-01 |
| Source Branch | development |
| Upstream Repo | `openMF/mifos-mobile` |
| Fork Repo | `therajanmaurya/mifos-mobile` |
| Workspace | `workspaces/mifos-x/mifos-mobile/` |
| Source Path | `workspaces/mifos-x/mifos-mobile/source/mifos-mobile/` |
| Remote (origin) | `git@github.com:therajanmaurya/mifos-mobile.git` (fork) |
| Remote (upstream) | `git@github.com:openMF/mifos-mobile.git` (org) |
| Fork Setup Needed | Yes — currently origin points to openMF, needs fork + remote fix |
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
| Room | 3.0.0-alpha03 (already) | 3.0.0-alpha03 | TypeConverter encryption only |
| Store 5 | Empty `AppStoreModule` exists (no Store instances) | Full adoption (10 cached + 6 memory + 7 network-only) | Populate with concrete Stores |
| Security | **Already wired** — SecurityModule is first in KoinModules | Verify + add to core/database | Mostly done, verify deps |
| DataStore | **Already dual-store** — plain + secure Settings via FieldEncryptor | Verify field placement | Mostly done, audit only |
| Kotlin | 2.1.20 | 2.3.20+ | Version bump |
| Koin | 4.1.0 | 4.1.1 | Minor bump |
| Entities | 2 (Charge, Notification) | **12 entities** (full offline) | Create 10 new entities |
| DAOs | 2 (ChargeDao, NotificationDao) — **both have missing queries** | **12 DAOs** (with full CRUD) | Fix existing 2 + create 10 new |
| TypeConverters | 1 (ChargeTypeConverters — uses FieldEncryptor typealiases) | 2 (add MifosTypeConverters) | Add converter for new entities |
| Mappers | **Commented out** — ChargeEntity↔Charge, Notification↔entity all commented | Full dto→entity, entity→domain mappers | Uncomment + create 12 new |
| Repository impls | **Stubbed** — ChargeRepo + NotificationRepo have DAO deps commented out | Full Store 5 integration | Reconstruct from scratch |
| SecurityGate | Not present | Root composable | Add wrapper |
| Offline Coverage | **~0%** (DAO calls commented out) | **100%** (all list/detail screens) | Full offline support |
| Staleness UI | Not present | Per-screen freshness indicator | Primitive params (no Store dep in UI) |
| KMPRoomConventionPlugin | Exists (Room 3 — already updated via sync-dirs) | Room 3 | Already done |
| AppDatabase | **Already has `@ConstructedBy`** on all platforms | Add new entities + bump version | Schema migration needed |

### Already Done (Verify Only — Do NOT Re-do)

> These items were found to be ALREADY IMPLEMENTED in the codebase:
> 1. `SecurityModule` is FIRST in `KoinModules.allModules`
> 2. `AppStoreModule` exists (includes `StoreModule` from core-base) — but is empty
> 3. `PreferencesModule` already provides dual Settings: `named("plain")` + `named("secure")`
> 4. `UserPreferencesDataSource` already accepts `plainSettings`, `secureSettings`, `dispatcher`, `fieldEncryptor`
> 5. `AppDatabase` already has `@ConstructedBy(AppDatabaseConstructor::class)` on all platforms
> 6. `core/data/build.gradle.kts` already depends on `coreBase.store`, `store5`, `store5-cache`
> 7. Room version is already 3.0.0-alpha03 in `libs.versions.toml`
> 8. Store version is already 5.1.0-alpha08 in `libs.versions.toml`

### Critical Technical Gaps

1. **Two incompatible `DataState` types** — `org.mifos.mobile.core.common.DataState` (Loading/Success/Error) vs `template.core.base.common.DataState` (adds Pending/NoNetwork). All ViewModels use the mifos version. `StoreData.toDataState()` produces the template version. **Must bridge or avoid template DataState entirely.**
2. **Ktorfit returns `Flow<T>`, Fetcher.of() needs `suspend (Key) -> T`** — ALL fetcher wiring must call `.first()` to convert.
3. **Entity↔domain mappers commented out** — ChargeEntity.toCharge(), Charge.toChargeEntity(), MifosNotification.toEntity() all commented. ChargeResponseDto→ChargeEntity doesn't exist. Codebase convention is `.toModel()` not `.toDomain()`.
4. **Repository implementations are stubs** — ChargeRepo and NotificationRepo have DAO deps commented out, returning hardcoded empty data.
5. **ChargeDao missing queries** — no `getChargesByClientId()`, no `deleteByClientId()`, no `deleteAll()`. Store 5 SourceOfTruth needs all three.
6. **ChargeEntity.clientId is `Int?`** but API and repository use `Long`. Type mismatch in queries.

### Offline Support Strategy

| Category | Repositories (17 total) | Offline Strategy | Entity Needed? |
|----------|-------------|-----------------|:--------------:|
| **Full Cache (SourceOfTruth)** | Accounts, Client, Home, Loans (detail+list), Savings (detail+list), Shares, Beneficiary (list), Charges, Notifications, Transactions, Guarantors (list) | Store 5 + Room entity + DAO. Read methods → `Flow<StoreData<T>>`. | Yes |
| **Memory Cache (ephemeral)** | LoanTemplate, LoanTemplateByProduct, SavingsTemplate, SavingsTemplateByProduct, AccountOptionsTemplate, BeneficiaryTemplate, GuarantorTemplate, ShareProducts, ShareProductById | `createMemoryStore` — templates change frequently, not worth persisting | No |
| **Network Only (mutations)** | UserAuth (login/register/verify/updatePassword), Transfer.makeTransfer, ThirdPartyTransfer.makeTransfer, ReviewLoan.submitLoan, Beneficiary (create/update/delete), Guarantor (create/update/delete), SavingsAccount (submit/update/withdraw), ShareAccount.submitApplication, LoanRepo.withdrawLoan, UserDetail (register/updateNotification) | Remain `suspend fun: DataState<T>`. NO Store wrapping. | No |

> **RULE**: Only `Flow<DataState<T>>` read methods become `Flow<StoreData<T>>`. Mutation methods (`suspend fun: DataState<T>`) are NEVER wrapped in Store 5.

### Staleness UI Strategy

Every screen that displays cached data shows a **freshness indicator**.
The `DataFreshnessIndicator` composable accepts **primitive params only** (no Store types) to keep `core/ui` decoupled:

```kotlin
// Parameters are primitives — NO StoreData.Origin import needed in core/ui
@Composable
fun DataFreshnessIndicator(
    isFreshData: Boolean,        // true when origin == NETWORK
    lastFetchedAt: Long?,        // epoch millis from entity.lastFetchedAt
    isRefreshing: Boolean,       // background refresh in progress
    isNetworkAvailable: Boolean, // from NetworkMonitor.isOnline
    onRefresh: () -> Unit,
)
```

- `isFreshData = true` → hidden (data is fresh from network)
- `isFreshData = false` + `lastFetchedAt != null` → "Updated X min ago" + Refresh button
- `isRefreshing = true` → subtle LinearProgressIndicator
- `isNetworkAvailable = false` → "Offline — showing cached data" banner
- `NetworkMonitor` already exists on all platforms (Android: ConnectivityManager, others: expect/actual)

---

## Migration Tasks

### Phase 0 — sync-dirs (MANDATORY FIRST STEP)
> Delivers core-base/security, core-base/store, core-base/database (Room 3), updated build-logic from template.
> **CRITICAL**: core-base files are OWNED by kmp-project-template. NEVER edit core-base/ directly in consumer apps.
> After sync, core-base/database imports will use `androidx.room3.*` (Room 3 package namespace).

| Task | Description | Blocking? |
|------|-------------|:---------:|
| T0.1 | Run `./sync-dirs.sh` from source root (fetches from upstream openMF/kmp-project-template) | Yes |
| T0.2 | Review sync changes — verify core-base/security/, core-base/store/, core-base/database/ updated with Room 3 imports (`import androidx.room3.*`) | Yes |
| T0.3 | Verify build-logic/convention plugins updated (KMPRoomConventionPlugin uses `androidx.room3` plugin + artifacts) | Yes |
| T0.4 | Verify `MifosGitHooksConventionPlugin` handles submodule `.git` file (sync brings fix for `resolveGitDir()`) | Yes |
| T0.5 | Commit sync changes to feature branch | Yes |

### Phase 1 — Gradle Verification + Additions
> **NOTE**: Most Gradle deps are ALREADY present (Room 3, Store 5, Security, Store cache). This phase is mostly verification.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T1.1 | **VERIFY** `gradle/libs.versions.toml` already has: `room = "3.0.0-alpha03"`, `store = "5.1.0-alpha08"`, room plugin ID = `androidx.room3` | `gradle/libs.versions.toml` | `grep "room3\|store5" gradle/libs.versions.toml` |
| T1.2 | **VERIFY** `settings.gradle.kts` includes `:core-base:security`, `:core-base:store`, `:core-base:datastore` | `settings.gradle.kts` | `grep "core-base" settings.gradle.kts` |
| T1.3 | **VERIFY** `core/data/build.gradle.kts` has `coreBase.store`, `store5`, `store5.cache` deps | `core/data/build.gradle.kts` | `grep "store" core/data/build.gradle.kts` |
| T1.4 | Add `implementation(projects.core.database)` to `core/data/build.gradle.kts` — needed for DAO injection into repositories | `core/data/build.gradle.kts` | `grep "core.database" core/data/build.gradle.kts` |
| T1.5 | Add `implementation(libs.kotlinx.datetime)` to `core/data/build.gradle.kts` — needed for `Clock.System.now()` in Store timestamps | `core/data/build.gradle.kts` | Gradle sync |

### Phase 2 — Security + DI Verification
> **GATE**: Phase 1 must compile build-logic (`./gradlew check -p build-logic`).
> **NOTE**: SecurityModule is ALREADY wired as first module. This phase is verification + minor additions.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T2.1 | **VERIFY** `SecurityModule` is FIRST in `KoinModules.allModules` (already true) | `cmp-navigation/.../di/KoinModules.kt` | Read file, confirm order |
| T2.2 | **VERIFY** `core/database/build.gradle.kts` depends on `coreBase.security` (already true) | `core/database/build.gradle.kts` | `grep "security" core/database/build.gradle.kts` |
| T2.3 | **VERIFY** `AppStoreModule` exists in `KoinModules.allModules` (already true — empty shell) | `cmp-navigation/.../di/KoinModules.kt` | Read file, confirm exists |
| T2.4 | **VERIFY** `PreferencesModule` provides dual Settings: `named("plain")` + `named("secure")` (already true) | `core/datastore/.../di/PreferenceModule.kt` | Read file, confirm dual Settings |
| T2.5 | **VERIFY** `UserPreferencesDataSource` accepts `plainSettings`, `secureSettings`, `fieldEncryptor` (already true) | `core/datastore/.../UserPreferencesDataSource.kt` | Read constructor |
| T2.6 | Verify: `./gradlew :cmp-navigation:compileDemoDebugKotlinAndroid` | CI | Exit 0 |

### Phase 3 — Room 3 Database Migration + Offline Entities
> **GATE**: Phase 2 must verify SecurityModule compiles.
> **IMPORTANT**: Room 3 changed BOTH artifact coordinates (`androidx.room3:room3-*`) AND Kotlin package namespace (`import androidx.room3.*`).
> After Phase 0 sync-dirs, core-base/database typealiases already use `import androidx.room3.*`.
> Consumer code in `core/database/` must also update to `import androidx.room3.*`.
> Consumer entities/DAOs that use `template.core.base.database.*` typealiases do NOT need import changes.

#### 3A — Verify Existing Code + Fix ChargeEntity/DAO Gaps

> **NOTE**: Existing entities use `template.core.base.database.*` typealiases — NO import changes needed.
> `@ConstructedBy` already exists on AppDatabase — NO annotation changes needed.
> Focus is on fixing gaps in existing ChargeDao + ChargeEntity for Store 5 compatibility.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3A.1 | **VERIFY** existing entities use `template.core.base.database.*` typealiases (NOT `import androidx.room.*`) | `core/database/src/commonMain/.../entity/*.kt` | `grep -r "import androidx.room\." core/database/src/commonMain/` returns 0 |
| T3A.2 | **VERIFY** AppDatabase already has `@ConstructedBy(AppDatabaseConstructor::class)` on all platforms | `core/database/src/*/AppDatabase.kt` | Read files, confirm annotation exists |
| T3A.3 | **FIX** `ChargeEntity.clientId` type: `Int?` → `Long?` (API uses `Long` for clientId) | `core/database/.../entity/ChargeEntity.kt` | Type matches repo signatures |
| T3A.4 | **ADD** missing queries to `ChargeDao` for Store 5 SourceOfTruth: | `core/database/.../dao/ChargeDao.kt` | KSP compiles |

**T3A.4 — queries to ADD to ChargeDao:**
```kotlin
// Store 5 SourceOfTruth needs per-key read, per-key delete, and deleteAll
@Query("SELECT * FROM charges WHERE clientId = :clientId")
fun getChargesByClientId(clientId: Long): Flow<List<ChargeEntity>>

@Query("DELETE FROM charges WHERE clientId = :clientId")
suspend fun deleteByClientId(clientId: Long)

@Query("DELETE FROM charges")
suspend fun deleteAll()
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3A.5 | **UNCOMMENT + FIX** entity↔domain mappers (currently commented out): | `core/data/.../mapper/` | Compiles |

**T3A.5 — mappers to uncomment/create:**
```kotlin
// In core/data/src/commonMain/.../mapper/charge/ChargeMapper.kt:
// UNCOMMENT and fix these (convention: .toModel() for domain, .toEntity() for entity):
fun ChargeEntity.toModel(): Charge { /* map all fields */ }
fun Charge.toEntity(lastFetchedAt: Long = 0L): ChargeEntity { /* map all fields */ }

// CREATE NEW — does not exist yet:
fun ChargeResponseDto.toEntity(clientId: Long, lastFetchedAt: Long): ChargeEntity { /* dto → entity */ }

// In core/data/src/commonMain/.../mapper/notification/:
// UNCOMMENT:
fun MifosNotificationEntity.toModel(): MifosNotification { /* map fields */ }
fun MifosNotification.toEntity(): MifosNotificationEntity { /* map fields */ }
```

> **NAMING CONVENTION**: Codebase uses `.toModel()` for→domain, `.toEntity()` for→entity. NOT `.toDomain()`.
> All code snippets in this plan use `.toModel()` and `.toEntity()` accordingly.

#### 3B — New Entities for Full Offline Support

> **10 new entities** to give every list/detail screen offline capability.
> All entities use `template.core.base.database.*` typealiases for Room 3 portability.
> Each entity includes `lastFetchedAt: Long` for staleness tracking in UI.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.1 | Create `ClientEntity` | NEW: `core/database/.../entity/ClientEntity.kt` | KSP compiles |

**T3B.1 implementation:**
```kotlin
@Entity(tableName = "clients")
data class ClientEntity(
    @PrimaryKey val clientId: Long,
    @ColumnInfo(name = "account_no") val accountNo: String,
    @ColumnInfo(name = "display_name") val displayName: String,
    @ColumnInfo(name = "office_name") val officeName: String,
    @ColumnInfo(name = "image_present") val imagePresent: Boolean = false,
    @ColumnInfo(name = "external_id") val externalId: String? = null,
    @ColumnInfo(name = "status") val status: String,
    @ColumnInfo(name = "active") val active: Boolean,
    @ColumnInfo(name = "activation_date") val activationDate: String? = null,
    @ColumnInfo(name = "gender") val gender: String? = null,
    @ColumnInfo(name = "phone_no") val phoneNo: String? = null,
    @ColumnInfo(name = "email") val email: String? = null,
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.2 | Create `LoanAccountEntity` | NEW: `core/database/.../entity/LoanAccountEntity.kt` | KSP compiles |

**T3B.2 implementation:**
```kotlin
@Entity(tableName = "loan_accounts")
data class LoanAccountEntity(
    @PrimaryKey val loanId: Long,
    @ColumnInfo(name = "client_id") val clientId: Long,
    @ColumnInfo(name = "account_no") val accountNo: String,
    @ColumnInfo(name = "product_name") val productName: String,
    @ColumnInfo(name = "principal") val principal: Double,
    @ColumnInfo(name = "loan_balance") val loanBalance: Double,
    @ColumnInfo(name = "amount_paid") val amountPaid: Double,
    @ColumnInfo(name = "total_outstanding") val totalOutstanding: Double,
    @ColumnInfo(name = "status") val status: String,
    @ColumnInfo(name = "loan_type") val loanType: String,
    @ColumnInfo(name = "currency_code") val currencyCode: String,
    @ColumnInfo(name = "in_arrears") val inArrears: Boolean = false,
    @ColumnInfo(name = "timeline_json") val timelineJson: String? = null,  // encrypted JSON
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.3 | Create `SavingsAccountEntity` | NEW: `core/database/.../entity/SavingsAccountEntity.kt` | KSP compiles |

```kotlin
@Entity(tableName = "savings_accounts")
data class SavingsAccountEntity(
    @PrimaryKey val savingsId: Long,
    @ColumnInfo(name = "client_id") val clientId: Long,
    @ColumnInfo(name = "account_no") val accountNo: String,
    @ColumnInfo(name = "product_name") val productName: String,
    @ColumnInfo(name = "account_balance") val accountBalance: Double,
    @ColumnInfo(name = "total_deposits") val totalDeposits: Double,
    @ColumnInfo(name = "total_withdrawals") val totalWithdrawals: Double,
    @ColumnInfo(name = "status") val status: String,
    @ColumnInfo(name = "currency_code") val currencyCode: String,
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.4 | Create `ShareAccountEntity` | NEW: `core/database/.../entity/ShareAccountEntity.kt` | KSP compiles |

```kotlin
@Entity(tableName = "share_accounts")
data class ShareAccountEntity(
    @PrimaryKey val shareId: Long,
    @ColumnInfo(name = "client_id") val clientId: Long,
    @ColumnInfo(name = "account_no") val accountNo: String,
    @ColumnInfo(name = "product_name") val productName: String,
    @ColumnInfo(name = "total_approved_shares") val totalApprovedShares: Int,
    @ColumnInfo(name = "total_pending_shares") val totalPendingShares: Int,
    @ColumnInfo(name = "status") val status: String,
    @ColumnInfo(name = "currency_code") val currencyCode: String,
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.5 | Create `BeneficiaryEntity` | NEW: `core/database/.../entity/BeneficiaryEntity.kt` | KSP compiles |

```kotlin
@Entity(tableName = "beneficiaries")
data class BeneficiaryEntity(
    @PrimaryKey val beneficiaryId: Long,
    @ColumnInfo(name = "name") val name: String,
    @ColumnInfo(name = "office_name") val officeName: String,
    @ColumnInfo(name = "account_type") val accountType: String,
    @ColumnInfo(name = "account_number") val accountNumber: String,
    @ColumnInfo(name = "transfer_limit") val transferLimit: Double,
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.6 | Create `TransactionEntity` | NEW: `core/database/.../entity/TransactionEntity.kt` | KSP compiles |

```kotlin
@Entity(
    tableName = "transactions",
    indices = [Index(value = ["client_id"])]
)
data class TransactionEntity(
    @PrimaryKey val transactionId: Long,
    @ColumnInfo(name = "client_id") val clientId: Long,
    @ColumnInfo(name = "account_id") val accountId: Long,
    @ColumnInfo(name = "amount") val amount: Double,
    @ColumnInfo(name = "date") val date: String,
    @ColumnInfo(name = "type") val type: String,
    @ColumnInfo(name = "currency_code") val currencyCode: String,
    @ColumnInfo(name = "account_type") val accountType: String,  // loan, savings, share
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.7 | Create `GuarantorEntity` | NEW: `core/database/.../entity/GuarantorEntity.kt` | KSP compiles |

```kotlin
@Entity(
    tableName = "guarantors",
    indices = [Index(value = ["loan_id"])]
)
data class GuarantorEntity(
    @PrimaryKey val guarantorId: Long,
    @ColumnInfo(name = "loan_id") val loanId: Long,
    @ColumnInfo(name = "firstname") val firstname: String,
    @ColumnInfo(name = "lastname") val lastname: String,
    @ColumnInfo(name = "guarantor_type") val guarantorType: String,
    @ColumnInfo(name = "relationship") val relationship: String? = null,
    @ColumnInfo(name = "amount") val amount: Double? = null,
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.8 | Create `ClientAccountsEntity` — denormalized summary of all account types per client | NEW: `core/database/.../entity/ClientAccountsEntity.kt` | KSP compiles |

```kotlin
@Entity(tableName = "client_accounts_summary")
data class ClientAccountsEntity(
    @PrimaryKey val clientId: Long,
    @ColumnInfo(name = "loan_accounts_json") val loanAccountsJson: String,       // encrypted JSON list
    @ColumnInfo(name = "savings_accounts_json") val savingsAccountsJson: String,  // encrypted JSON list
    @ColumnInfo(name = "share_accounts_json") val shareAccountsJson: String,      // encrypted JSON list
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.9 | Create `LoanDetailsEntity` — full loan with associations (for detail screen offline) | NEW: `core/database/.../entity/LoanDetailsEntity.kt` | KSP compiles |

```kotlin
@Entity(tableName = "loan_details")
data class LoanDetailsEntity(
    @PrimaryKey val loanId: Long,
    @ColumnInfo(name = "details_json") val detailsJson: String,  // encrypted JSON — full LoanWithAssociations
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B.10 | Create `SavingsDetailsEntity` — full savings with associations | NEW: `core/database/.../entity/SavingsDetailsEntity.kt` | KSP compiles |

```kotlin
@Entity(tableName = "savings_details")
data class SavingsDetailsEntity(
    @PrimaryKey val savingsId: Long,
    @ColumnInfo(name = "details_json") val detailsJson: String,  // encrypted JSON — full SavingsWithAssociations
    @ColumnInfo(name = "last_fetched_at") val lastFetchedAt: Long = 0L,
)
```

#### 3B-extra — Mappers for New Entities

> **Every new entity needs 3 mappers**: `Dto.toEntity()`, `Entity.toModel()`, `DomainModel.toEntity()`.
> Place in `core/data/src/commonMain/.../mapper/{domain}/` following existing convention.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3B-M.1 | Create `ClientResponseDto.toEntity()`, `ClientEntity.toModel()`, `Client.toEntity()` | NEW: `core/data/.../mapper/client/ClientMapper.kt` | Compiles |
| T3B-M.2 | Create `LoanAccount` mappers (dto→entity, entity→model) — handle `timelineJson` encrypted field | NEW: `core/data/.../mapper/loan/LoanAccountMapper.kt` | Compiles |
| T3B-M.3 | Create `SavingsAccount` mappers | NEW: `core/data/.../mapper/savings/SavingsAccountMapper.kt` | Compiles |
| T3B-M.4 | Create `ShareAccount` mappers | NEW: `core/data/.../mapper/share/ShareAccountMapper.kt` | Compiles |
| T3B-M.5 | Create `Beneficiary` mappers | NEW: `core/data/.../mapper/beneficiary/BeneficiaryMapper.kt` | Compiles |
| T3B-M.6 | Create `Transaction` mappers | NEW: `core/data/.../mapper/transaction/TransactionMapper.kt` | Compiles |
| T3B-M.7 | Create `Guarantor` mappers | NEW: `core/data/.../mapper/guarantor/GuarantorMapper.kt` | Compiles |
| T3B-M.8 | Create `ClientAccounts` mappers — handles encrypted JSON list columns | NEW: `core/data/.../mapper/account/ClientAccountsMapper.kt` | Compiles |
| T3B-M.9 | Create `LoanDetails` mappers — encrypted JSON blob for LoanWithAssociations | NEW: `core/data/.../mapper/loan/LoanDetailsMapper.kt` | Compiles |
| T3B-M.10 | Create `SavingsDetails` mappers — encrypted JSON blob for SavingsWithAssociations | NEW: `core/data/.../mapper/savings/SavingsDetailsMapper.kt` | Compiles |

#### 3C — New DAOs for Full Offline Support

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3C.1 | Create `ClientDao` | NEW: `core/database/.../dao/ClientDao.kt` | KSP compiles |

```kotlin
@Dao
interface ClientDao {
    @Query("SELECT * FROM clients WHERE clientId = :clientId")
    fun getClient(clientId: Long): Flow<ClientEntity?>

    @Query("SELECT * FROM clients ORDER BY displayName ASC")
    fun getAllClients(): Flow<List<ClientEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(clients: List<ClientEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(client: ClientEntity)

    @Query("DELETE FROM clients")
    suspend fun deleteAll()
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3C.2 | Create `LoanAccountDao` | NEW: `core/database/.../dao/LoanAccountDao.kt` | KSP compiles |

```kotlin
@Dao
interface LoanAccountDao {
    @Query("SELECT * FROM loan_accounts WHERE client_id = :clientId")
    fun getLoansByClientId(clientId: Long): Flow<List<LoanAccountEntity>>

    @Query("SELECT * FROM loan_accounts WHERE loanId = :loanId")
    fun getLoanById(loanId: Long): Flow<LoanAccountEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(loans: List<LoanAccountEntity>)

    @Query("DELETE FROM loan_accounts WHERE client_id = :clientId")
    suspend fun deleteByClientId(clientId: Long)

    @Query("DELETE FROM loan_accounts")
    suspend fun deleteAll()
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3C.3 | Create `SavingsAccountDao` | NEW | KSP compiles |
| T3C.4 | Create `ShareAccountDao` | NEW | KSP compiles |
| T3C.5 | Create `BeneficiaryDao` | NEW | KSP compiles |
| T3C.6 | Create `TransactionDao` (with `getByClientId`, `getByAccountId`, pagination support) | NEW | KSP compiles |
| T3C.7 | Create `GuarantorDao` (with `getByLoanId`) | NEW | KSP compiles |
| T3C.8 | Create `ClientAccountsDao` (single row per client — summary) | NEW | KSP compiles |
| T3C.9 | Create `LoanDetailsDao` (full detail JSON per loan) | NEW | KSP compiles |
| T3C.10 | Create `SavingsDetailsDao` (full detail JSON per savings) | NEW | KSP compiles |

All DAOs follow the same pattern as T3C.1-2: `Flow<>` for reads, `suspend` for writes, `OnConflictStrategy.REPLACE`, delete methods.

#### 3D — TypeConverter Encryption

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3D.1 | Add encrypted TypeConverters with exact pattern: | `core/database/src/commonMain/.../utils/ChargeTypeConverters.kt` | Compiles |

**T3D.1 implementation pattern:**
```kotlin
class ChargeTypeConverters {
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
    // Wrap ALL existing @TypeConverter methods with encrypt/decrypt
    @TypeConverter fun fromChargeList(charges: List<Charge>): String = encrypt(Json.encodeToString(charges))
    @TypeConverter fun toChargeList(json: String): List<Charge> = Json.decodeFromString(decrypt(json))
    // ... repeat for all converter methods
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3D.2 | Create `MifosTypeConverters` — unified converter for all new entity JSON fields (loanAccountsJson, detailsJson, etc.) | NEW: `core/database/.../utils/MifosTypeConverters.kt` | Compiles |

```kotlin
class MifosTypeConverters {
    companion object {
        @kotlin.concurrent.Volatile
        private var encryptor: FieldEncryptor? = null
        fun install(fieldEncryptor: FieldEncryptor) { encryptor = fieldEncryptor }
    }
    private fun encrypt(value: String): String { /* same pattern */ }
    private fun decrypt(value: String): String { /* same pattern */ }

    // Converters for new entity JSON fields
    @TypeConverter fun fromIntList(list: List<Int>): String = encrypt(Json.encodeToString(list))
    @TypeConverter fun toIntList(json: String): List<Int> = Json.decodeFromString(decrypt(json))
    @TypeConverter fun fromLongList(list: List<Long>): String = encrypt(Json.encodeToString(list))
    @TypeConverter fun toLongList(json: String): List<Long> = Json.decodeFromString(decrypt(json))
}
```

#### 3E — Update AppDatabase + Platform DI

> **NOTE**: `@ConstructedBy(AppDatabaseConstructor::class)` is ALREADY present — do NOT re-add.
> **MIGRATION**: Version 1→2 adds 10 new tables. Use `fallbackToDestructiveMigration()` for initial dev
> (no prod users yet). For prod release, write proper `AutoMigration(from = 1, to = 2)` or manual Migration.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3E.1 | Update `AppDatabase` to register ALL new entities and DAOs: | `core/database/src/commonMain/.../AppDatabase.kt` | Compiles |

**T3E.1 — AppDatabase updated:**
```kotlin
@Database(
    entities = [
        ChargeEntity::class, MifosNotificationEntity::class,
        // NEW offline entities:
        ClientEntity::class, LoanAccountEntity::class, SavingsAccountEntity::class,
        ShareAccountEntity::class, BeneficiaryEntity::class, TransactionEntity::class,
        GuarantorEntity::class, ClientAccountsEntity::class,
        LoanDetailsEntity::class, SavingsDetailsEntity::class,
    ],
    version = 2,  // Bump from 1
    autoMigrations = [AutoMigration(from = 1, to = 2)],  // Safe: only ADD tables, no column changes to existing
    exportSchema = true,
)
@TypeConverters(ChargeTypeConverters::class, MifosTypeConverters::class)
@ConstructedBy(AppDatabaseConstructor::class)  // ALREADY EXISTS — verify, do not re-add
abstract class AppDatabase : RoomDatabase() {
    // Existing
    abstract fun chargeDao(): ChargeDao
    abstract fun notificationDao(): MifosNotificationDao
    // NEW offline DAOs
    abstract fun clientDao(): ClientDao
    abstract fun loanAccountDao(): LoanAccountDao
    abstract fun savingsAccountDao(): SavingsAccountDao
    abstract fun shareAccountDao(): ShareAccountDao
    abstract fun beneficiaryDao(): BeneficiaryDao
    abstract fun transactionDao(): TransactionDao
    abstract fun guarantorDao(): GuarantorDao
    abstract fun clientAccountsDao(): ClientAccountsDao
    abstract fun loanDetailsDao(): LoanDetailsDao
    abstract fun savingsDetailsDao(): SavingsDetailsDao

    companion object { const val DATABASE_NAME = "mifos_mobile_database" }
}

// ALREADY EXISTS — do NOT recreate:
// expect object AppDatabaseConstructor : RoomDatabaseConstructor<AppDatabase>
```

> **⚠ ChargeEntity.clientId type change (T3A.3)**: Changing `Int?` → `Long?` is a COLUMN TYPE CHANGE.
> `AutoMigration` cannot handle this. Options:
> 1. Use `fallbackToDestructiveMigration()` (OK for dev — existing data is minimal)
> 2. Write manual `Migration(1, 2)` with `ALTER TABLE charges RENAME TO charges_old; CREATE TABLE charges ...; INSERT INTO charges SELECT ...`
> **Recommendation**: Use option 1 for dev branch, write proper migration before prod release.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3E.2 | Update platform DatabaseModule DI — install ALL TypeConverters BEFORE `build()`: | `core/database/src/*/di/DatabaseModule.*.kt` | Compiles |

**T3E.2 implementation (per platform):**
```kotlin
single {
    val fieldEncryptor = get<FieldEncryptor>()
    ChargeTypeConverters.install(fieldEncryptor)
    MifosTypeConverters.install(fieldEncryptor)

    AppDatabaseFactory(/* platform context */)
        .createDatabase(AppDatabase::class.java, AppDatabase.DATABASE_NAME)
        .fallbackToDestructiveMigrationOnDowngrade(false)
        .setDriver(BundledSQLiteDriver())
        .setQueryCoroutineContext(get(named(MifosDispatchers.IO.name)))
        .build()
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T3E.3 | Update common DatabaseModule to expose ALL DAO singletons | `core/database/src/commonMain/.../di/DatabaseModule.kt` | Compiles |

```kotlin
val DatabaseModule = module {
    includes(platformDatabaseModule)
    // Existing
    single { get<AppDatabase>().chargeDao() }
    single { get<AppDatabase>().notificationDao() }
    // NEW offline DAOs
    single { get<AppDatabase>().clientDao() }
    single { get<AppDatabase>().loanAccountDao() }
    single { get<AppDatabase>().savingsAccountDao() }
    single { get<AppDatabase>().shareAccountDao() }
    single { get<AppDatabase>().beneficiaryDao() }
    single { get<AppDatabase>().transactionDao() }
    single { get<AppDatabase>().guarantorDao() }
    single { get<AppDatabase>().clientAccountsDao() }
    single { get<AppDatabase>().loanDetailsDao() }
    single { get<AppDatabase>().savingsDetailsDao() }
}
```

#### 3F — Verification

| Task | Description | Command | Verify |
|------|-------------|---------|--------|
| T3F.1 | Verify KSP on ALL platforms | `./gradlew :core:database:kspKotlinIosArm64` | Exit 0 |
| T3F.2 | Verify all 12 DAOs are exposed via DI | `./gradlew :core:database:compileDemoDebugKotlinAndroid` | Exit 0 |

### Phase 4 — DataStore Verification (ALREADY IMPLEMENTED)
> **GATE**: Phase 3 must pass KSP verification.
> **NOTE**: Dual-store is ALREADY implemented. `PreferencesModule` already provides `named("plain")` + `named("secure")`.
> `UserPreferencesDataSource` already accepts `plainSettings`, `secureSettings`, `dispatcher`, `fieldEncryptor`.
> This phase is **verification only** — do NOT re-implement.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T4.1 | **VERIFY** `core/datastore/build.gradle.kts` depends on `coreBase.datastore` (already true) | `core/datastore/build.gradle.kts` | `grep "datastore" core/datastore/build.gradle.kts` |
| T4.2 | **VERIFY** `PreferencesModule` includes `DatastoreBaseModule` and injects dual Settings (already true) | `core/datastore/.../di/PreferenceModule.kt` | Read file, confirm `named("plain")` + `named("secure")` |
| T4.3 | **VERIFY** `UserPreferencesDataSource` constructor has `plainSettings`, `secureSettings`, `fieldEncryptor` params (already true) | `core/datastore/.../UserPreferencesDataSource.kt` | Read constructor |
| T4.4 | **AUDIT** which fields are stored in `plainSettings` vs `secureSettings` — ensure sensitive data (token, passcode, authKey, userId, clientId) is in `secureSettings` | Same file | Sensitive fields in secure store |
| T4.5 | Verify: `./gradlew :core:datastore:compileDemoDebugKotlinAndroid` | CI | Exit 0 |

### Phase 5 — Store 5 Adoption (Full Offline + Staleness UI)
> **GATE**: Phase 4 must verify dual-store reads/writes.
> Store 5 uses `StoreFactory` from core-base/store. Each repository wraps its API service (Fetcher) + Room DAO (SourceOfTruth).
> The repository returns `Flow<StoreData<T>>` instead of raw `Flow<T>`, giving consumers origin/freshness metadata.
> **FULL OFFLINE**: Every list/detail screen works from cache. Memory-only for templates. Network-only for mutations.
> **STALENESS UI**: Every screen shows data freshness via `StoreData.origin` + `StoreData.fetchedAt`.

#### 5A — Store Module + Staleness UI Components

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5A.1 | **VERIFY** `AppStoreModule` already exists in `KoinModules.allModules` (empty shell). Populate it or keep as-is if stores are created inline in repositories | `cmp-navigation/.../di/KoinModules.kt` | Read file, confirm exists |

> **NOTE**: `AppStoreModule` already exists and includes `StoreModule` from core-base. Do NOT re-create.
> Store instances can live inline in repository classes (simpler) or be extracted to `AppStoreModule` (shared).
> This plan uses inline stores in repos for simplicity.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5A.2 | Create `DataFreshnessIndicator` composable — **PRIMITIVE PARAMS ONLY** (no Store types in core/ui): | NEW: `core/ui/src/commonMain/.../component/DataFreshnessIndicator.kt` | Compiles |

> **CRITICAL**: `core/ui` must NOT depend on `coreBase.store`. Use primitive params only.
> The ViewModel maps `StoreData.Origin` → `Boolean` before passing to UI state.

**T5A.2 implementation:**
```kotlin
// NO import of StoreData or any store types here — core/ui stays decoupled

/**
 * Shows data freshness status to the user.
 * Accepts PRIMITIVE params only — no Store types.
 * - isFreshData=true + not refreshing → hidden (data is fresh from network)
 * - isFreshData=false → "Last updated X ago" with refresh button
 * - isRefreshing → subtle progress indicator
 * - isNetworkAvailable=false → "Offline — showing cached data"
 */
@Composable
fun DataFreshnessIndicator(
    isFreshData: Boolean,           // true when data came from network (origin == NETWORK)
    lastFetchedAt: Long?,           // epoch millis from entity.lastFetchedAt
    isRefreshing: Boolean,          // background refresh in progress
    isNetworkAvailable: Boolean,    // from NetworkMonitor.isOnline
    onRefresh: () -> Unit,
    modifier: Modifier = Modifier,
) {
    when {
        !isNetworkAvailable -> {
            // Offline banner
            Surface(
                modifier = modifier.fillMaxWidth(),
                color = MaterialTheme.colorScheme.tertiaryContainer,
                tonalElevation = 1.dp,
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Icon(Icons.Outlined.CloudOff, contentDescription = null, modifier = Modifier.size(16.dp))
                    Text(
                        text = "Offline — showing cached data",
                        style = MaterialTheme.typography.labelMedium,
                    )
                    if (lastFetchedAt != null && lastFetchedAt > 0L) {
                        Text(
                            text = "· ${formatRelativeTime(lastFetchedAt)}",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onTertiaryContainer.copy(alpha = 0.7f),
                        )
                    }
                }
            }
        }
        isRefreshing -> {
            // Subtle refreshing indicator
            LinearProgressIndicator(
                modifier = modifier.fillMaxWidth().height(2.dp),
                color = MaterialTheme.colorScheme.primary,
                trackColor = MaterialTheme.colorScheme.surfaceVariant,
            )
        }
        !isFreshData && lastFetchedAt != null -> {
            // Stale data banner with refresh action
            Surface(
                modifier = modifier.fillMaxWidth(),
                color = MaterialTheme.colorScheme.surfaceVariant,
                tonalElevation = 0.dp,
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Icon(
                        Icons.Outlined.Schedule,
                        contentDescription = null,
                        modifier = Modifier.size(14.dp),
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        text = "Updated ${formatRelativeTime(lastFetchedAt)}",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.weight(1f),
                    )
                    TextButton(onClick = onRefresh, contentPadding = PaddingValues(horizontal = 8.dp)) {
                        Text("Refresh", style = MaterialTheme.typography.labelSmall)
                    }
                }
            }
        }
        // isFreshData == true → show nothing (data is fresh from network)
    }
}

/**
 * Formats a timestamp into a human-readable relative time.
 */
private fun formatRelativeTime(epochMillis: Long): String {
    val now = Clock.System.now().toEpochMilliseconds()
    val diff = now - epochMillis
    return when {
        diff < 60_000L -> "just now"
        diff < 3_600_000L -> "${diff / 60_000L} min ago"
        diff < 86_400_000L -> "${diff / 3_600_000L} hour${if (diff / 3_600_000L > 1) "s" else ""} ago"
        diff < 172_800_000L -> "yesterday"
        else -> "${diff / 86_400_000L} days ago"
    }
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5A.3 | Create `CachedData<T>` wrapper + `toCachedDataState()` extension — bridges `StoreData` → mifos `DataState`: | NEW: `core/data/src/commonMain/.../utils/StoreDataState.kt` | Compiles |

> **CRITICAL**: Uses `org.mifos.mobile.core.common.DataState` (Loading/Success/Error) — NOT `template.core.base.common.DataState`.
> All ViewModels use the mifos DataState. The template DataState (with Pending/NoNetwork) is NEVER exposed to consumers.

**T5A.3 implementation:**
```kotlin
import org.mifos.mobile.core.common.DataState  // MIFOS version, NOT template version
import template.core.base.store.StoreData

/**
 * UI-ready wrapper that carries both domain data AND freshness metadata.
 * ViewModels expose CachedData<T> in their state, then map to primitive params for UI.
 */
@Immutable
data class CachedData<T>(
    val data: T,
    val isFreshData: Boolean,       // true when origin == NETWORK
    val lastFetchedAt: Long?,       // epoch millis for staleness display
    val isRefreshing: Boolean,
)

/**
 * Extension to convert Flow<StoreData<T>> into Flow<DataState<CachedData<T>>>
 * using the MIFOS DataState (Loading/Success/Error), NOT the template DataState.
 */
fun <T> Flow<StoreData<T>>.toCachedDataState(): Flow<DataState<CachedData<T>>> = this.map { storeData ->
    when {
        storeData.error != null -> DataState.Error(storeData.error!!)
        storeData.data != null -> DataState.Success(
            CachedData(
                data = storeData.data!!,
                isFreshData = storeData.origin == StoreData.Origin.NETWORK,
                lastFetchedAt = storeData.fetchedAt,
                isRefreshing = storeData.isRefreshing,
            )
        )
        else -> DataState.Loading
    }
}
```

#### 5B — Full Offline Repositories (Store 5 + SourceOfTruth)

> **CRITICAL PATTERN RULES** (apply to ALL repos in this phase):
> 1. `Fetcher.of { }` requires a **suspend lambda**. Ktorfit services return `Flow<T>`. Use `.first()` to convert.
> 2. Mapper convention: `.toModel()` for entity→domain, `.toEntity()` for domain→entity. NEVER `.toDomain()`.
> 3. Writer lambda must pass `lastFetchedAt = Clock.System.now().toEpochMilliseconds()` to `.toEntity()`.
> 4. Only **read methods** (returning `Flow`) become Store-wrapped. Mutation methods stay `suspend fun: DataState<T>`.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5B.1 | Wrap `ClientChargeRepository` with Store 5 (existing DAO — template pattern): | `core/data/.../repository/ClientChargeRepositoryImpl.kt` | Compiles |

**T5B.1 implementation (template for all cached repos):**
```kotlin
class ClientChargeRepositoryImpl(
    private val apiService: ClientChargeService,
    private val chargeDao: ChargeDao,
) : ClientChargeRepository {

    private val chargeStore = StoreFactory.createStore(
        fetcher = Fetcher.of { clientId: Long ->
            apiService.getClientChargeList(clientId).first()  // .first() — Ktorfit returns Flow, Fetcher needs suspend
        },
        sourceOfTruth = SourceOfTruth.of(
            reader = { clientId: Long ->
                chargeDao.getChargesByClientId(clientId)
                    .map { entities -> entities.map { it.toModel() } }  // .toModel() NOT .toDomain()
            },
            writer = { clientId: Long, charges: Page<ChargeDto> ->
                chargeDao.insertAll(charges.pageItems.map {
                    it.toEntity(clientId, lastFetchedAt = Clock.System.now().toEpochMilliseconds())
                })
            },
            delete = { clientId: Long -> chargeDao.deleteByClientId(clientId) },
            deleteAll = { chargeDao.deleteAll() },
        ),
        validator = DefaultValidator.withTtl(15.minutes),
    )

    override fun getClientCharges(clientId: Long): Flow<StoreData<List<Charge>>> =
        chargeStore.streamData(key = clientId, refresh = true)

    override fun refreshCharges(clientId: Long): Flow<StoreData<List<Charge>>> =
        chargeStore.freshData(key = clientId)
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5B.2 | Wrap `NotificationRepository` — uncomment DAO calls, wire Store 5 with MifosNotificationDao | `core/data/.../repository/NotificationRepositoryImpl.kt` | Compiles |
| T5B.3 | Wrap `HomeRepository` / `ClientRepository` with Store 5 + ClientDao + ClientAccountsDao: | `core/data/.../repository/HomeRepositoryImpl.kt` | Compiles |

**T5B.3 implementation (multi-store per repository):**
```kotlin
class HomeRepositoryImpl(
    private val clientService: ClientService,
    private val clientDao: ClientDao,
    private val clientAccountsDao: ClientAccountsDao,
) : HomeRepository {

    private val clientStore = StoreFactory.createStore(
        fetcher = Fetcher.of { clientId: Long ->
            clientService.getClientForId(clientId).first()  // .first() — Flow→suspend
        },
        sourceOfTruth = SourceOfTruth.of(
            reader = { clientId: Long ->
                clientDao.getClient(clientId).map { it?.toModel() }  // .toModel() NOT .toDomain()
            },
            writer = { clientId: Long, dto: ClientResponseDto ->
                clientDao.insert(dto.toEntity(lastFetchedAt = Clock.System.now().toEpochMilliseconds()))
            },
            delete = { _: Long -> },
            deleteAll = { clientDao.deleteAll() },
        ),
        validator = DefaultValidator.withTtl(30.minutes),
    )

    private val accountsStore = StoreFactory.createStore(
        fetcher = Fetcher.of { clientId: Long ->
            clientService.getClientAccounts(clientId).first()  // .first() — Flow→suspend
        },
        sourceOfTruth = SourceOfTruth.of(
            reader = { clientId: Long ->
                clientAccountsDao.getByClientId(clientId).map { it?.toModel() }  // .toModel()
            },
            writer = { clientId: Long, dto: AccountsResponseDto ->
                clientAccountsDao.insert(dto.toEntity(clientId, lastFetchedAt = Clock.System.now().toEpochMilliseconds()))
            },
            delete = { clientId: Long -> clientAccountsDao.deleteByClientId(clientId) },
            deleteAll = { clientAccountsDao.deleteAll() },
        ),
        validator = DefaultValidator.withTtl(15.minutes),
    )

    override fun currentClient(clientId: Long): Flow<StoreData<Client>> =
        clientStore.streamData(key = clientId, refresh = true)

    override fun clientAccounts(clientId: Long): Flow<StoreData<ClientAccounts>> =
        accountsStore.streamData(key = clientId, refresh = true)
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5B.4 | Wrap `AccountsRepository` with Store 5 + ClientAccountsDao | `core/data/.../repository/AccountsRepositoryImpl.kt` | Compiles |
| T5B.5 | Wrap `LoanRepository` with Store 5 + LoanDetailsDao (full detail JSON cache) + LoanAccountDao (list cache) | `core/data/.../repository/LoanRepositoryImpl.kt` | Compiles |

**T5B.5 loan detail store pattern (JSON blob for complex nested objects):**
```kotlin
private val loanDetailStore = StoreFactory.createStore(
    fetcher = Fetcher.of { key: LoanDetailKey ->
        apiService.getLoanWithAssociations(key.loanId, key.associationType).first()  // .first() — Flow→suspend
    },
    sourceOfTruth = SourceOfTruth.of(
        reader = { key: LoanDetailKey ->
            loanDetailsDao.getLoanDetails(key.loanId).map { entity ->
                entity?.let { Json.decodeFromString<LoanWithAssociations>(fieldEncryptor.decrypt(it.detailsJson)) }
            }
        },
        writer = { key: LoanDetailKey, dto: LoanWithAssociationsResponseDto ->
            loanDetailsDao.insert(LoanDetailsEntity(
                loanId = key.loanId,
                detailsJson = fieldEncryptor.encrypt(Json.encodeToString(dto.toDomain())),
                lastFetchedAt = Clock.System.now().toEpochMilliseconds(),
            ))
        },
        delete = { key: LoanDetailKey -> loanDetailsDao.delete(key.loanId) },
        deleteAll = { loanDetailsDao.deleteAll() },
    ),
    validator = DefaultValidator.withTtl(10.minutes),
)

data class LoanDetailKey(val loanId: Long, val associationType: String?)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5B.6 | Wrap `SavingsAccountRepository` with Store 5 + SavingsDetailsDao + SavingsAccountDao | `core/data/.../repository/SavingsAccountRepositoryImpl.kt` | Compiles |
| T5B.7 | Wrap `ShareAccountRepository` with Store 5 + ShareAccountDao | `core/data/.../repository/ShareAccountRepositoryImpl.kt` | Compiles |
| T5B.8 | Wrap `BeneficiaryRepository` with Store 5 + BeneficiaryDao | `core/data/.../repository/BeneficiaryRepositoryImpl.kt` | Compiles |
| T5B.9 | Wrap `RecentTransactionRepository` with Store 5 + TransactionDao | `core/data/.../repository/RecentTransactionRepositoryImpl.kt` | Compiles |
| T5B.10 | Wrap `GuarantorRepository` with Store 5 + GuarantorDao (list by loanId) | `core/data/.../repository/GuarantorRepositoryImpl.kt` | Compiles |

#### 5C — Memory-Only Stores (Templates + Ephemeral Data)

> Templates are fetched per-interaction and change server-side frequently. Memory cache with short TTL is sufficient.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5C.1 | Wrap template methods in LoanRepository with `createMemoryStore`: | Already in `LoanRepositoryImpl.kt` | Compiles |

**T5C.1 pattern:**
```kotlin
private val loanTemplateStore = StoreFactory.createMemoryStore(
    fetcher = Fetcher.of { clientId: Long ->
        apiService.getLoanTemplate(clientId).first()  // .first() — Ktorfit returns Flow, Fetcher needs suspend
    }
)
override fun template(clientId: Long): Flow<StoreData<LoanTemplate?>> =
    loanTemplateStore.streamData(key = clientId, refresh = true)
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5C.2 | Wrap `SavingsAccountTemplate` methods with `createMemoryStore` | `SavingsAccountRepositoryImpl.kt` | Compiles |
| T5C.3 | Wrap `ThirdPartyTransferRepository.thirdPartyTransferTemplate()` with `createMemoryStore` | `ThirdPartyTransferRepositoryImpl.kt` | Compiles |
| T5C.4 | Wrap `BeneficiaryRepository.beneficiaryTemplate()` with `createMemoryStore` | `BeneficiaryRepositoryImpl.kt` | Compiles |
| T5C.5 | Wrap `GuarantorRepository.getGuarantorTemplate()` with `createMemoryStore` | `GuarantorRepositoryImpl.kt` | Compiles |
| T5C.6 | Wrap `ShareAccountRepository.getShareProducts()` with `createMemoryStore` | `ShareAccountRepositoryImpl.kt` | Compiles |

#### 5D — ViewModel Integration + Staleness UI Wiring

> ViewModels must carry `CachedData<T>` instead of raw `T` to surface freshness info to UI.
> Screens render `DataFreshnessIndicator` at the top, driven by the state.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5D.1 | Update `HomeViewModel` — add freshness fields to `HomeState`: | `feature/home/.../HomeViewModel.kt` | Compiles |

**T5D.1 state update pattern:**
```kotlin
@Immutable
data class HomeState(
    // ... existing fields ...
    // NEW: freshness metadata — PRIMITIVE types only (no StoreData.Origin import in feature modules)
    val isFreshData: Boolean = true,
    val lastFetchedAt: Long? = null,
    val isRefreshing: Boolean = false,
)

// In HomeViewModel, when collecting from repository:
repository.clientAccounts(clientId)
    .toCachedDataState()  // produces Flow<DataState<CachedData<T>>> using MIFOS DataState
    .collect { dataState ->
        when (dataState) {
            is DataState.Success -> {
                sendState {
                    copy(
                        uiState = HomeScreenState.Success,
                        // Map account data ...
                        isFreshData = dataState.data.isFreshData,        // Boolean — already mapped in CachedData
                        lastFetchedAt = dataState.data.lastFetchedAt,    // Long? — epoch millis
                        isRefreshing = dataState.data.isRefreshing,      // Boolean
                    )
                }
            }
            // ... error, loading
        }
    }
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5D.2 | Update `HomeScreen` — add `DataFreshnessIndicator` below NetworkBanner: | `feature/home/.../HomeScreen.kt` | UI shows staleness |

**T5D.2 screen integration pattern:**
```kotlin
@Composable
fun HomeScreen(state: HomeState, onAction: (HomeAction) -> Unit) {
    Column {
        // Staleness indicator — primitive params, no Store types in UI layer
        DataFreshnessIndicator(
            isFreshData = state.isFreshData,              // Boolean
            lastFetchedAt = state.lastFetchedAt,          // Long?
            isRefreshing = state.isRefreshing,             // Boolean
            isNetworkAvailable = state.networkStatus,      // Boolean from NetworkMonitor
            onRefresh = { onAction(HomeAction.OnRefresh) },
        )
        // ... rest of screen content
    }
}
```

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T5D.3 | Add `OnRefresh` action to HomeAction + handler in ViewModel | Same files | Refresh works |
| T5D.4 | Update `AccountsViewModel` + `AccountsScreen` with staleness fields + indicator | `feature/accounts/` | UI shows staleness |
| T5D.5 | Update `LoanAccountDetailViewModel` + screen with staleness | `feature/loan-account/` | UI shows staleness |
| T5D.6 | Update `SavingsAccountDetailViewModel` + screen with staleness | `feature/savings-account/` | UI shows staleness |
| T5D.7 | Update `BeneficiaryListViewModel` + screen with staleness | `feature/beneficiary/` | UI shows staleness |
| T5D.8 | Update `RecentTransactionViewModel` + screen with staleness | `feature/recent-transaction/` | UI shows staleness |
| T5D.9 | Update `NotificationViewModel` + screen with staleness | `feature/notification/` | UI shows staleness |
| T5D.10 | Update `ClientChargeViewModel` + screen with staleness | `feature/charge/` | UI shows staleness |
| T5D.11 | Update `GuarantorListViewModel` + screen with staleness | `feature/guarantor/` | UI shows staleness |
| T5D.12 | Add `AppStoreModule` to `KoinModules.allModules` (after DatabaseModule, before featureModules) | `cmp-navigation/.../di/KoinModules.kt` | Koin resolves |

### Phase 6 — DI Wiring (Final Order)
> **GATE**: Phase 5 must verify at least one Store compiles and returns data.

| Task | Description | Files | Verify |
|------|-------------|-------|--------|
| T6.1 | Enforce final module order in `KoinModules.allModules`: | `cmp-navigation/.../di/KoinModules.kt` | App starts without Koin errors |

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
    featureModules,        // 8. Features — ViewModels consuming repositories
    sharedModule,          // 9. Navigation ViewModels
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
        MifosMobileTheme(darkTheme = uiState.darkTheme, ...) {
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
| T7.2 | Optional: Override `SecurityPolicy` in DI for custom timeout (default 30 min). For a banking app, consider shorter timeout: | DI override in KoinModules | Policy applied |

**T7.2 optional override:**
```kotlin
// In sharedModule or a securityOverrideModule:
single { SecurityPolicy(sessionTimeoutMinutes = 15, requireBiometricForSensitiveOps = true) }
```

### Phase 8 — Verification
> **GATE**: Phase 7 must verify SecurityGate wraps the app correctly.

#### 8A — Build Verification (all platforms)

| Task | Description | Command | Verify |
|------|-------------|---------|--------|
| T8A.1 | Build demo debug APK | `./gradlew :cmp-android:assembleDemoDebug` | Exit 0 |
| T8A.2 | Static analysis | `./gradlew spotlessCheck detekt` | Exit 0 |
| T8A.3 | iOS KSP (verifies TypeConverters with `@kotlin.concurrent.Volatile`) | `./gradlew :core:database:kspKotlinIosArm64` | Exit 0 |
| T8A.4 | iOS framework link | `./gradlew :cmp-shared:linkDebugFrameworkIosArm64` | Exit 0 |
| T8A.5 | Desktop build | `./gradlew :cmp-desktop:jar` | Exit 0 |

#### 8B — Security + DataStore Verification

| Task | Description | Command | Verify |
|------|-------------|---------|--------|
| T8B.1 | Encryption roundtrip test: encrypt a TypeConverter value, read it back, verify `ENC:` prefix and correct decryption | Unit test | Values match |
| T8B.2 | DataStore audit: verify sensitive fields (token, passcode, authKey, userId) are in secureSettings, NOT plainSettings | Read UserPreferencesDataSource | All sensitive in secure |

#### 8C — Offline + Staleness Verification

| Task | Description | Command | Verify |
|------|-------------|---------|--------|
| T8C.1 | **Store 5 online test**: fresh fetch returns `StoreData` with `origin = NETWORK` | Unit test or manual | `isFreshData = true` |
| T8C.2 | **Store 5 offline test**: disable network → open any list screen → data loads from cache | Manual (airplane mode) | Screen shows cached data |
| T8C.3 | **Staleness UI test**: cached data shows "Updated X min ago" banner with Refresh button | Manual | Banner visible |
| T8C.4 | **Refresh test**: tap Refresh on stale data banner → data refreshes → banner disappears | Manual | Banner hidden after refresh |
| T8C.5 | **Offline banner test**: airplane mode → shows "Offline — showing cached data" | Manual | Offline banner visible |
| T8C.6 | **Database migration test**: v1→v2 migration succeeds (existing Charge + Notification data preserved OR destructive migration confirmed for dev) | Manual | No crash on upgrade |
| T8C.7 | **All 12 DAOs resolvable**: Koin provides all 12 DAOs without circular dependency or missing binding | `./gradlew :cmp-android:assembleDemoDebug` + app launch | No Koin errors |
| T8C.8 | **Mapper correctness**: verify at least one entity↔domain roundtrip preserves all fields (e.g., `charge.toEntity().toModel() == charge`) | Unit test | Fields match |
| T8C.9 | **Network monitor integration**: verify `NetworkMonitor.isOnline` updates `isNetworkAvailable` in at least one ViewModel state | Manual (toggle airplane mode) | State updates |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Alpha dependencies** (Room 3.0.0-alpha03, Store 5.1.0-alpha08) | **HIGH** | Pin exact versions, test all platforms, prepare for breaking API changes on upgrade. Monitor release notes. |
| Room 2→3 breaking changes (import paths) | Medium | Small existing entity set (2), typealiases handle most. Only 2 files need import changes. |
| 10 new entities — schema design | Medium | Entities modeled directly from API DTOs + domain models |
| ChargeEntity.clientId type change (Int→Long) | Medium | Requires destructive migration or manual ALTER TABLE. Use destructive for dev. |
| Two incompatible DataState types | **HIGH** | Bridge via `CachedData<T>` wrapper. NEVER expose template DataState to ViewModels. Use `org.mifos.mobile.core.common.DataState` everywhere. |
| Fetcher.of() + Ktorfit Flow mismatch | Medium | ALL fetchers use `.first()` to convert. Pattern is documented — apply consistently. |
| TypeConverter encryption backward compat | Low | `ENC:` prefix detection handles legacy unencrypted data |
| Store 5 adoption for 17 repos | Medium | Consistent pattern (5B template), repeat for each repo. Only 10 need SourceOfTruth. |
| Detail screens offline (JSON blob entities) | Low | LoanDetailsEntity/SavingsDetailsEntity store full encrypted JSON — simple but large |
| iOS KSP PROCESSING_ERROR | Medium | Use `@kotlin.concurrent.Volatile`, not `@Volatile` |
| Staleness UI across all screens | Low | Single shared `DataFreshnessIndicator` composable with primitive params |
| Database version migration (v1→v2) | Medium | `fallbackToDestructiveMigration` for dev, proper AutoMigration for prod |

## Estimated Effort

| Phase | Effort | Notes |
|-------|--------|-------|
| Phase 0 (sync-dirs) | 15 min | |
| Phase 1 (Gradle verification) | **10 min** | Mostly verify — 2 new additions only |
| Phase 2 (Security verification) | **10 min** | All verify — already implemented |
| Phase 3A (Verify + fix ChargeEntity/DAO/mappers) | 30 min | Fix gaps in existing code |
| Phase 3B-3C (10 new entities + 10 new DAOs) | 2-3 hours | Main new work |
| Phase 3B-extra (10 new mapper files) | 1 hour | 3 mappers per entity |
| Phase 3D-3F (TypeConverters + AppDatabase + DI + verify) | 1 hour | |
| Phase 4 (DataStore verification) | **10 min** | All verify — already implemented |
| Phase 5A (staleness UI + CachedData wrapper) | 1 hour | DataFreshnessIndicator + toCachedDataState |
| Phase 5B (10 offline repos with SourceOfTruth) | 3-4 hours | Main Store 5 work |
| Phase 5C (6 memory-only template stores) | 30 min | Simple pattern |
| Phase 5D (ViewModel + screen staleness wiring — 9 screens) | 2-3 hours | Repetitive but per-screen |
| Phase 6 (DI order verification) | **10 min** | Verify + minor reorder |
| Phase 7 (SecurityGate) | 15 min | |
| Phase 8 (Verification — build + offline + staleness) | 1-2 hours | Expanded with offline tests |
| **Total** | **~13-17 hours** | Reduced: Phase 1, 2, 4 are now verify-only |

---

## Session Strategy

Execute in a **dedicated session** per phase group:
- **Session 1**: Phase 0-2 (sync-dirs + Gradle verify + Security verify) — mostly verification, fast
- **Session 2**: Phase 3A-3C + 3B-extra (fix ChargeEntity/DAO gaps + new entities + new DAOs + new mappers)
- **Session 3**: Phase 3D-3F + Phase 4 (TypeConverters + AppDatabase + DI + DataStore verify)
- **Session 4**: Phase 5A-5B (staleness UI components + CachedData wrapper + 10 offline repos with SourceOfTruth)
- **Session 5**: Phase 5C-5D (memory stores + ViewModel/screen staleness wiring for 9 screens)
- **Session 6**: Phase 6-8 (DI order + SecurityGate + full verification including offline + staleness tests)

## Gap Fix Summary (22 items)

All 22 gaps identified in the audit have been addressed:

| # | Gap | Fix Applied |
|---|-----|-------------|
| 1 | Repo count wrong (15→17) | Corrected to 17 in Offline Support Strategy |
| 2 | DataState type clash | `CachedData<T>` bridges to mifos DataState; template DataState never exposed |
| 3 | Suspend vs Flow (Fetcher.of) | ALL fetcher calls use `.first()` |
| 4 | ChargeDao missing queries | T3A.4 adds `getChargesByClientId`, `deleteByClientId`, `deleteAll` |
| 5 | Fetcher.of() needs .first() | Applied to ALL code snippets (T5B, T5C) |
| 6 | Mappers commented out | T3A.5 uncomments + fixes naming |
| 7 | Repo impls are stubs | T5B reconstructs all repos with Store 5 |
| 8 | AppDatabase already has @ConstructedBy | T3E.1 notes "ALREADY EXISTS — verify, do not re-add" |
| 9 | core/ui no Store dep | DataFreshnessIndicator uses primitive params only |
| 10 | AppStoreModule already exists | T5A.1 changed to VERIFY |
| 11 | PreferencesModule already dual-store | Phase 4 changed to verification-only |
| 12 | Two BaseViewModel classes | Plan uses mifos BaseViewModel<State, Event, Action> |
| 13 | Alpha deps risk | Risk elevated to HIGH |
| 14 | .toDomain() → .toModel() | ALL snippets corrected |
| 15 | ChargeEntity.clientId Int→Long | T3A.3 fixes type + migration note |
| 16 | ChargeResponseDto→ChargeEntity missing | T3A.5 creates new mapper |
| 17 | SecurityModule already first | Phase 2 changed to verify |
| 18 | Room/Store versions already correct | Phase 1 changed to verify |
| 19 | core/data already has store deps | T1.3 changed to VERIFY |
| 20 | AppDatabase autoMigration | T3E.1 adds AutoMigration + migration strategy note |
| 21 | StoreData.Origin in ViewModel state | Changed to primitive `isFreshData: Boolean` + `lastFetchedAt: Long?` |
| 22 | Effort overestimated | Reduced Phase 1, 2, 4 to verify-only (~13-17h total) |
