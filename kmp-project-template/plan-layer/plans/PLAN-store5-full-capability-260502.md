# PLAN-store5-full-capability-260502: Store5 Full Capability Adoption

| Field | Value |
|-------|-------|
| ID | store5-full-capability-260502 |
| Status | Completed |
| Priority | P1 |
| Scope | `core-base/store` + `core/data` + `core/database` |
| Created | 2026-05-02 |
| Updated | 2026-05-02 |
| Prerequisites | PLAN-store-architecture-v2-260502 (completed) |
| Effort | ~8-10 hours (4 phases) |
| Parent Plan | PLAN-store-architecture-v2-260502 |
| New Deps | None (all Store5 APIs already available at v5.1.0-alpha08) |
| DI Framework | **Koin** |

---

## Problem Statement

After completing the Store Architecture V2 plan, we are leveraging ~50% of Store5's capabilities. The audit identified unused features that directly impact security, data freshness, and future write-operation support.

### Current State (What's Used)
- `Fetcher` — all 4 stores
- `SourceOfTruth` (reader/writer/delete/deleteAll) — all 4 stores
- `Store` (read-only) via `StoreFactory.createStore()` — all 4 stores
- `StoreReadRequest.cached/fresh/localOnly` — 3 of 4 request variants
- `StoreReadResponse` full variant handling (Data/Error/Loading/NoNewData/Initial)
- `StoreReadResponseOrigin` mapping to `DataOrigin`

### What's NOT Used (Audit Findings)

| # | Feature | Impact | Effort |
|---|---------|--------|--------|
| F-1 | **Validator (TTL cache invalidation)** — `DefaultValidator` exists but not wired | HIGH — stale financial data served indefinitely | LOW |
| F-2 | **store.clear(key) / clearAll()** — no cache invalidation on logout | CRITICAL — previous user data leaks | LOW |
| F-3 | **MutableStore + Updater + Bookkeeper** — write-back infrastructure unused | MEDIUM — no offline-first writes | HIGH |
| F-4 | **Converter** — no Network/Local/Output type separation | LOW — same type used throughout | MEDIUM |
| F-5 | **StoreReadRequest.skipMemory()** — not exposed | LOW — freshData() covers most cases | LOW |
| F-6 | **Cache5 memory policies** — no eviction configured | LOW — datasets small | LOW |
| F-7 | **Persistent Bookkeeper** — InMemoryBookkeeper loses state on process death | MEDIUM — offline sync breaks on restart | MEDIUM |

---

## Phase 1: Validator TTL Integration (F-1)

**Goal:** Wire `DefaultValidator` into all 4 stores so stale cached data triggers automatic re-fetch.

### Step 1.1: Define TTL Constants in ApplicationStoreRegistry

**File:** `core/data/src/commonMain/.../di/ApplicationStoreRegistry.kt`

```kotlin
object ApplicationStoreRegistry : StoreRegistry() {
    val ExchangeRates = store("exchangeRates")
    val RateHistory = store("rateHistory")
    val CoinMarkets = store("coinMarkets")
    val CoinDetail = store("coinDetail")

    // TTL durations — financial data has different freshness requirements
    object Ttl {
        val EXCHANGE_RATES = 5.minutes    // Forex rates update frequently
        val RATE_HISTORY = 1.hours        // Historical data is stable
        val COIN_MARKETS = 2.minutes      // Crypto prices are volatile
        val COIN_DETAIL = 5.minutes       // Detail page staleness threshold
    }
}
```

### Step 1.2: Wire Validator into Each Store Provider

**File:** `core/data/src/commonMain/.../store/ExchangeRatesStore.kt`

Add `DefaultValidator.withTtl(ApplicationStoreRegistry.Ttl.EXCHANGE_RATES)` as the `validator` param to `StoreFactory.createStore()`.

**Repeat for all 4 stores:**

| Store | TTL | Rationale |
|-------|-----|-----------|
| ExchangeRates | 5 min | Forex rates change during trading hours |
| RateHistory | 1 hour | Historical data rarely changes intraday |
| CoinMarkets | 2 min | Crypto prices are highly volatile |
| CoinDetail | 5 min | Detail data like market cap changes moderately |

### Step 1.3: Handle Validator.markFresh() in StoreDataMapper

The `DefaultValidator` needs `markFresh()` called when network data arrives. Currently `lastFetchMark` is set in `mapToStoreData*` — the Validator must be passed into the mapper or marked externally.

**Option A (Preferred):** Since Store5 calls `Validator.isValid()` internally on cached reads, and `DefaultValidator` tracks its own `lastFetchMark` via `markFresh()`, we need the Store to call `markFresh()` after each successful fetch. This should be done in the SourceOfTruth writer:

```kotlin
sourceOfTruth = SourceOfTruth.of(
    reader = { ... },
    writer = { key, data ->
        validator.markFresh()  // Mark fresh BEFORE writing to DB
        dao.upsert(data.toEntity(key))
    },
    ...
)
```

**Option B:** Create a `ValidatingSourceOfTruth` wrapper in core-base/store that auto-calls `markFresh()` on write.

### Step 1.4: Update StoreFactory.createStore() Usage

Current signature already accepts `validator: Validator<Output>? = null`. No factory changes needed — just pass the validator at each call site.

### Files Modified
- `core/data/src/commonMain/.../di/ApplicationStoreRegistry.kt` — add Ttl constants
- `core/data/src/commonMain/.../store/ExchangeRatesStore.kt` — add validator param
- `core/data/src/commonMain/.../store/CoinDetailStore.kt` — add validator param
- `core/data/src/commonMain/.../store/CoinMarketsStore.kt` — add validator param
- `core/data/src/commonMain/.../store/RateHistoryStore.kt` — add validator param

### Verification
- Unit test: Create store with 1-second TTL, verify `stream()` re-fetches after TTL expires
- Unit test: Verify `markFresh()` resets TTL timer
- Manual: Open exchange rates, wait 5 min, observe auto-refresh

---

## Phase 2: Cache Invalidation on Logout (F-2)

**Goal:** Clear all Store caches when user logs out to prevent data leakage.

### Step 2.1: Create StoreCacheManager Interface

**File:** `core/data/src/commonMain/.../repository/StoreCacheManager.kt`

```kotlin
interface StoreCacheManager {
    /** Clears all store caches (in-memory + database). Call on logout. */
    suspend fun clearAll()
}
```

### Step 2.2: Implement StoreCacheManagerImpl

**File:** `core/data/src/commonMain/.../repositoryImpl/StoreCacheManagerImpl.kt`

```kotlin
class StoreCacheManagerImpl(
    private val exchangeRatesStore: Store<String, ExchangeRates>,
    private val rateHistoryStore: Store<RateHistoryKey, RateHistory>,
    private val coinMarketsStore: Store<PageKey, List<CoinMarket>>,
    private val coinDetailStore: Store<String, CoinDetail>,
    private val exchangeRatesDao: ExchangeRatesDao,
    private val coinMarketDao: CoinMarketDao,
    private val coinDetailDao: CoinDetailDao,
    private val rateHistoryDao: RateHistoryDao,
) : StoreCacheManager {

    override suspend fun clearAll() {
        // Clear Store in-memory caches
        exchangeRatesStore.clear()
        rateHistoryStore.clear()
        coinMarketsStore.clear()
        coinDetailStore.clear()

        // Clear database tables (SourceOfTruth)
        exchangeRatesDao.deleteAll()
        coinMarketDao.deleteAll()
        coinDetailDao.deleteAll()
        rateHistoryDao.deleteAll()
    }
}
```

### Step 2.3: Register in Koin

**File:** `core/data/src/commonMain/.../di/RepositoryModule.kt`

```kotlin
single<StoreCacheManager> {
    StoreCacheManagerImpl(
        exchangeRatesStore = get(ApplicationStoreRegistry.ExchangeRates),
        rateHistoryStore = get(ApplicationStoreRegistry.RateHistory),
        coinMarketsStore = get(ApplicationStoreRegistry.CoinMarkets),
        coinDetailStore = get(ApplicationStoreRegistry.CoinDetail),
        exchangeRatesDao = get(),
        coinMarketDao = get(),
        coinDetailDao = get(),
        rateHistoryDao = get(),
    )
}
```

### Step 2.4: Integrate with UserLogoutManagerImpl

**File:** `core/data/src/commonMain/.../repositoryImpl/UserLogoutManagerImpl.kt`

```kotlin
class UserLogoutManagerImpl(
    private val repository: UserPreferencesRepository,
    private val storeCacheManager: StoreCacheManager,
    dispatcherManager: DispatcherManager,
) : UserLogoutManager {

    private fun clearUserData() {
        scope.launch {
            repository.clearUserData()
            storeCacheManager.clearAll()  // NEW — clear all cached store data
        }
    }
}
```

### Files Modified
- `core/data/src/commonMain/.../repository/StoreCacheManager.kt` — NEW interface
- `core/data/src/commonMain/.../repositoryImpl/StoreCacheManagerImpl.kt` — NEW implementation
- `core/data/src/commonMain/.../di/RepositoryModule.kt` — register StoreCacheManager
- `core/data/src/commonMain/.../repositoryImpl/UserLogoutManagerImpl.kt` — inject + call clearAll()

### Verification
- Unit test: Mock stores + DAOs, verify clearAll() calls `store.clear()` and `dao.deleteAll()` for each
- Manual: Login, load exchange rates, logout, login as different user, verify no stale data shown

---

## Phase 3: skipMemory Request + Cache Eviction (F-5, F-6)

**Goal:** Expose `skipMemory` request type and configure memory cache eviction policies.

### Step 3.1: Add skipMemory Extension to StoreDataExtensions

**File:** `core-base/store/src/commonMain/.../StoreDataExtensions.kt`

```kotlin
/**
 * Bypasses in-memory cache, reads from SourceOfTruth + optional network refresh.
 * Useful when you know in-memory state may be stale but disk is authoritative.
 */
fun <Key : Any, Output : Any> Store<Key, Output>.skipMemoryData(
    key: Key,
    refresh: Boolean = true,
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    return stream(StoreReadRequest.skipMemory(key, refresh))
        .mapToStoreDataNoFallback(isEmpty)
}
```

### Step 3.2: Configure Memory Cache Policy in StoreFactory

**File:** `core-base/store/src/commonMain/.../StoreFactory.kt`

Store5 uses `MemoryPolicy` (from `store5-cache`) to control in-memory cache behavior. Add an optional param:

```kotlin
fun <Key : Any, Input : Any, Output : Any> createStore(
    fetcher: Fetcher<Key, Input>,
    sourceOfTruth: SourceOfTruth<Key, Input, Output>,
    validator: Validator<Output>? = null,
    memoryPolicy: MemoryPolicy<Key, Output>? = null,
): Store<Key, Output> {
    var builder = StoreBuilder.from(fetcher, sourceOfTruth)
    if (validator != null) builder = builder.validator(validator)
    if (memoryPolicy != null) builder = builder.cachePolicy(memoryPolicy)
    return builder.build()
}
```

### Step 3.3: Apply Default Memory Policies

Use sensible defaults per store type:

| Store | Max Items | Expire After | Rationale |
|-------|-----------|-------------|-----------|
| ExchangeRates | 10 | 10 min | Few base currencies cached |
| RateHistory | 20 | 30 min | Multiple currency pair histories |
| CoinMarkets | 5 | 5 min | Few pages of market data |
| CoinDetail | 50 | 15 min | Users browse many coins |

### Files Modified
- `core-base/store/src/commonMain/.../StoreDataExtensions.kt` — add `skipMemoryData()`
- `core-base/store/src/commonMain/.../StoreFactory.kt` — add `memoryPolicy` param
- `core/data/src/commonMain/.../store/*.kt` — pass memory policies

### Verification
- Unit test: Verify `skipMemoryData()` doesn't return stale in-memory data
- Unit test: Verify memory policy evicts entries beyond max size

---

## Phase 4: MutableStore Foundation (F-3, F-7)

**Goal:** Establish the write-back pattern using MutableStore + Updater + persistent Bookkeeper, ready for when write operations are needed.

### Step 4.1: Create Room-backed Persistent Bookkeeper

**File:** `core/database/src/commonMain/.../entity/BookkeeperEntity.kt`

```kotlin
@Entity(tableName = "store_bookkeeper")
data class BookkeeperEntity(
    @PrimaryKey val key: String,
    val lastFailedSync: Long,
)
```

**File:** `core/database/src/commonMain/.../dao/BookkeeperDao.kt`

```kotlin
@Dao
interface BookkeeperDao {
    @Query("SELECT lastFailedSync FROM store_bookkeeper WHERE `key` = :key")
    suspend fun getLastFailedSync(key: String): Long?

    @Upsert
    suspend fun upsert(entity: BookkeeperEntity)

    @Query("DELETE FROM store_bookkeeper WHERE `key` = :key")
    suspend fun delete(key: String)

    @Query("DELETE FROM store_bookkeeper")
    suspend fun deleteAll()
}
```

### Step 4.2: Create RoomBookkeeper Adapter

**File:** `core/data/src/commonMain/.../store/RoomBookkeeper.kt`

```kotlin
class RoomBookkeeper<Key : Any>(
    private val dao: BookkeeperDao,
    private val keySerializer: (Key) -> String,
) : Bookkeeper<Key> {

    override suspend fun getLastFailedSync(key: Key): Long? =
        dao.getLastFailedSync(keySerializer(key))

    override suspend fun setLastFailedSync(key: Key, timestamp: Long): Boolean {
        dao.upsert(BookkeeperEntity(key = keySerializer(key), lastFailedSync = timestamp))
        return true
    }

    override suspend fun clear(key: Key): Boolean {
        dao.delete(keySerializer(key))
        return true
    }

    override suspend fun clearAll(): Boolean {
        dao.deleteAll()
        return true
    }
}
```

### Step 4.3: Create Example MutableStore (User Preferences Sync)

Demonstrate the full write-back pattern with a concrete use case. When the project adds user-modifiable data (e.g., watchlist, favorites, settings sync), use this template:

**File:** `core/data/src/commonMain/.../store/MUTABLE_STORE_TEMPLATE.md`

Document the pattern for creating a MutableStore:

```kotlin
// 1. Define types
//    Network = API response DTO
//    Local = Room Entity
//    Output = Domain model

// 2. Create Converter
val converter = Converter.Builder<NetworkDto, LocalEntity, DomainModel>()
    .fromNetworkToLocal { dto -> dto.toEntity() }
    .fromOutputToLocal { model -> model.toEntity() }
    .fromLocalToOutput { entity -> entity.toDomain() }
    .build()

// 3. Create Updater (write-back to server)
val updater = Updater.by { key, output ->
    api.update(key, output.toDto())
    UpdaterResult.Success.Typed(output)
}

// 4. Create Bookkeeper (persistent sync tracking)
val bookkeeper = RoomBookkeeper(dao = bookkeeperDao, keySerializer = { it.toString() })

// 5. Create MutableStore
val store = StoreFactory.createMutableStore(
    fetcher = Fetcher.of { key -> api.get(key) },
    sourceOfTruth = SourceOfTruth.of(...),
    converter = converter,
    updater = updater,
    bookkeeper = bookkeeper,
)

// 6. Write data
store.write(StoreWriteRequest.of(key, value))
```

### Step 4.4: Register BookkeeperDao in Database

**File:** `core/database/src/commonMain/.../AppDatabase.kt`

Add `BookkeeperEntity` to entities array, add `abstract val bookkeeperDao: BookkeeperDao`, bump VERSION to 3.

**File:** `core/database/src/commonMain/.../di/DatabaseModule.kt`

Add `single { get<AppDatabase>().bookkeeperDao }`.

### Files Created
- `core/database/src/commonMain/.../entity/BookkeeperEntity.kt` — NEW
- `core/database/src/commonMain/.../dao/BookkeeperDao.kt` — NEW
- `core/data/src/commonMain/.../store/RoomBookkeeper.kt` — NEW
- `core/data/src/commonMain/.../store/MUTABLE_STORE_TEMPLATE.md` — NEW (documentation)

### Files Modified
- `core/database/src/commonMain/.../AppDatabase.kt` — add entity + DAO + bump version
- `core/database/src/commonMain/.../di/DatabaseModule.kt` — provide BookkeeperDao
- `core/data/src/commonMain/.../repositoryImpl/StoreCacheManagerImpl.kt` — clear bookkeeper on logout

### Verification
- Unit test: RoomBookkeeper CRUD operations via BookkeeperDao
- Integration test: Verify persistent bookkeeper survives process restart (desktop test)
- Documentation review: MUTABLE_STORE_TEMPLATE.md is clear and complete

---

## Dependency Graph

```
Phase 1 (Validator TTL)
    │
    ├── Phase 2 (Logout Cache Clear) ── depends on stores being injectable
    │
    └── Phase 3 (skipMemory + Cache Policy)
            │
            └── Phase 4 (MutableStore Foundation) ── depends on all read-only patterns being solid
```

Phases 1-3 can be implemented independently. Phase 4 depends on Phase 2 (StoreCacheManager must also clear bookkeeper).

---

## File Impact Summary

| File | Phase | Change |
|------|-------|--------|
| `core/data/.../di/ApplicationStoreRegistry.kt` | 1 | Add TTL constants |
| `core/data/.../store/ExchangeRatesStore.kt` | 1 | Add validator + markFresh in writer |
| `core/data/.../store/CoinDetailStore.kt` | 1 | Add validator + markFresh in writer |
| `core/data/.../store/CoinMarketsStore.kt` | 1 | Add validator + markFresh in writer |
| `core/data/.../store/RateHistoryStore.kt` | 1 | Add validator + markFresh in writer |
| `core/data/.../repository/StoreCacheManager.kt` | 2 | NEW interface |
| `core/data/.../repositoryImpl/StoreCacheManagerImpl.kt` | 2 | NEW implementation |
| `core/data/.../di/RepositoryModule.kt` | 2 | Register StoreCacheManager |
| `core/data/.../repositoryImpl/UserLogoutManagerImpl.kt` | 2 | Inject + call clearAll() |
| `core-base/store/.../StoreDataExtensions.kt` | 3 | Add skipMemoryData() |
| `core-base/store/.../StoreFactory.kt` | 3 | Add memoryPolicy param |
| `core/data/.../store/*.kt` | 3 | Pass memory policies |
| `core/database/.../entity/BookkeeperEntity.kt` | 4 | NEW entity |
| `core/database/.../dao/BookkeeperDao.kt` | 4 | NEW DAO |
| `core/database/.../AppDatabase.kt` | 4 | Add entity + DAO + VERSION 3 |
| `core/database/.../di/DatabaseModule.kt` | 4 | Provide BookkeeperDao |
| `core/data/.../store/RoomBookkeeper.kt` | 4 | NEW persistent Bookkeeper |
| `core/data/.../store/MUTABLE_STORE_TEMPLATE.md` | 4 | NEW documentation |

**Total:** 12 modified + 6 new = 18 files

---

## Success Criteria

### Phase 1 (Validator)
- [ ] All 4 stores have TTL-based validation
- [ ] `DefaultValidator.markFresh()` called on every successful fetch
- [ ] Stale cached data triggers automatic re-fetch
- [ ] Unit tests verify TTL behavior

### Phase 2 (Logout Cache Clear)
- [ ] `StoreCacheManager.clearAll()` clears all in-memory + database caches
- [ ] `UserLogoutManagerImpl` calls `storeCacheManager.clearAll()` on logout
- [ ] No stale data visible after re-login
- [ ] Unit tests verify all stores + DAOs cleared

### Phase 3 (skipMemory + Cache Policy)
- [ ] `skipMemoryData()` extension available in StoreDataExtensions
- [ ] `StoreFactory.createStore()` accepts optional `memoryPolicy`
- [ ] All 4 stores have configured memory eviction policies
- [ ] Unit tests verify memory cache behavior

### Phase 4 (MutableStore Foundation)
- [ ] `RoomBookkeeper` persists sync failure tracking to Room
- [ ] `BookkeeperEntity` + `BookkeeperDao` registered in AppDatabase
- [ ] `MUTABLE_STORE_TEMPLATE.md` documents the complete write-back pattern
- [ ] `StoreCacheManagerImpl` clears bookkeeper table on logout
- [ ] Integration test verifies bookkeeper persistence

---

## Store5 Capability Coverage After Plan

| Feature | Before | After |
|---------|--------|-------|
| Fetcher | 100% | 100% |
| SourceOfTruth | 100% | 100% |
| Store (read-only) | 100% | 100% |
| Validator (TTL) | 0% | **100%** |
| store.clear()/clearAll() | 0% | **100%** |
| StoreReadRequest variants | 75% (3/4) | **100%** (4/4) |
| Memory policies | 0% | **100%** |
| MutableStore | 0% | **Ready** (template + infra) |
| Updater | 0% | **Ready** (documented pattern) |
| Bookkeeper (persistent) | 0% | **100%** |
| Converter | 0% | **Ready** (used when MutableStore activated) |
| **Overall Store5 utilization** | **~50%** | **~95%** |
