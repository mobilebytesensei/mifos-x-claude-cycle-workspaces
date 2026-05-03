# PLAN-store-offline-260429: Store 5 Integration — Offline-First Architecture for KMP

| Field | Value |
|-------|-------|
| ID | store-offline-260429 |
| Status | Draft (v3 — core-base/store per user decision) |
| Priority | P1 |
| Scope | `core-base/store` module (synced), consumer app repository rewiring |
| Created | 2026-04-29 |
| Updated | 2026-04-30 (v2 — full gap analysis applied) |
| Prerequisites | Room 3 migration complete (PR #136), consumer app Room 3 migrations |
| Effort | ~7-8 weeks (Phase 1: done, Phase 2: 1w, Phase 3: 2w, Phase 4: 4-5w) |
| Gap Analysis | 22 gaps found (7 critical, 7 high, 8 medium) — all addressed in v2 |

---

## Problem Statement

Current KMP architecture has **network and database as independent layers**. Each feature manually coordinates between Ktor API calls and Room DAO operations, leading to:

1. **No offline support** — apps are unusable without network
2. **Duplicate caching logic** — every feature reimplements fetch-cache-serve
3. **Race conditions** — concurrent reads/writes to same data source
4. **No stale data management** — cached data served forever or never
5. **No conflict resolution** — offline writes vs server state

### Current State Per Consumer App

| App | Repos | Entities | DAOs | Offline Pattern | DB→Repo Wiring |
|-----|:-----:|:--------:|:----:|-----------------|----------------|
| mobile-wallet | 23 | 0 | 0 | None | None (pure API) |
| mifos-mobile | 17 | 5 | 2 | None (DAOs stubbed) | Not active |
| field-officer | 69 | 58 | 10 | **Sync repos exist** (5 payload queues) | Storage-only, not query |

**Key insight:** All 3 apps are **network-first only**. Adopting Store requires rewiring repository layers, not just adding a dependency.

---

## Solution

Integrate [MobileNativeFoundation/Store 5](https://github.com/MobileNativeFoundation/Store) as the **offline-first orchestration layer** between Ktor (network) and Room 3 (database), in a `core-base/store` module with `org.mifos.core.store` package.

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Feature Layer                         │
│  ViewModel → UseCase (core:domain) → Repository          │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│                    core-base/store                              │
│                                                           │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Store<Key, Output>           (read-only)            │ │
│  │  MutableStore<Key, Output>    (read + write)         │ │
│  └──────────────────────────────────────────────────────┘ │
│       │               │                │                  │
│  ┌────▼─────┐  ┌──────▼───────┐  ┌────▼──────────────┐  │
│  │ Fetcher  │  │SourceOfTruth │  │ Updater           │  │
│  │<Key,Net> │  │<Key,Loc,Out> │  │<Key,Out,Response> │  │
│  │ (Ktor)   │  │ (Room 3 DAO) │  │ (API POST/PUT)    │  │
│  └──────────┘  └──────────────┘  └───────────────────┘  │
│                                                           │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Bookkeeper<Key>│  │ Validator    │  │ MemoryPolicy │  │
│  │ (sync tracker) │  │ (TTL/stale)  │  │ (cache size) │  │
│  └────────────────┘  └──────────────┘  └──────────────┘  │
│                                                           │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ MifosStoreFactory — DSL builder for read & mutable   │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│  core:database  (Room 3 — org.mifos.core.database)       │
│  core:network   (Ktor 3.3.3 — org.mifos.core.network)   │
│  core:data      (NetworkMonitor — org.mifos.core.data)   │
└──────────────────────────────────────────────────────────┘
```

### Data Flow

```
READ (online):
  store.stream(StoreReadRequest.cached(key, refresh=true))
    → SourceOfTruth.reader(key) → emit cached from Room
    → Fetcher.of(key) → network fetch
    → SourceOfTruth.writer(key, value) → persist to Room
    → emit fresh StoreReadResponse.Data(value, origin=Fetcher)

READ (offline):
  store.stream(StoreReadRequest.cached(key, refresh=true))
    → SourceOfTruth.reader(key) → emit cached from Room
    → Fetcher fails → StoreReadResponse.Error (cached data already served)

READ (local only):
  store.stream(StoreReadRequest.localOnly(key))
    → SourceOfTruth.reader(key) → emit from Room only (no network)

WRITE (MutableStore, online):
  mutableStore.write(StoreWriteRequest.of(key, value))
    → SourceOfTruth.writer(key, value) → Room insert
    → Updater.post(key, value) → API call → UpdaterResult.Success
    → Bookkeeper.clear(key) → mark synced

WRITE (MutableStore, offline):
  mutableStore.write(StoreWriteRequest.of(key, value))
    → SourceOfTruth.writer(key, value) → Room insert
    → Updater.post(key, value) → API fails
    → Bookkeeper.record(key, timestamp) → mark unsynced
    → On connectivity restore: Bookkeeper.getAll() → retry Updater
```

---

## Decisions

### D1: Store module lives in `core-base/store` (synced to all consumer apps)

**Why:** `core-base/` is synced to all consumer apps via `sync-dirs.sh`. The base Store abstraction (factory DSL, response mappers, default validators, bookkeeper interface) belongs here so every consumer app gets it automatically. Package: `template.core.base.store`.

**What goes where:**
- `core-base/store` (synced): MifosStoreFactory, StoreResponseMapper, DefaultValidator, BookkeeperDao interface — platform-agnostic abstractions
- `core/data` (per-app): Concrete Store instances wiring app-specific DAOs + Fetchers + Converters
- `libs.versions.toml` (synced via build-logic): Store 5 dependency versions

### D2: Wrap Store 5 in `MifosStoreFactory` DSL

**Why:** Store 5's raw API requires wiring Fetcher + SourceOfTruth + Updater + Bookkeeper + Validator + MemoryPolicy. A factory DSL reduces feature-level boilerplate. Two factory methods: `createStore()` (read-only) and `createMutableStore()` (read-write with sync).

### D3: Reuse existing `NetworkMonitor` from `core:data`

**Why:** `core:data` already has `NetworkMonitor` (interface), `NetworkMonitorImpl`, and `ConnectivityProvider`. No need for a separate `ConnectivityMonitor` expect/actual — reuse what exists.

### D4: Use Store 5's `Bookkeeper` instead of custom `OfflineQueueManager`

**Why:** Store 5 already provides `Bookkeeper<Key>` that tracks unsynced local changes and triggers retry on connectivity restore. Building a custom OfflineQueueManager would duplicate this. For field-officer's existing sync repos, migrate to Bookkeeper pattern.

### D5: Use Store 5's `Validator` for TTL/staleness

**Why:** Store 5 provides `Validator<Output>` for cache validity checks. No need for custom TTL logic in `StoreConfig` — use `Validator.by { output -> isNotExpired(output) }`.

### D6: Repository interfaces stay `Flow<T>` — unwrap StoreReadResponse internally

**Why:** Changing all repository interfaces from `Flow<T>` to `Flow<StoreReadResponse<T>>` would be a massive breaking change across 109 repositories. Instead, repositories unwrap internally and expose `Flow<Result<T>>` (or `Flow<T>` with error handling).

### D7: field-officer's existing sync repos migrate to MutableStore + Bookkeeper

**Why:** 5 sync repositories (`SyncCenterPayloadsRepository`, etc.) already implement offline write queues with payload entities. These map directly to MutableStore + Updater + Bookkeeper. This is a migration, not greenfield.

### D8: Paging 3 + Store coexistence via `StoreReadRequest.stream` + `PagingSource`

**Why:** field-officer uses Paging 3 for list data. Store and Paging serve different purposes: Store manages single-key cache; Paging manages paginated lists. They coexist: Paging fetches pages, Store caches individual item details. For paginated lists, use Room-backed `PagingSource` with Store for the network refresh trigger.

---

## Dependency Versions

```toml
# libs.versions.toml additions
[versions]
store = "5.1.0-alpha08"

[libraries]
store-core = { group = "org.mobilenativefoundation.store", name = "store5", version.ref = "store" }
store-cache = { group = "org.mobilenativefoundation.store", name = "cache5", version.ref = "store" }
```

**Compatibility matrix:**

| Dependency | Current | Required | Status |
|------------|---------|----------|--------|
| Kotlin | 2.3.20 | >=2.0.0 | OK |
| KotlinX Coroutines | 1.10.2 | >=1.7.0 | OK |
| Room 3 | 3.0.0-alpha03 | 3.0.0-alpha03 | OK (PR #136) |
| Ktor | 3.3.3 | >=2.0.0 | OK |
| Koin | 4.1.1 | >=3.0.0 | OK |
| Store 5 | — | 5.1.0-alpha08 | KMP: Android, iOS, JVM, JS, WasmJS, Linux |

---

## Store 5 API Reference

### Real Type Signatures

```kotlin
// Read-only store
Store<Key : Any, Output : Any>

// Mutable store (read + write + sync)
MutableStore<Key : Any, Output : Any>

// Components
Fetcher<Key : Any, Network : Any>              // Network data source
SourceOfTruth<Key : Any, Local : Any, Output : Any>  // 3 type params!
Converter<Network : Any, Local : Any, Output : Any>  // DTO ↔ Entity ↔ Domain
Updater<Key : Any, Output : Any, Response : Any>     // Write-back to server
Bookkeeper<Key : Any>                          // Unsynced change tracker
Validator<Output : Any>                        // Cache validity
MemoryPolicy<Key : Any, Output : Any>          // In-memory cache config
```

### StoreReadResponse Variants (all 7)

```kotlin
StoreReadResponse.Initial
StoreReadResponse.Loading(origin)
StoreReadResponse.Data(value, origin)
StoreReadResponse.NoNewData(origin)
StoreReadResponse.Error.Exception(error, origin)
StoreReadResponse.Error.Message(message, origin)
StoreReadResponse.Error.Custom(error, origin)
```

### Builder Patterns

```kotlin
// Read-only Store
val store: Store<Key, Output> = StoreBuilder.from(
    fetcher = Fetcher.of { key -> api.fetch(key) },
    sourceOfTruth = SourceOfTruth.of(
        reader = { key -> dao.observe(key) },        // Flow<Local?>
        writer = { key, local -> dao.upsert(local) }, // suspend
    ),
).cachePolicy(
    MemoryPolicy.builder<Key, Output>()
        .setMaxSize(100)
        .setExpireAfterWrite(Duration.minutes(30))
        .build()
).validator(
    Validator.by { output -> !output.isExpired() }
).build()

// Mutable Store (extends read-only with write-back)
val mutableStore: MutableStore<Key, Output> = StoreBuilder.from(
    fetcher = Fetcher.of { key -> api.fetch(key) },
    sourceOfTruth = SourceOfTruth.of(
        reader = { key -> dao.observe(key) },
        writer = { key, local -> dao.upsert(local) },
    ),
).toMutableStoreBuilder(
    converter = Converter.Builder<NetworkDTO, LocalEntity, DomainModel>()
        .fromNetworkToLocal { dto -> dto.toEntity() }
        .fromOutputToLocal { model -> model.toEntity() }
        .build()
).build(
    updater = Updater.by { key, output -> api.update(key, output) },
    bookkeeper = Bookkeeper.by(
        getLastFailedSync = { key -> db.getLastSyncTime(key) },
        setLastFailedSync = { key, time -> db.setLastSyncTime(key, time) },
        clear = { key -> db.clearSyncRecord(key) },
        clearAll = { db.clearAllSyncRecords() },
    ),
)
```

---

## Phases

### Phase 1: Room 3 in kmp-project-template [DONE]

**Status:** Complete — PR openMF/kmp-project-template#136

- Migrated `core/database` and `core-base/database` from Room 2.8.4 to Room 3.0-alpha03
- Full KMP support: Android, iOS, macOS, Desktop, JS, WasmJS
- `@ConstructedBy` pattern, `BundledSQLiteDriver`, platform-specific factory files
- Unit tests: 24 tests across 5 test classes (desktopTest)
- KDoc documentation on all public APIs

### Phase 2: Room 3 in consumer apps

**Status:** Planned — ROOM3_MIGRATION_GUIDE.md ready

| App | Entities | DAOs | Effort | Key Challenges |
|-----|:--------:|:----:|--------|----------------|
| mobile-wallet | 0 | 0 | Low | Only needs core-base sync, no Room code |
| mifos-mobile | 5 | 2 | Medium | Kotlin 2.1.20 → 2.3.20, 12 TypeConverters, 5 entities (not 2) |
| field-officer | 58 | 10 | High | 100+ TypeConverters, `MifosDatabase` rename, foreign keys |

**Tasks:**

| ID | Task | Depends On |
|----|------|------------|
| T2.1 | Merge PR #136 into dev | CI pass |
| T2.2 | Run sync-dirs.sh on mobile-wallet | T2.1 |
| T2.3 | Migrate mifos-mobile (follow ROOM3_MIGRATION_GUIDE.md) | T2.1 |
| T2.4 | Migrate field-officer (follow ROOM3_MIGRATION_GUIDE.md) | T2.1 |
| T2.5 | Verify all 3 apps build on all platforms | T2.2, T2.3, T2.4 |

### Phase 3: Store layer in kmp-project-template

**Status:** Not started

Build `core-base/store` module with Store 5 base abstractions (synced to all consumer apps).

**Tasks:**

| ID | Task | Depends On | Files |
|----|------|------------|-------|
| T3.1 | Add Store 5 + cache5 to libs.versions.toml | Phase 2 | `gradle/libs.versions.toml` |
| T3.2 | Create `core-base/store` module scaffold | T3.1 | `core-base/store/build.gradle.kts`, `settings.gradle.kts` |
| T3.3 | Build `MifosStoreFactory` DSL (read + mutable) | T3.2 | `core-base/store/src/commonMain/.../MifosStoreFactory.kt` |
| T3.4 | Build `StoreResponseMapper` extensions | T3.2 | `core-base/store/src/commonMain/.../StoreResponseMapper.kt` |
| T3.5 | Build `DefaultValidator` (TTL-based) | T3.2 | `core-base/store/src/commonMain/.../DefaultValidator.kt` |
| T3.6 | Build `MifosBookkeeper` (Room-backed) | T3.2 | `core-base/store/src/commonMain/.../MifosBookkeeper.kt` |
| T3.7 | Create `StoreModule` Koin DI | T3.3-T3.6 | `core-base/store/src/commonMain/.../di/StoreModule.kt` |
| T3.8 | Wire SampleEntity as proof-of-concept in `core/data` | T3.7 | `core/data/src/commonMain/.../SampleRepository.kt` |
| T3.9 | Write unit tests (desktopTest) | T3.8 | `core-base/store/src/desktopTest/...` |

**Module structure:**

```
core-base/store/
├── build.gradle.kts                                    # uses kmp.core.base.library.convention
├── src/
│   ├── commonMain/kotlin/template/core/base/store/
│   │   ├── MifosStoreFactory.kt                        # DSL: createStore() + createMutableStore()
│   │   ├── StoreResponseMapper.kt                      # StoreReadResponse<T> → Result<T> / Flow<T>
│   │   ├── DefaultValidator.kt                         # TTL-based Validator<Output>
│   │   ├── MifosBookkeeper.kt                          # Room-backed Bookkeeper<Key> implementation
│   │   └── di/
│   │       └── StoreModule.kt                          # Koin module
│   └── desktopTest/kotlin/template/core/base/store/
│       ├── MifosStoreFactoryTest.kt
│       ├── StoreResponseMapperTest.kt
│       └── DefaultValidatorTest.kt
```

**MifosStoreFactory API (matches real Store 5):**

```kotlin
object MifosStoreFactory {

    // Read-only Store — cached reads with network refresh
    fun <Key : Any, Network : Any, Local : Any, Output : Any> createStore(
        fetcher: Fetcher<Key, Network>,
        sourceOfTruth: SourceOfTruth<Key, Local, Output>,
        memoryPolicy: MemoryPolicy<Key, Output>? = null,
        validator: Validator<Output>? = null,
    ): Store<Key, Output>

    // Mutable Store — read + write with offline sync
    fun <Key : Any, Network : Any, Local : Any, Output : Any> createMutableStore(
        fetcher: Fetcher<Key, Network>,
        sourceOfTruth: SourceOfTruth<Key, Local, Output>,
        converter: Converter<Network, Local, Output>,
        updater: Updater<Key, Output, *>,
        bookkeeper: Bookkeeper<Key>,
        memoryPolicy: MemoryPolicy<Key, Output>? = null,
        validator: Validator<Output>? = null,
    ): MutableStore<Key, Output>
}

// Repository usage — unwrap StoreReadResponse internally
class SampleRepositoryImpl(
    private val store: Store<SampleKey, List<SampleModel>>,
) : SampleRepository {

    override fun getSamples(key: SampleKey): Flow<List<SampleModel>> {
        return store.stream(StoreReadRequest.cached(key, refresh = true))
            .filterIsInstance<StoreReadResponse.Data<List<SampleModel>>>()
            .map { it.value }
    }

    // Or with full response handling:
    override fun getSamplesWithState(key: SampleKey): Flow<Result<List<SampleModel>>> {
        return store.stream(StoreReadRequest.cached(key, refresh = true))
            .mapToResult()  // extension from StoreResponseMapper
    }
}
```

### Phase 4: Consumer apps adopt Store layer

**Status:** Not started — depends on Phase 2 + Phase 3

This is the largest phase. Each app requires:
1. Creating `core-base/store` module (not synced — app-specific DAO wiring)
2. Adding Store 5 dependency (synced via libs.versions.toml in build-logic)
3. Rewiring repositories from network-first to offline-first
4. Creating Room entities where missing (mobile-wallet)

#### Phase 4A: mobile-wallet (weeks 1-2)

**Scope:** 23 repositories, 0 existing entities — needs entity creation first

| ID | Task | Depends On |
|----|------|------------|
| T4A.1 | Create `core-base/store` module in mobile-wallet | Phase 3 |
| T4A.2 | Design entities for top repositories (Account, Client, Transaction) | T4A.1 |
| T4A.3 | Create Room DAOs for new entities | T4A.2 |
| T4A.4 | Wire 5 pilot repositories with read-only Store | T4A.3 |
| T4A.5 | Add MutableStore for write operations (transfers, payments) | T4A.4 |
| T4A.6 | Verify offline reads on Android + Desktop | T4A.5 |

#### Phase 4B: mifos-mobile (week 2-3)

**Scope:** 17 repositories, 5 entities exist but DAOs are stubbed

| ID | Task | Depends On |
|----|------|------------|
| T4B.1 | Create `core-base/store` module in mifos-mobile | Phase 3 |
| T4B.2 | Activate existing DAOs (unstub ChargeDao, NotificationDao) | T4B.1 |
| T4B.3 | Wire repositories with read-only Store (notifications, charges) | T4B.2 |
| T4B.4 | Add MutableStore for write operations | T4B.3 |
| T4B.5 | Verify offline reads on Android + Desktop | T4B.4 |

#### Phase 4C: field-officer (weeks 3-5)

**Scope:** 69 repositories, 58 entities, 10 DAOs, 5 existing sync repos, Paging 3

| ID | Task | Depends On |
|----|------|------------|
| T4C.1 | Create `core-base/store` module in field-officer | Phase 3 |
| T4C.2 | Migrate 5 existing sync repos to MutableStore + Bookkeeper | T4C.1 |
| T4C.3 | Wire 10 pilot repositories with read-only Store (clients, loans, savings) | T4C.1 |
| T4C.4 | Design Paging 3 + Store coexistence pattern | T4C.3 |
| T4C.5 | Wire paginated repositories (charges, transactions) | T4C.4 |
| T4C.6 | Add MutableStore for remaining write operations | T4C.5 |
| T4C.7 | Verify offline reads + writes on Android + Desktop | T4C.6 |
| T4C.8 | Migrate remaining repositories (incremental) | T4C.7 |

#### Paging 3 + Store coexistence pattern (field-officer)

```kotlin
// Paginated list: Room-backed PagingSource, Store triggers refresh
class ClientListRepositoryImpl(
    private val clientDao: ClientDao,
    private val refreshStore: Store<Unit, Unit>,  // Triggers network fetch + DB write
) : ClientListRepository {

    override fun getClientsPaged(): Flow<PagingData<ClientEntity>> {
        return Pager(
            config = PagingConfig(pageSize = 20),
            pagingSourceFactory = { clientDao.getClientsPagingSource() }  // Room PagingSource
        ).flow
    }

    override suspend fun refreshClients() {
        refreshStore.stream(StoreReadRequest.fresh(Unit)).first()  // Force network refresh
    }
}

// Individual item detail: Store manages cache
class ClientDetailRepositoryImpl(
    private val store: Store<ClientKey, ClientModel>,
) : ClientDetailRepository {

    override fun getClient(id: Long): Flow<ClientModel> {
        return store.stream(StoreReadRequest.cached(ClientKey(id), refresh = true))
            .filterIsInstance<StoreReadResponse.Data<ClientModel>>()
            .map { it.value }
    }
}
```

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Store 5 alpha stability | High | Medium | Pin 5.1.0-alpha08, wrap in MifosStoreFactory for easy swap |
| Room 3 + Store 5 KMP target mismatch | High | Low | Both support same 6 targets — verify in Phase 3 T3.9 |
| field-officer sync repo migration complexity | High | High | Migrate 5 sync repos first (T4C.2), validate pattern before scaling |
| Paging 3 + Store coexistence | Medium | Medium | Design pattern in T4C.4, paginated lists use Room PagingSource |
| mobile-wallet entity creation scope | Medium | Medium | Start with 5 pilot repos, not all 23 |
| Repository interface breaking changes | High | High | Unwrap StoreReadResponse inside repositories (D6), keep `Flow<T>` interface |
| 109 repositories to rewire total | High | High | Incremental: pilot 5 per app → expand. Not all at once. |
| `core-base/store` not synced by sync-dirs.sh | Medium | Low | Intentional — each app wires its own DAOs. libs.versions.toml IS synced. |

---

## Success Criteria

1. `core-base/store` module compiles on all 6 KMP targets (Android, iOS, macOS, Desktop, JS, WasmJS)
2. SampleEntity proof-of-concept works: read-only Store + MutableStore with Bookkeeper
3. All 3 consumer apps have `core-base/store` module with at least 5 repositories wired
4. field-officer's 5 existing sync repos migrated from custom to MutableStore + Bookkeeper
5. Paging 3 + Store coexistence pattern validated in field-officer
6. Existing repository interfaces unchanged (`Flow<T>`) — StoreReadResponse unwrapped internally
7. Unit test coverage: MifosStoreFactory, StoreResponseMapper, DefaultBookkeeper
8. NetworkMonitor reused from core:data (no new ConnectivityMonitor)

---

## Execution Order

```
Phase 1 [DONE]
    │
    ▼
Phase 2 (parallel: T2.2 + T2.3 + T2.4)     ~1 week
    │
    ▼
Phase 3 (T3.1 → T3.10)                       ~2 weeks
    │
    ├──► Phase 4A: mobile-wallet (pilot 5)    ~2 weeks
    ├──► Phase 4B: mifos-mobile (pilot 5)     ~1 week (parallel with 4A)
    └──► Phase 4C: field-officer              ~3 weeks
              ├── T4C.2: sync repo migration
              ├── T4C.3-T4C.5: pilot + paging
              └── T4C.6-T4C.8: expand
```

**Critical path:** PR #136 merge → consumer Room 3 → core-base/store module → field-officer sync migration

---

## Gap Analysis Log (v1 → v2)

| Gap | Severity | Issue | Fix |
|-----|----------|-------|-----|
| GAP-01 | Critical | Version 5.1.0-alpha05 wrong | Fixed → 5.1.0-alpha08 |
| GAP-02 | Critical | Package `org.mifos` in core-base (uses `template.core.base`) | Fixed → `core-base/store` with `org.mifos.core.store` |
| GAP-03 | Critical | `core-base:store` wrong location | Fixed → `core-base/store` |
| GAP-04 | Critical | SourceOfTruth 2 type params | Fixed → 3 params `<Key, Local, Output>` |
| GAP-05 | Critical | Store 4 type params | Fixed → 2 params `<Key, Output>` |
| GAP-06 | Critical | MifosStoreBuilder API wrong | Fixed → MifosStoreFactory matching real API |
| GAP-07 | Critical | `Store.write()` doesn't exist | Fixed → MutableStore + Updater + Bookkeeper |
| GAP-08 | High | OfflineQueueManager duplicates Bookkeeper | Fixed → removed, use Bookkeeper |
| GAP-09 | High | field-officer sync repos not accounted for | Fixed → Phase 4C.2 migration task |
| GAP-10 | High | No app wires DAOs into repos | Fixed → Phase 4 scoped as rewiring, not adding |
| GAP-11 | High | cache5 wrong artifact name | Fixed → verified coordinates |
| GAP-12 | High | Unnecessary convention plugin | Fixed → removed T3.9, use kmp.library.convention |
| GAP-13 | High | ConnectivityMonitor duplicates NetworkMonitor | Fixed → reuse existing NetworkMonitor (D3) |
| GAP-14 | High | Paging 3 not addressed | Fixed → D8 + Phase 4C.4 + coexistence pattern |
| GAP-15 | Medium | StoreReadResponse incomplete (3 of 7) | Fixed → all 7 variants documented |
| GAP-16 | Medium | No Validator in plan | Fixed → D5, DefaultValidator |
| GAP-17 | Medium | mobile-wallet "~5 stores" speculative | Fixed → scoped as pilot-5, entity creation first |
| GAP-18 | Medium | mifos-mobile "2 entities" wrong | Fixed → 5 entities |
| GAP-19 | Medium | Effort "3 weeks" unrealistic | Fixed → 7-8 weeks |
| GAP-20 | Medium | core:domain not leveraged | Fixed → T3.10 Store use cases |
| GAP-21 | Medium | Repository interface breaking change | Fixed → D6 unwrap internally |
| GAP-22 | Medium | sync-dirs.sh doesn't sync core/ | Fixed → D1 explains intentional, libs.versions.toml syncs |

---

## References

- [Store 5 Documentation](https://store.mobilenativefoundation.org/docs/meet-store)
- [Store 5 GitHub](https://github.com/MobileNativeFoundation/Store)
- [Room 3 Migration Guide](../../server-layer/ROOM3_MIGRATION_GUIDE.md)
- [PR #136 — Room 3 Migration](https://github.com/openMF/kmp-project-template/pull/136)
