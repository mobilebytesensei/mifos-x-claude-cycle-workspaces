# PLAN-store-architecture-v2-260502: Store Architecture V2 — Database Sync, Repository Layer, Professional UI

| Field | Value |
|-------|-------|
| ID | store-architecture-v2-260502 |
| Status | Draft |
| Priority | P0 |
| Scope | `core-base/store` + `core-base/ui` + `core/data` + `core/database` + `feature/*` |
| Created | 2026-05-02 |
| Updated | 2026-05-02 |
| Prerequisites | PLAN-screen-stream-260501 (completed), PLAN-storedata-api-260430 (completed) |
| Effort | ~20-24 hours (3 phases) |
| Parent Plan | PLAN-store-offline-260429 |
| New Deps | `compottie` (Lottie), `compottie-resources` (Compose resources) |
| DI Framework | **Koin** (project-wide standard — all DI uses Koin, no Dagger/Hilt) |

---

## Problem Statement

The Store architecture is functionally complete for network-to-UI flow but has critical gaps in data persistence, architectural layering, UI polish, and customizability.

### Current State (What Works)
- StoreFactory with createMemoryStore/createStore/createMutableStore
- ScreenDataStream + PagingScreenStream with NetworkMonitor fusion
- DecisionEngine mapping StoreData + NetworkStatus -> ScreenState
- DataFreshnessIndicator (basic STALE/UPDATING banner)
- ScreenContent rendering ScreenState with default state views
- Ktorfit APIs (FrankfurterApi, CoinGeckoApi) with retry
- Koin DI with named qualifiers (`StoreRegistry` object) in core/data

### What's Missing (8 Original Gaps + 23 Implementation Gaps)

| Gap | Description | Severity |
|-----|-------------|----------|
| GAP-1 | No database sync — all stores network-only (createMemoryStore) | HIGH |
| GAP-2 | StoreRegistry in wrong module (core/data instead of core-base/store) | MEDIUM |
| GAP-3 | Stores exposed directly to features — no repository layer | HIGH |
| GAP-4 | DataFreshnessIndicator lacks timestamps + offline badge | MEDIUM |
| GAP-5 | State UI components basic — not professional, not customizable, no Lottie | MEDIUM |
| GAP-6 | Pagination load-more has no built-in progress UI | MEDIUM |
| GAP-7 | No TTL/cache validity wired to stores | LOW |
| GAP-8 | No PagingScreenContent composable | LOW |

### Implementation Gaps (Found During Deep Analysis)

| # | Gap | Severity | Phase | Fix |
|---|-----|----------|-------|-----|
| IG-1 | core-base/store has NO Koin dependency — `named()` unavailable there | CRITICAL | 1 | Add `koin-core` to core-base/store `build.gradle.kts` |
| IG-2 | Features import `core/domain` NOT `core/data` — repository interfaces must go in core/domain | CRITICAL | 1 | Put interfaces in `core/domain`, impls in `core/data` |
| IG-3 | `StoreData.fetchedAt` uses `TimeSource.Monotonic.ValueTimeMark` not wall-clock `Instant` | HIGH | 2 | Add `fetchedAtInstant: Instant?` alongside existing monotonic mark |
| IG-4 | `ScreenState.Content` lacks `fetchedAt: Instant?` field | HIGH | 3 | Add field to Content data class |
| IG-5 | `DecisionEngine` doesn't pass `fetchedAt` to `ScreenState.Content` | HIGH | 3 | Update `mapToContent()` to propagate `StoreData.fetchedAtInstant` |
| IG-6 | `ScreenStateExtensions` `mapContent`/`combineContent` will break with Content changes | HIGH | 3 | Update all extension functions to preserve/copy `fetchedAt` |
| IG-7 | No fintech Room entities — only `SampleEntity` exists | HIGH | 2 | Create 4 entities + 4 DAOs + type converters (9 new files) |
| IG-8 | `PagingScreenStream.error` is private — can't expose load-more errors | HIGH | 3 | Make `error` public as `StateFlow<Throwable?>` |
| IG-9 | Registry naming — `ApplicationStoreRegistry` (generic, project-agnostic) | MEDIUM | 1 | Rename `StoreRegistry` object → `ApplicationStoreRegistry` extending base `StoreRegistry` |
| IG-10 | Repository interfaces have `CoroutineScope` + `NetworkMonitor` params — leaky abstraction | MEDIUM | 1 | Inject scope/monitor via constructor, not per-call |
| IG-11 | Plan uses `DefaultValidator.withTtl()` but Store5 API is `Validator.of {}` | MEDIUM | 2 | Use `Validator.of { storeData -> storeData.fetchedAt.elapsedNow() < ttl }` |
| IG-12 | Room's `@TypeConverter` needs `kotlinx.serialization` for `Map<String, Double>` JSON | MEDIUM | 2 | Use `Json.encodeToString`/`decodeFromString` in converters |
| IG-13 | `ExchangeRatesDto` has `@SerialName("start_date")` but entity maps from domain | MEDIUM | 2 | Entity maps from domain model, not DTO — separate mapping |
| IG-14 | `CoinMarketEntity` page tracking for paginated upsert | MEDIUM | 2 | Add `page: Int` column for page-aware SourceOfTruth |
| IG-15 | `ScreenContent` already has `content: @Composable (T, DataFreshness?) -> Unit` — 2-arg lambda | MEDIUM | 3 | Match existing API: pass `fetchedAt` via `ScreenState.Content`, not lambda args |
| IG-16 | Lottie assets need sourcing — plan references 5 JSON files that don't exist | MEDIUM | 3 | Source from LottieFiles or create minimal vector animations |
| IG-17 | `StoreDataExtensions.kt` `mapValue`/`combine` must preserve `fetchedAtInstant` | MEDIUM | 2 | Update all transformation helpers |
| IG-18 | `ScreenDataStream` constructor takes `Store` — repo must create stream itself | LOW | 1 | Repo creates `ScreenDataStream(store, ...)` internally |
| IG-19 | `formatRelativeTime` needs `kotlinx-datetime` dependency in core-base/ui | LOW | 3 | Add `kotlinx-datetime` to core-base/ui deps |
| IG-20 | Migration V1→V2 — destructive OK for template but plan should document explicitly | LOW | 2 | Add `fallbackToDestructiveMigration()` call in builder |
| IG-21 | `PagingScreenStream.loadNextPage()` auto-trigger in composable needs debounce | LOW | 3 | Add `snapshotFlow` debounce (300ms) to prevent rapid-fire |
| IG-22 | No `EmiCalculatorRepository` — EMI feature is offline-only (no store) | LOW | 1 | Skip — EMI is pure calculation, no network/DB needed |
| IG-23 | `StoreDataMapper.kt` EMPTY_SENTINEL suppression already applied — no change needed | INFO | — | Already handled in prior commit |

---

## Phase 1: Architecture Foundation (GAP-2, GAP-3, IG-1, IG-2, IG-9, IG-10, IG-18, IG-22)

### Step 1.1: Add Koin Dependency to core-base/store (IG-1)

**Problem:** core-base/store currently has NO Koin dependency. `named()` function is unavailable.

**Files to modify:**
- `core-base/store/build.gradle.kts` — Add to commonMain dependencies:
  ```kotlin
  commonMain.dependencies {
      api(libs.koin.core)  // Required for StoreRegistry named qualifiers
  }
  ```

### Step 1.2: Move StoreRegistry to core-base/store

**Goal:** StoreRegistry becomes a reusable base pattern in core-base/store. Projects extend it in core/data.

**Files to create:**
- `core-base/store/src/commonMain/kotlin/template/core/base/store/StoreRegistry.kt`
  ```kotlin
  package template.core.base.store

  import org.koin.core.qualifier.StringQualifier
  import org.koin.core.qualifier.named

  /**
   * Base registry for Store DI qualifiers (Koin).
   * Projects extend this in their core/data module to define
   * app-specific store qualifiers that prevent type erasure collisions.
   */
  abstract class StoreRegistry {
      protected fun store(name: String): StringQualifier = named(name)
  }
  ```

**Files to modify:**
- `core/data/src/commonMain/.../di/StoreRegistry.kt` — Rename + extend base (IG-9):
  ```kotlin
  import template.core.base.store.StoreRegistry

  object ApplicationStoreRegistry : StoreRegistry() {
      val ExchangeRates = store("exchangeRates")
      val RateHistory = store("rateHistory")
      val CoinMarkets = store("coinMarkets")
      val CoinDetail = store("coinDetail")
  }
  ```
- `core/data/src/commonMain/.../di/RepositoryModule.kt` — Use `ApplicationStoreRegistry.*`
- `feature/crypto/src/commonMain/.../di/CryptoModule.kt` — Use `ApplicationStoreRegistry.*`
- `feature/currency-rates/src/commonMain/.../di/CurrencyRatesModule.kt` — Use `ApplicationStoreRegistry.*`

**Verification:** Build compiles, all features resolve stores via Koin named qualifiers.

---

### Step 1.3: Repository Layer — Stores Hidden Behind Repositories (IG-2, IG-10, IG-18)

**Goal:** ViewModels inject repositories (not raw Store). Store becomes implementation detail.

**CRITICAL (IG-2):** Feature modules import `core/domain`, NOT `core/data`. Therefore:
- Repository **interfaces** go in `core/domain` (accessible to features)
- Repository **implementations** go in `core/data` (hidden from features)

**Architecture:**
```
Feature ViewModel (feature/*)
    -> Repository interface (core/domain/repository)  ← IG-2 FIX
        -> RepositoryImpl (core/data/repository)
            -> Store<Key, T> (core/data/store — internal)
            -> ScreenDataStream / PagingScreenStream created inside repo
```

**CRITICAL (IG-10):** Repository interfaces must NOT leak `CoroutineScope` or `NetworkMonitor` as per-call params. These are constructor-injected via Koin into the implementation.

**Files to create:**

1. `core/domain/src/commonMain/.../repository/CurrencyRepository.kt`
   ```kotlin
   interface CurrencyRepository {
       fun exchangeRatesStream(baseCurrency: String): ScreenDataStream<ExchangeRates>
       fun rateHistoryStream(keyFlow: Flow<RateHistoryKey>): ScreenDataStream<RateHistory>
   }
   ```

2. `core/domain/src/commonMain/.../repository/CryptoRepository.kt`
   ```kotlin
   interface CryptoRepository {
       fun coinMarketsStream(pageSize: Int = 20): PagingScreenStream<CoinMarket>
       fun coinDetailStream(coinId: String): ScreenDataStream<CoinDetail>
   }
   ```

3. `core/data/src/commonMain/.../repository/CurrencyRepositoryImpl.kt` (IG-18)
   ```kotlin
   class CurrencyRepositoryImpl(
       private val exchangeRatesStore: Store<String, ExchangeRates>,
       private val rateHistoryStore: Store<RateHistoryKey, RateHistory>,
       private val networkMonitor: NetworkMonitor,
   ) : CurrencyRepository {
       override fun exchangeRatesStream(baseCurrency: String): ScreenDataStream<ExchangeRates> {
           return ScreenDataStream(exchangeRatesStore, baseCurrency, networkMonitor)
       }
       // ...
   }
   ```

4. `core/data/src/commonMain/.../repository/CryptoRepositoryImpl.kt`

**Note (IG-22):** EMI calculator is pure offline calculation — no repository needed. Skip.

**Files to modify:**
- `core/data/src/commonMain/.../di/RepositoryModule.kt` — Register repos via Koin `singleOf(...) bind`, make stores internal
- `feature/currency-rates/.../di/CurrencyRatesModule.kt` — Inject `CurrencyRepository` (resolved by Koin)
- `feature/crypto/.../di/CryptoModule.kt` — Inject `CryptoRepository` (resolved by Koin)
- `feature/currency-rates/.../ui/CurrencyRatesViewModel.kt` — Use `CurrencyRepository`
- `feature/currency-rates/.../ui/RateHistoryViewModel.kt` — Use `CurrencyRepository`
- `feature/crypto/.../ui/CryptoWatchlistViewModel.kt` — Use `CryptoRepository`
- `feature/crypto/.../ui/CoinDetailViewModel.kt` — Use `CryptoRepository`

**Key design decision:** Repository creates the ScreenDataStream internally with the Store + NetworkMonitor (both injected by Koin). ViewModel calls `repository.exchangeRatesStream("USD")` — clean API. Store types never leak to feature modules.

**Verification:** Feature modules have zero imports from `org.mobilenativefoundation.store`. ViewModels only depend on repository interfaces from `core/domain`.

---

## Phase 2: Database Integration (GAP-1, GAP-7, IG-3, IG-7, IG-11, IG-12, IG-13, IG-14, IG-17, IG-20)

### Step 2.1: Room Entities + DAOs for Fintech Data (IG-7)

**Goal:** All network data syncs to Room database. Store uses SourceOfTruth.

**IMPORTANT (IG-7):** Currently only `SampleEntity` exists. All 4 fintech entities + DAOs are new.

**Files to create in `core/database/src/commonMain/`:**

1. **Entities:**
   - `ExchangeRatesEntity.kt` — base currency, date, rates (JSON string), fetchedAt (Long epochMillis)
   - `CoinMarketEntity.kt` — id, symbol, name, image, currentPrice, marketCap, rank, priceChange24h, page (Int), fetchedAt
     - **(IG-14):** `page: Int` column for paginated SourceOfTruth — enables page-aware upsert/delete
   - `CoinDetailEntity.kt` — id, symbol, name, description, image, marketDataJson (String), fetchedAt
   - `RateHistoryEntity.kt` — fromCurrency, toCurrency, startDate, endDate, ratesJson (String), fetchedAt

2. **DAOs:**
   - `ExchangeRatesDao.kt` — `@Upsert upsert(entity)`, `@Query getByBase(currency): Flow<Entity?>`, `@Query deleteOlderThan(epochMillis: Long)`
   - `CoinMarketDao.kt` — `@Upsert upsertAll(list)`, `@Query getPage(limit, offset): Flow<List<Entity>>`, `@Query deleteByPage(page: Int)`, `@Query count(): Int`
   - `CoinDetailDao.kt` — `@Upsert upsert(entity)`, `@Query getById(id): Flow<Entity?>`, `@Query delete(id)`
   - `RateHistoryDao.kt` — `@Upsert upsert(entity)`, `@Query get(from, to, startDate, endDate): Flow<Entity?>`

3. **TypeConverters (IG-12):**
   - `FintechTypeConverters.kt` — Uses `kotlinx.serialization.json.Json`:
     ```kotlin
     @TypeConverter
     fun mapToString(map: Map<String, Double>): String = Json.encodeToString(map)

     @TypeConverter
     fun stringToMap(json: String): Map<String, Double> = Json.decodeFromString(json)

     @TypeConverter
     fun instantToLong(instant: Instant): Long = instant.toEpochMilliseconds()

     @TypeConverter
     fun longToInstant(epochMillis: Long): Instant = Instant.fromEpochMilliseconds(epochMillis)
     ```

4. **Entity ↔ Domain Mappers (IG-13):**
   - `ExchangeRatesEntityMapper.kt` — Maps between `ExchangeRatesEntity` ↔ `ExchangeRates` domain model
   - `CoinMarketEntityMapper.kt` — Maps between `CoinMarketEntity` ↔ `CoinMarket`
   - `CoinDetailEntityMapper.kt` — Maps between `CoinDetailEntity` ↔ `CoinDetail`
   - `RateHistoryEntityMapper.kt` — Maps between `RateHistoryEntity` ↔ `RateHistory`
   - **NOTE:** Entity maps from DOMAIN model, not from DTO. DTO → Domain mapping happens in Store fetcher, Domain → Entity in SourceOfTruth writer.

**Files to modify:**
- `core/database/.../AppDatabase.kt` — Add all 4 entities, 4 DAOs, `FintechTypeConverters`, bump VERSION to 2
- **(IG-20):** Use `fallbackToDestructiveMigration()` in database builder — acceptable for template project with no production users

### Step 2.2: Wire SourceOfTruth into Stores (IG-11)

**Goal:** Switch from `createMemoryStore` to `createStore` with Room SourceOfTruth.

**(IG-11):** Store5 uses `Validator.of { }` not `DefaultValidator.withTtl()`. Correct pattern:
```kotlin
validator = Validator.of { storeData ->
    storeData.fetchedAt.elapsedNow() < 5.minutes
}
```

**Files to modify in `core/data/src/commonMain/.../store/`:**

1. `ExchangeRatesStore.kt`:
   ```kotlin
   fun provideExchangeRatesStore(
       api: FrankfurterApi,
       dao: ExchangeRatesDao,
   ): Store<String, ExchangeRates> = StoreFactory.createStore(
       fetcher = Fetcher.of { baseCurrency ->
           api.getLatestRates(from = baseCurrency).toDomain()
       },
       sourceOfTruth = SourceOfTruth.of(
           reader = { key -> dao.getByBase(key).map { it?.toDomain() } },
           writer = { key, value -> dao.upsert(value.toEntity(key)) },
           delete = { key -> dao.deleteByBase(key) },
           deleteAll = { dao.deleteAll() },
       ),
   )
   ```

2. `CoinMarketsStore.kt` — SourceOfTruth with page-aware upsert (IG-14: `deleteByPage` before `upsertAll`)
3. `CoinDetailStore.kt` — SourceOfTruth keyed by coinId
4. `RateHistoryStore.kt` — SourceOfTruth keyed by composite key string

**DI update:** `RepositoryModule.kt` store providers now take DAO params from Koin:
```kotlin
single(ApplicationStoreRegistry.ExchangeRates) { provideExchangeRatesStore(get(), get()) }
```

### Step 2.3: Wall-Clock Timestamps for Staleness (IG-3, IG-17)

**Goal:** Track real `fetchedAt` Instant that survives process restart.

**(IG-3):** `StoreData.fetchedAt` uses `TimeSource.Monotonic.ValueTimeMark` — this does NOT survive process death. We add a parallel wall-clock field.

**Files to modify:**
- `core-base/store/.../StoreData.kt` — Add `fetchedAtInstant: Instant? = null` (from `kotlinx-datetime`)
  ```kotlin
  data class StoreData<out T>(
      val value: T,
      val origin: ResponseOrigin,
      val fetchedAt: TimeSource.Monotonic.ValueTimeMark,  // existing — for in-process freshness
      val fetchedAtInstant: Instant? = null,               // NEW — wall-clock, survives restart
  )
  ```
- `core-base/store/.../StoreDataExtensions.kt` **(IG-17):** Update `mapValue`, `combine` to preserve `fetchedAtInstant`:
  ```kotlin
  fun <T, R> StoreData<T>.mapValue(transform: (T) -> R): StoreData<R> = StoreData(
      value = transform(value),
      origin = origin,
      fetchedAt = fetchedAt,
      fetchedAtInstant = fetchedAtInstant,  // PRESERVE
  )
  ```
- `core-base/store/.../StoreDataMapper.kt` — Populate `fetchedAtInstant = Clock.System.now()` when mapping from Store response
- Entity `fetchedAt` column stores `Instant.toEpochMilliseconds()` via TypeConverter — read back populates `fetchedAtInstant`

**Verification:** Kill app, reopen — cached data appears instantly with correct "Last updated X ago" timestamp from Room.

---

## Phase 3: Professional UI (GAP-4, GAP-5, GAP-6, GAP-8, IG-4, IG-5, IG-6, IG-8, IG-15, IG-16, IG-19, IG-21)

### Step 3.1: Add Compottie (Lottie) Dependency

**Files to modify:**

`gradle/libs.versions.toml`:
```toml
[versions]
compottie = "2.0.0"

[libraries]
compottie = { module = "io.github.alexzhirkevich:compottie", version.ref = "compottie" }
compottie-resources = { module = "io.github.alexzhirkevich:compottie-resources", version.ref = "compottie" }
```

`core-base/ui/build.gradle.kts`:
```kotlin
commonMain.dependencies {
    api(libs.compottie)
    api(libs.compottie.resources)
}
```

**Lottie assets** (add to `core-base/ui/src/commonMain/composeResources/files/`):
- `loading.json` — Loading spinner/pulse animation
- `empty.json` — Empty state illustration (empty box, no items)
- `no_network.json` — Offline/no WiFi animation
- `error.json` — Error/warning animation
- `load_more.json` — Small loading dots for pagination

---

### Step 3.2: Professional State UI Components (GAP-5)

**Goal:** Default state views are professional with Lottie + fully customizable.

**Files to create in `core-base/ui/src/commonMain/.../ui/`:**

1. **`StateDefaults.kt`** — Centralized defaults configuration:
   ```kotlin
   object StateDefaults {
       // Lottie animation resource refs
       val loadingAnimation: String = "files/loading.json"
       val emptyAnimation: String = "files/empty.json"
       val noNetworkAnimation: String = "files/no_network.json"
       val errorAnimation: String = "files/error.json"

       // Default text
       val emptyTitle = "Nothing here yet"
       val emptyDescription = "Data will appear once available"
       val noNetworkTitle = "You're offline"
       val noNetworkDescription = "Check your connection and try again"
       val noNetworkCaptiveTitle = "Sign in to WiFi"
       val noNetworkCaptiveDescription = "This network requires sign-in"
       val errorTitle = "Something went wrong"
       val errorDescription: (Throwable) -> String = { it.message ?: "An unexpected error occurred" }
       val retryButtonText = "Try Again"
   }
   ```

2. **`StateContent.kt`** — Reusable state view with Lottie + customization:
   ```kotlin
   @Composable
   fun StateContent(
       modifier: Modifier = Modifier,
       // Lottie or static icon — one wins
       lottieRes: String? = null,           // Lottie JSON resource path
       lottieIterations: Int = Int.MAX_VALUE,
       imageVector: ImageVector? = null,     // Fallback static icon
       imagePainter: Painter? = null,        // Custom painter (Bitmap etc)
       // Text
       title: String,
       description: String? = null,
       // Action
       actionText: String? = null,
       onAction: (() -> Unit)? = null,
       // Sizing
       animationSize: Dp = 180.dp,
       iconSize: Dp = 64.dp,
   )
   ```
   - Priority: lottieRes > imagePainter > imageVector
   - If lottieRes provided → render with `rememberLottieComposition` + `rememberLottiePainter`
   - If none provided → shows nothing (text-only)
   - Consistent spacing: animation → 24dp → title → 8dp → description → 24dp → button

3. **Refactored defaults using StateContent:**

   ```kotlin
   // DefaultLoadingContent — Lottie loading animation
   @Composable
   fun DefaultLoadingContent(modifier: Modifier = Modifier) {
       StateContent(
           modifier = modifier,
           lottieRes = StateDefaults.loadingAnimation,
           title = "",  // No text for loading — just animation
       )
   }

   // DefaultEmptyContent — customizable empty state
   @Composable
   fun DefaultEmptyContent(
       modifier: Modifier = Modifier,
       lottieRes: String? = StateDefaults.emptyAnimation,
       imageVector: ImageVector? = Icons.Default.Inbox,
       title: String = StateDefaults.emptyTitle,
       description: String? = StateDefaults.emptyDescription,
   ) { StateContent(...) }

   // DefaultNoNetworkContent — offline with Lottie + retry
   @Composable
   fun DefaultNoNetworkContent(
       onRetry: () -> Unit,
       modifier: Modifier = Modifier,
       isCaptivePortal: Boolean = false,
       lottieRes: String? = StateDefaults.noNetworkAnimation,
       imageVector: ImageVector? = if (isCaptivePortal) Icons.Default.CloudOff else Icons.Default.WifiOff,
       title: String = if (isCaptivePortal) StateDefaults.noNetworkCaptiveTitle else StateDefaults.noNetworkTitle,
       description: String? = if (isCaptivePortal) StateDefaults.noNetworkCaptiveDescription else StateDefaults.noNetworkDescription,
       actionText: String = StateDefaults.retryButtonText,
   ) { StateContent(..., actionText, onAction = onRetry) }

   // DefaultErrorContent — error with Lottie + retry
   @Composable
   fun DefaultErrorContent(
       error: Throwable,
       onRetry: () -> Unit,
       modifier: Modifier = Modifier,
       lottieRes: String? = StateDefaults.errorAnimation,
       imageVector: ImageVector? = Icons.Default.Error,
       title: String = StateDefaults.errorTitle,
       description: String? = StateDefaults.errorDescription(error),
       actionText: String = StateDefaults.retryButtonText,
   ) { StateContent(..., actionText, onAction = onRetry) }
   ```

4. **Update `ScreenContent.kt`** — Wire customizable defaults:
   ```kotlin
   @Composable
   fun <T> ScreenContent(
       state: ScreenState<T>,
       onRetry: () -> Unit,
       modifier: Modifier = Modifier,
       showFreshnessIndicator: Boolean = true,
       // Customizable state overrides (null = use defaults)
       loading: @Composable (() -> Unit)? = null,
       empty: @Composable (() -> Unit)? = null,
       noNetwork: @Composable ((isCaptivePortal: Boolean) -> Unit)? = null,
       error: @Composable ((Throwable) -> Unit)? = null,
       // Customizable default params (when using built-in defaults)
       emptyTitle: String = StateDefaults.emptyTitle,
       emptyDescription: String? = StateDefaults.emptyDescription,
       emptyLottie: String? = StateDefaults.emptyAnimation,
       errorTitle: String = StateDefaults.errorTitle,
       // Content
       content: @Composable (T) -> Unit,
   )
   ```

---

### Step 3.3: ScreenState.Content + DecisionEngine Updates (IG-4, IG-5, IG-6)

**Goal:** Propagate `fetchedAtInstant` from `StoreData` through `DecisionEngine` to `ScreenState.Content`.

**(IG-4)** Update `ScreenState.kt`:
```kotlin
data class Content<out T>(
    val data: T,
    val freshness: DataFreshness,
    val fetchedAt: Instant? = null,  // NEW — wall-clock from StoreData.fetchedAtInstant
) : ScreenState<T>
```

**(IG-5)** Update `DecisionEngine.kt` — `mapToContent()`:
```kotlin
private fun <T> mapToContent(storeData: StoreData<T>, networkStatus: NetworkStatus): ScreenState.Content<T> {
    return ScreenState.Content(
        data = storeData.value,
        freshness = determineFreshness(storeData, networkStatus),
        fetchedAt = storeData.fetchedAtInstant,  // NEW — propagate wall-clock
    )
}
```

**(IG-6)** Update `ScreenStateExtensions.kt` — ALL transformation functions must preserve `fetchedAt`:
```kotlin
fun <T, R> ScreenState<T>.mapContent(transform: (T) -> R): ScreenState<R> = when (this) {
    is ScreenState.Content -> ScreenState.Content(
        data = transform(data),
        freshness = freshness,
        fetchedAt = fetchedAt,  // PRESERVE
    )
    // ... other branches unchanged
}

fun <T1, T2, R> combineContent(
    state1: ScreenState<T1>,
    state2: ScreenState<T2>,
    transform: (T1, T2) -> R,
): ScreenState<R> {
    // When both are Content, use the OLDER fetchedAt (more conservative staleness)
    val fetchedAt = listOfNotNull(
        (state1 as? ScreenState.Content)?.fetchedAt,
        (state2 as? ScreenState.Content)?.fetchedAt,
    ).minOrNull()
    // ...
}
```

### Step 3.4: Professional DataFreshnessIndicator with Timestamps (GAP-4, IG-19)

**Goal:** Show human-readable "Last updated 5 min ago" + offline badge.

**(IG-19):** `core-base/ui` needs `kotlinx-datetime` dependency for `Instant` and time formatting.

**Files to modify:**
- `core-base/ui/build.gradle.kts` — Add `api(libs.kotlinx.datetime)` to commonMain deps

**Files to modify in `core-base/ui/`:**

1. **`DataFreshnessIndicator.kt`** — Enhanced version:
   ```kotlin
   @Composable
   fun DataFreshnessIndicator(
       freshness: DataFreshness,
       fetchedAt: Instant? = null,
       modifier: Modifier = Modifier,
       staleMessage: String? = null,
       showTimestamp: Boolean = true,
       timestampFormatter: ((Instant) -> String)? = null,
   ) {
       // FRESH -> hidden
       // STALE -> Row: [WifiOff icon] "Offline" + "Last updated 5 min ago" pill
       // UPDATING -> LinearProgressIndicator + "Updating..."
   }

   internal fun formatRelativeTime(fetchedAt: Instant, now: Instant): String {
       val duration = now - fetchedAt
       return when {
           duration < 1.minutes -> "Just now"
           duration < 60.minutes -> "${duration.inWholeMinutes} min ago"
           duration < 24.hours -> "${duration.inWholeHours}h ago"
           duration < 7.days -> "${duration.inWholeDays}d ago"
           else -> fetchedAt.toLocalDateTime(TimeZone.currentSystemDefault()).date.toString()
       }
   }
   ```

2. **`OfflineBadge.kt`** — Small reusable offline indicator:
   ```kotlin
   @Composable
   fun OfflineBadge(
       fetchedAt: Instant? = null,
       modifier: Modifier = Modifier,
       icon: ImageVector = Icons.Default.WifiOff,
       label: String = "Offline",
       showTimestamp: Boolean = true,
   ) {
       // Small pill/chip: [WifiOff] Offline . 5 min ago
       // Uses Surface with tonalElevation for subtle background
   }
   ```

3. **Update `ScreenContent.kt`** **(IG-15):** — Pass `fetchedAt` through Content state (NOT via lambda args):
   ```kotlin
   // In Content branch — fetchedAt comes from ScreenState.Content, not extra lambda param:
   is ScreenState.Content -> {
       Column(modifier) {
           DataFreshnessIndicator(
               freshness = state.freshness,
               fetchedAt = state.fetchedAt,  // From ScreenState.Content
           )
           content(state.data)
       }
   }
   ```
   **Note (IG-15):** Current `ScreenContent` has 2-arg lambda `content: @Composable (T, DataFreshness?) -> Unit`. The `fetchedAt` goes into `ScreenState.Content` — no need to change the lambda signature.

---

### Step 3.5: Expose PagingScreenStream Error (IG-8)

**Goal:** Make load-more errors accessible to the UI.

**Files to modify:**
- `core-base/store/.../PagingScreenStream.kt` — Change `error` from private to public:
  ```kotlin
  val loadMoreError: StateFlow<Throwable?> = _loadMoreError.asStateFlow()  // was private
  ```

### Step 3.6: Professional Load-More Footer (GAP-6)

**Goal:** Built-in pagination footer with progress, messaging, error, end-of-list.

**Files to create in `core-base/ui/`:**

1. **`LoadMoreFooter.kt`**:
   ```kotlin
   @Composable
   fun LoadMoreFooter(
       isLoadingMore: Boolean,
       hasMore: Boolean,
       error: Throwable? = null,
       onRetry: (() -> Unit)? = null,
       modifier: Modifier = Modifier,
       loadingLottie: String? = StateDefaults.loadMoreAnimation,
       loadingMessage: String? = null,  // null = random quote from built-in list
       endOfListMessage: String = "You've seen it all",
       errorMessage: String = "Couldn't load more",
   ) {
       // States:
       // isLoadingMore=true -> Lottie dots + message/quote
       // error!=null -> "Couldn't load more" + [Retry]
       // !hasMore -> subtle "You've seen it all" divider
       // else -> hidden (spacer only)
   }
   ```

   Built-in loading quotes (rotated randomly):
   ```
   "Fetching more goodness..."
   "Almost there..."
   "Loading the next batch..."
   "Hang tight..."
   "Getting more data..."
   ```

2. **(IG-21)** Auto-trigger with debounce in PagingScreenContent:
   ```kotlin
   LaunchedEffect(listState) {
       snapshotFlow { listState.layoutInfo }
           .debounce(300)  // IG-21: prevent rapid-fire triggers
           .collect { info ->
               val lastVisible = info.visibleItemsInfo.lastOrNull()?.index ?: 0
               val total = info.totalItemsCount
               if (lastVisible >= total - 3 && hasMore && !isLoadingMore) {
                   pagingStream.loadNextPage()
               }
           }
   }
   ```

---

### Step 3.7: PagingScreenContent Composable (GAP-8)

**Files to create in `core-base/ui/`:**

1. **`PagingScreenContent.kt`**:
   ```kotlin
   @Composable
   fun <T> PagingScreenContent(
       state: ScreenState<List<T>>,
       hasMore: Boolean,
       isLoadingMore: Boolean,
       onRetry: () -> Unit,
       onLoadMore: () -> Unit,
       modifier: Modifier = Modifier,
       showFreshnessIndicator: Boolean = true,
       // Customizable state overrides
       loading: @Composable (() -> Unit)? = null,
       empty: @Composable (() -> Unit)? = null,
       noNetwork: @Composable ((Boolean) -> Unit)? = null,
       error: @Composable ((Throwable) -> Unit)? = null,
       // Load more customization
       loadMoreError: Throwable? = null,
       loadMoreFooter: @Composable (() -> Unit)? = null,
       // Content
       itemContent: @Composable LazyItemScope.(T) -> Unit,
   ) {
       // Handles: Loading/Empty/NoNetwork/Error states via ScreenContent
       // Content: LazyColumn with items + auto-trigger loadNextPage + LoadMoreFooter
   }
   ```

---

## File Impact Summary

### New Files (Phase 1-3)
| File | Module | Phase | Gap |
|------|--------|-------|-----|
| `template.core.base.store.StoreRegistry` | core-base/store | 1 | GAP-2 |
| `CurrencyRepository.kt` | core/domain/repository | 1 | GAP-3, IG-2 |
| `CryptoRepository.kt` | core/domain/repository | 1 | GAP-3, IG-2 |
| `CurrencyRepositoryImpl.kt` | core/data/repository | 1 | GAP-3 |
| `CryptoRepositoryImpl.kt` | core/data/repository | 1 | GAP-3 |
| `ExchangeRatesEntity.kt` | core/database | 2 | GAP-1, IG-7 |
| `CoinMarketEntity.kt` | core/database | 2 | GAP-1, IG-7, IG-14 |
| `CoinDetailEntity.kt` | core/database | 2 | GAP-1, IG-7 |
| `RateHistoryEntity.kt` | core/database | 2 | GAP-1, IG-7 |
| `ExchangeRatesDao.kt` | core/database | 2 | GAP-1 |
| `CoinMarketDao.kt` | core/database | 2 | GAP-1 |
| `CoinDetailDao.kt` | core/database | 2 | GAP-1 |
| `RateHistoryDao.kt` | core/database | 2 | GAP-1 |
| `FintechTypeConverters.kt` | core/database | 2 | IG-12 |
| `ExchangeRatesEntityMapper.kt` | core/database | 2 | IG-13 |
| `CoinMarketEntityMapper.kt` | core/database | 2 | IG-13 |
| `CoinDetailEntityMapper.kt` | core/database | 2 | IG-13 |
| `RateHistoryEntityMapper.kt` | core/database | 2 | IG-13 |
| `StateDefaults.kt` | core-base/ui | 3 | GAP-5 |
| `StateContent.kt` | core-base/ui | 3 | GAP-5 |
| `OfflineBadge.kt` | core-base/ui | 3 | GAP-4 |
| `LoadMoreFooter.kt` | core-base/ui | 3 | GAP-6 |
| `PagingScreenContent.kt` | core-base/ui | 3 | GAP-8 |
| Lottie JSON assets (5) | core-base/ui/composeResources | 3 | GAP-5, IG-16 |

### Modified Files
| File | Module | Phase | Gap |
|------|--------|-------|-----|
| `core-base/store/build.gradle.kts` | core-base/store | 1 | IG-1 (add koin-core) |
| `StoreRegistry.kt` → `ApplicationStoreRegistry` | core/data | 1 | IG-9 |
| `RepositoryModule.kt` | core/data | 1, 2 | GAP-3 |
| `CurrencyRatesModule.kt` | feature/currency-rates | 1 | GAP-3 |
| `CryptoModule.kt` | feature/crypto | 1 | GAP-3 |
| `CurrencyRatesViewModel.kt` | feature/currency-rates | 1 | GAP-3, IG-10 |
| `RateHistoryViewModel.kt` | feature/currency-rates | 1 | GAP-3, IG-10 |
| `CryptoWatchlistViewModel.kt` | feature/crypto | 1 | GAP-3, IG-10 |
| `CoinDetailViewModel.kt` | feature/crypto | 1 | GAP-3, IG-10 |
| `ExchangeRatesStore.kt` | core/data/store | 2 | GAP-1, IG-11 |
| `CoinMarketsStore.kt` | core/data/store | 2 | GAP-1, IG-14 |
| `CoinDetailStore.kt` | core/data/store | 2 | GAP-1 |
| `RateHistoryStore.kt` | core/data/store | 2 | GAP-1 |
| `AppDatabase.kt` | core/database | 2 | IG-7, IG-20 |
| `StoreData.kt` | core-base/store | 2 | IG-3 |
| `StoreDataExtensions.kt` | core-base/store | 2 | IG-17 |
| `StoreDataMapper.kt` | core-base/store | 2 | IG-3 |
| `ScreenState.kt` | core-base/store | 3 | IG-4 |
| `DecisionEngine.kt` | core-base/store | 3 | IG-5 |
| `ScreenStateExtensions.kt` | core-base/store | 3 | IG-6 |
| `PagingScreenStream.kt` | core-base/store | 3 | IG-8 |
| `ScreenContent.kt` | core-base/ui | 3 | GAP-5, IG-15 |
| `DataFreshnessIndicator.kt` | core-base/ui | 3 | GAP-4 |
| `libs.versions.toml` | gradle | 3 | GAP-5 |
| `core-base/ui/build.gradle.kts` | core-base/ui | 3 | GAP-5, IG-19 |

---

## Dependency Graph

```
Phase 1 (Architecture)          Phase 2 (Database)           Phase 3 (UI)
┌─────────────────┐            ┌─────────────────┐          ┌─────────────────┐
│ 1.1 Koin dep    │            │ 2.1 Entities+DAO│          │ 3.1 Compottie   │
│  (core-base/    │            │ + TypeConverters │          │  + kotlinx-dt   │
│   store)  IG-1  │            │ + Mappers  IG-7 │          │  dep add  IG-19 │
└────────┬────────┘            │ IG-12,13,14     │          └────────┬────────┘
         │                     └────────┬────────┘                   │
┌────────▼────────┐                     │                   ┌────────▼────────┐
│ 1.2 StoreRegistry│            ┌────────▼────────┐         │ 3.2 StateContent│
│   base (core-   │            │ 2.2 SourceOfTruth│         │   + Lottie      │
│   base/store)   │            │ wiring IG-11     │         └────────┬────────┘
└────────┬────────┘            └────────┬────────┘                   │
         │                              │                   ┌────────▼────────┐
┌────────▼────────┐            ┌────────▼────────┐         │ 3.3 ScreenState │
│ 1.3 Application │            │ 2.3 Wall-clock   │────────>│ + DecisionEngine│
│ StoreRegistry   │            │ timestamps       │         │ IG-4,5,6        │
│ + Repository    │───────────>│ IG-3,17          │         └────────┬────────┘
│ Layer IG-2,10   │            └─────────────────┘                   │
└─────────────────┘                                         ┌────────▼────────┐
                                                            │ 3.4 Freshness  │
                                                            │ + timestamps   │
                                                            │ IG-19          │
                                                            └────────┬────────┘
                                                                     │
                                                            ┌────────▼────────┐
                                                            │ 3.5 PagingStream│
                                                            │ error IG-8     │
                                                            └────────┬────────┘
                                                                     │
                                                            ┌────────▼────────┐
                                                            │ 3.6 LoadMore   │
                                                            │ Footer IG-21   │
                                                            └────────┬────────┘
                                                                     │
                                                            ┌────────▼────────┐
                                                            │ 3.7 PagingScreen│
                                                            │   Content       │
                                                            └─────────────────┘
```

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Room migration V1→V2 breaks existing installs | Data loss | Destructive migration OK for template (no prod users) |
| Compottie binary size increase | ~1-2MB APK | Use `compottie-lite` if expressions unneeded |
| Lottie assets quality | Poor animations | Source from LottieFiles free tier or create minimal custom |
| SourceOfTruth complexity | Store behavior changes | Keep createMemoryStore as fallback, feature-flag DB stores |
| Repository layer adds indirection | More files | Worth it for clean architecture — features never see Store5 |

---

## Success Criteria

### Phase 1 — Architecture
- [ ] `core-base/store` has `koin-core` dependency (IG-1)
- [ ] `StoreRegistry` abstract base in `core-base/store`, `ApplicationStoreRegistry` in `core/data` (IG-9)
- [ ] Repository interfaces in `core/domain`, implementations in `core/data` (IG-2)
- [ ] No `CoroutineScope`/`NetworkMonitor` in repository interface signatures (IG-10)
- [ ] No `org.mobilenativefoundation.store` imports in any feature module
- [ ] All Koin DI resolves correctly — app runs with repositories

### Phase 2 — Database
- [ ] 4 Room entities + 4 DAOs + type converters + entity mappers created (IG-7, IG-12, IG-13)
- [ ] `CoinMarketEntity` has `page: Int` column for paginated upsert (IG-14)
- [ ] All stores use `SourceOfTruth.of()` with Room DAOs (not `createMemoryStore`)
- [ ] `Validator.of {}` used (not `DefaultValidator.withTtl`) (IG-11)
- [ ] `StoreData.fetchedAtInstant: Instant?` survives process restart (IG-3)
- [ ] `StoreDataExtensions` preserve `fetchedAtInstant` in all transformations (IG-17)
- [ ] Kill app → reopen → cached data appears instantly with correct "Last updated X ago"
- [ ] `fallbackToDestructiveMigration()` for V1→V2 (IG-20)

### Phase 3 — Professional UI
- [ ] `ScreenState.Content` has `fetchedAt: Instant?` field (IG-4)
- [ ] `DecisionEngine` propagates `fetchedAtInstant` → `Content.fetchedAt` (IG-5)
- [ ] `ScreenStateExtensions` preserve `fetchedAt` in `mapContent`/`combineContent` (IG-6)
- [ ] `PagingScreenStream.loadMoreError` is public `StateFlow` (IG-8)
- [ ] `kotlinx-datetime` in `core-base/ui` deps (IG-19)
- [ ] All state views (loading/empty/error/no-network) show Lottie animations by default
- [ ] State views fully customizable: title, description, icon, lottie, action button
- [ ] Offline mode: data visible with OfflineBadge, reconnect auto-refreshes
- [ ] Pagination auto-trigger debounced at 300ms (IG-21)
- [ ] Pagination footer shows progress + end-of-list + error retry
- [ ] Lottie assets sourced and bundled (IG-16)

### Gaps Explicitly NOT Addressed
- [ ] IG-22: EMI calculator — no repository needed (pure offline calculation)
- [ ] IG-23: `StoreDataMapper` EMPTY_SENTINEL — already handled in prior commit
