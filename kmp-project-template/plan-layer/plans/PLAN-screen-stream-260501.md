# PLAN-screen-stream-260501: Unified ScreenDataStream — Network-Fused Store → UI State

| Field | Value |
|-------|-------|
| ID | screen-stream-260501 |
| Status | Draft (v3 — cmp-network-monitor integrated) |
| Priority | P0 |
| Scope | `core-base/store` + `core-base/ui` + `core/data` (migration) |
| Created | 2026-05-01 |
| Updated | 2026-05-02 |
| Prerequisites | PLAN-storedata-api-260430 (StoreData, StoreDataExtensions, StorePagingSource) |
| Effort | ~6-8 hours |
| Parent Plan | PLAN-store-offline-260429 |
| Library Deps | `cmp-network-monitor` (core), `cmp-network-monitor-compose` (UI) |

---

## Problem Statement

Every ViewModel repeats ~150-200 lines of identical boilerplate combining Store data + network state → UI state. Network monitoring is handled by a thin third-party wrapper (`dev.jordond.connectivity`) that provides only `Flow<Boolean>` with no quality/type/captive-portal awareness.

### Pain Points

1. **Decision logic duplicated** — Every VM manually combines StoreData + network state → UI state
2. **NetworkMonitor too thin** — Current interface is just `Flow<Boolean>`, no quality/type/captive info
3. **Third-party dep redundant** — `cmp-network-monitor` already exists in the workspace with richer API
4. **No retry intelligence** — Fetchers don't leverage network-aware retry
5. **Paging has no unified state** — Raw `loadPage()` with no network/empty/error orchestration
6. **WiFi↔Cell handoff flicker** — Raw `isOnline` causes 200ms UI flash during handoffs

### Goal

One function call in ViewModel that produces a `Flow<ScreenState<T>>` with ALL decisions pre-made, powered by `cmp-network-monitor`:

```kotlin
val stream = accountsStore.asScreenStream(
    key = clientId,
    networkMonitor = networkMonitor,  // cmp-network-monitor's NetworkMonitor
    scope = viewModelScope,
)
// That's it. No observeNetwork, no handleNetworkStatus, no retry logic needed.
```

---

## Architecture

### Dependency Direction (Simplified — No Interface Move Needed)

```
cmp-network-monitor          ← Library (zero deps beyond kotlinx-coroutines)
       ↑
core-base/store              ← api(cmp-network-monitor) + ScreenState + DecisionEngine + ScreenDataStream
       ↑
core-base/ui                 ← api(core-base/store) + api(cmp-network-monitor-compose) + ScreenContent
       ↑
core/data                    ← NetworkMonitorImpl → delegates to library singleton
       ↑
feature/*                    ← Consumer ViewModels (50 lines each)
```

**Key insight:** `cmp-network-monitor` IS the interface. Its `NetworkMonitor` interface has zero dependencies. No need to create a wrapper in `core-base/common`. The library is designed for exactly this use case.

### Decision Matrix (Enhanced with NetworkStatus)

| isEmpty? | NetworkStatus | error | isRefreshing | → ScreenState |
|:--------:|:------------:|:-----:|:------------:|:-------------:|
| true | Available | null | - | `Loading` |
| true | Unavailable | null | - | `NoNetwork` |
| true | CaptivePortal | null | - | `NoNetwork(captive=true)` |
| true | Available | IOException | - | `NoNetwork` |
| true | Unavailable | IOException | - | `NoNetwork` |
| true | Available | other | - | `Error(ex)` |
| false | Available | null | false | `Content(data, FRESH)` |
| false | Unavailable | null | false | `Content(data, STALE)` |
| false | CaptivePortal | null | false | `Content(data, STALE)` |
| false | - | null | true | `Content(data, UPDATING)` |
| false | - | non-null | - | `Content(data, STALE)` |

### Data Flow

```
                           ┌─── isOnlineDebounced(300ms) (goes true) ──┐
                           │                                            ↓
refreshTrigger ──onStart──►│◄─────────────────────────────────── autoRefreshOnReconnect
        │                  │
        ↓                  ↓
  Store.streamDataWithErrors(key)  ──┐
                                     ├──► combine() ──► DecisionEngine ──► ScreenState<T>
  NetworkMonitor.networkStatus ──────┘         ↓
                                        lastContentCache (preserves data during refresh)
```

---

## Implementation Tasks

### Phase 0: Migration — Replace jordond/connectivity with cmp-network-monitor

#### Task 0.1: Remove jordond/connectivity dependency

**Files to modify:**
- `core/data/build.gradle.kts` — Remove `connectivity-core`, `connectivity-device`, `connectivity-http`
- `gradle/libs.versions.toml` — Remove `connectivity` version and 6 library entries

**Files to DELETE:**
- `core/data/src/commonMain/.../ConnectivityProvider.kt` (expect)
- `core/data/src/mobileMain/.../ConnectivityProvider.mobile.kt` (actual)
- `core/data/src/jvmJsCommonMain/.../ConnectivityProvider.jvmJsCommon.kt` (actual)

#### Task 0.2: Rewrite NetworkMonitorImpl using cmp-network-monitor

**File:** `core/data/src/commonMain/kotlin/org/mifos/core/data/repositoryImpl/NetworkMonitorImpl.kt`

```kotlin
package org.mifos.core.data.repositoryImpl

import io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkMonitor
import io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkMonitorProvider
import io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkStatus
import kotlinx.coroutines.flow.StateFlow

/**
 * Singleton NetworkMonitor backed by cmp-network-monitor.
 * Auto-initializes on first access via NetworkMonitorProvider.
 */
class NetworkMonitorImpl : NetworkMonitor by NetworkMonitorProvider.install()
```

#### Task 0.3: Update NetworkMonitor interface (typealias)

**File:** `core/data/src/commonMain/kotlin/org/mifos/core/data/repository/NetworkMonitor.kt`

```kotlin
package org.mifos.core.data.repository

// Backward-compatible typealias — existing consumers keep their import
typealias NetworkMonitor = io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkMonitor
```

#### Task 0.4: Update Koin module

**File:** `core/data/src/commonMain/kotlin/org/mifos/core/data/di/RepositoryModule.kt`

```kotlin
// Replace:
singleOf(::NetworkMonitorImpl) bind NetworkMonitor::class
// With:
single<NetworkMonitor> { NetworkMonitorProvider.install() }
```

#### Task 0.5: Update 2 existing consumers

1. **AuthenticatedNavbarNavigationViewModel** — Now gets `StateFlow<Boolean>` (was `Flow<Boolean>`). Remove `.stateIn()` — it's already a StateFlow.
2. **MainActivity** — Same: `networkMonitor.isOnline` is already StateFlow.

#### Task 0.6: Add cmp-network-monitor dependency to core/data

**File:** `core/data/build.gradle.kts`
```kotlin
commonMain.dependencies {
    api(libs.cmp.network.monitor)
}
```

**File:** `gradle/libs.versions.toml` — Already has `cmp-network-monitor` entry ✅

---

### Phase 1: Core Types (core-base/store)

#### Task 1.1: Add cmp-network-monitor dependency

**File:** `core-base/store/build.gradle.kts`
```kotlin
commonMain.dependencies {
    api(libs.cmp.network.monitor)  // NetworkMonitor, NetworkStatus types
    // ... existing store5, coroutines deps
}
```

#### Task 1.2: ScreenState sealed interface + DataFreshness

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/ScreenState.kt`

```kotlin
package template.core.base.store

/**
 * Unified UI state produced by [ScreenDataStream].
 * Replaces per-ViewModel ScreenUiState + isFromCache + isRefreshing + networkStatus.
 */
sealed interface ScreenState<out T> {

    /** Initial load — no data available yet. */
    data object Loading : ScreenState<Nothing>

    /** Data fetched successfully but content is empty (e.g., empty list). */
    data object Empty : ScreenState<Nothing>

    /**
     * No network connectivity and no cached data available.
     * @param isCaptivePortal true when behind a captive portal (hotel WiFi login).
     */
    data class NoNetwork(
        val isCaptivePortal: Boolean = false,
    ) : ScreenState<Nothing>

    /** Error occurred with no usable cached data. */
    data class Error(
        val error: Throwable,
        val isNetworkError: Boolean = false,
    ) : ScreenState<Nothing>

    /** Data available with freshness metadata. */
    data class Content<T>(
        val data: T,
        val freshness: DataFreshness,
    ) : ScreenState<T>
}

/**
 * Indicates how fresh the data in [ScreenState.Content] is.
 */
enum class DataFreshness {
    /** Online, data is the latest from server. */
    FRESH,
    /** Showing cached data — offline or refresh failed. */
    STALE,
    /** Has cached data, network refresh currently in flight. */
    UPDATING,
}
```

#### Task 1.3: DecisionEngine (uses NetworkStatus, not just Boolean)

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/DecisionEngine.kt`

```kotlin
package template.core.base.store

import io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkStatus
import kotlinx.io.IOException

/**
 * Pure function combining StoreData metadata + NetworkStatus into ScreenState.
 * No side effects, no coroutines — exhaustively unit testable.
 *
 * Uses full [NetworkStatus] (not just Boolean) to detect captive portals.
 */
object DecisionEngine {

    fun <T> decide(
        storeData: StoreData<T>,
        networkStatus: NetworkStatus,
    ): ScreenState<T> {
        val noData = storeData.isEmpty
        val error = storeData.error
        val isOnline = networkStatus is NetworkStatus.Available
        val isCaptivePortal = networkStatus is NetworkStatus.CaptivePortal

        // === No data branch ===
        if (noData) {
            return when {
                isCaptivePortal -> ScreenState.NoNetwork(isCaptivePortal = true)
                !isOnline -> ScreenState.NoNetwork()
                error != null && error.isNetworkError() -> ScreenState.NoNetwork()
                error != null -> ScreenState.Error(error, isNetworkError = false)
                else -> ScreenState.Loading
            }
        }

        // === Has data branch ===
        return when {
            storeData.isRefreshing -> ScreenState.Content(storeData.data, DataFreshness.UPDATING)
            !isOnline || isCaptivePortal -> ScreenState.Content(storeData.data, DataFreshness.STALE)
            error != null -> ScreenState.Content(storeData.data, DataFreshness.STALE)
            else -> ScreenState.Content(storeData.data, DataFreshness.FRESH)
        }
    }

    private fun Throwable.isNetworkError(): Boolean {
        return this is IOException ||
            cause is IOException ||
            this::class.simpleName?.contains("Connect") == true ||
            this::class.simpleName?.contains("Timeout") == true
    }
}
```

#### Task 1.4: ScreenState Flow Extensions

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/ScreenStateExtensions.kt`

```kotlin
package template.core.base.store

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.map

/**
 * Transforms only [ScreenState.Content] data, passing through all other states unchanged.
 */
fun <T, R> Flow<ScreenState<T>>.mapContent(
    transform: (data: T, freshness: DataFreshness) -> R,
): Flow<ScreenState<R>> = map { state ->
    when (state) {
        is ScreenState.Content -> ScreenState.Content(
            data = transform(state.data, state.freshness),
            freshness = state.freshness,
        )
        is ScreenState.Loading -> ScreenState.Loading
        is ScreenState.Empty -> ScreenState.Empty
        is ScreenState.NoNetwork -> state
        is ScreenState.Error -> state
    }
}

/**
 * Combines ScreenState with a local state flow for reactive filter/sort/preferences.
 */
fun <T, S, R> Flow<ScreenState<T>>.combineContent(
    other: Flow<S>,
    transform: (data: T, extra: S, freshness: DataFreshness) -> R,
): Flow<ScreenState<R>> = combine(this, other) { state, extra ->
    when (state) {
        is ScreenState.Content -> ScreenState.Content(
            data = transform(state.data, extra, state.freshness),
            freshness = state.freshness,
        )
        is ScreenState.Loading -> ScreenState.Loading
        is ScreenState.Empty -> ScreenState.Empty
        is ScreenState.NoNetwork -> state
        is ScreenState.Error -> state
    }
}

/**
 * Converts Content to Empty when business-level predicate says data is empty.
 * Applied AFTER DecisionEngine (which only handles structural empty from Store).
 */
fun <T> Flow<ScreenState<T>>.emptyIfContent(
    predicate: (T) -> Boolean,
): Flow<ScreenState<T>> = map { state ->
    when (state) {
        is ScreenState.Content -> if (predicate(state.data)) ScreenState.Empty else state
        else -> state
    }
}

/** Extracts data from Content state or null for other states. */
val <T> ScreenState<T>.dataOrNull: T?
    get() = (this as? ScreenState.Content)?.data

/** True if state has displayable content. */
val <T> ScreenState<T>.hasContent: Boolean
    get() = this is ScreenState.Content

/** Maps Error throwable to a user-facing type. */
fun <T> Flow<ScreenState<T>>.mapError(
    transform: (Throwable) -> Throwable,
): Flow<ScreenState<T>> = map { state ->
    when (state) {
        is ScreenState.Error -> ScreenState.Error(
            error = transform(state.error),
            isNetworkError = state.isNetworkError,
        )
        else -> state
    }
}
```

---

### Phase 2: Stream Combinator (core-base/store)

#### Task 2.1: Add no-fallback `streamDataWithErrors` overload

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/StoreDataExtensions.kt` (ADD overload)

```kotlin
/**
 * Like [streamDataWithErrors] but without requiring a fallback value.
 * Emits StoreData with isEmpty=true when error arrives before any data.
 * Used by ScreenDataStream where DecisionEngine handles the no-data case.
 */
fun <Key : Any, Output : Any> Store<Key, Output>.streamDataNoFallback(
    key: Key,
    refresh: Boolean = true,
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>>
```

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/StoreDataMapper.kt` (ADD mapper)

```kotlin
/**
 * Maps Store responses to StoreData without requiring a fallback.
 * On error before any data: emits StoreData with isEmpty=true and error set.
 * Uses internal sentinel — data field is only accessed when isEmpty=false.
 */
@Suppress("UNCHECKED_CAST")
internal fun <Output> Flow<StoreReadResponse<Output>>.mapToStoreDataNoFallback(
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    var lastData: Output? = null
    return transform { response ->
        when (response) {
            is StoreReadResponse.Data -> {
                lastData = response.value
                emit(StoreData(
                    data = response.value,
                    origin = response.origin.toDataOrigin(),
                    isEmpty = isEmpty(response.value),
                ))
            }
            is StoreReadResponse.Error -> {
                val data = lastData
                if (data != null) {
                    emit(StoreData(
                        data = data,
                        origin = DataOrigin.CACHE,
                        error = response.toThrowable(),
                        isEmpty = false,
                    ))
                } else {
                    // No data yet — emit empty with error for DecisionEngine
                    emit(StoreData(
                        data = null as Output, // Safe: only accessed when isEmpty=false
                        origin = DataOrigin.NETWORK,
                        error = response.toThrowable(),
                        isEmpty = true,
                    ))
                }
            }
            is StoreReadResponse.Loading -> {
                // If we have previous data, emit as refreshing
                lastData?.let { data ->
                    emit(StoreData(
                        data = data,
                        origin = DataOrigin.CACHE,
                        isRefreshing = true,
                        isEmpty = false,
                    ))
                }
            }
            else -> { /* Initial, NoNewData — skip */ }
        }
    }
}
```

#### Task 2.2: ScreenDataStream class + asScreenStream factory

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/ScreenDataStream.kt`

```kotlin
package template.core.base.store

import io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkMonitor
import io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkStatus
import io.github.mobilebytelabs.kmptoolkit.networkmonitor.isOnlineDebounced
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.flow.drop
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.launch
import org.mobilenativefoundation.store.store5.Store

/**
 * A unified data stream combining Store data + cmp-network-monitor into pre-decided [ScreenState].
 *
 * Eliminates all ViewModel boilerplate:
 * - No manual network observation (auto-refreshes on reconnect)
 * - No manual DataState → UI state mapping (DecisionEngine handles it)
 * - No manual retry/refresh logic (built-in)
 * - No WiFi↔Cell handoff flicker (debounced at 300ms)
 * - Preserves existing content during pull-to-refresh (lastContent cache)
 * - Detects captive portals (hotel WiFi login pages)
 *
 * Usage:
 * ```
 * class MyViewModel(store: Store<Long, Data>, networkMonitor: NetworkMonitor) : ViewModel() {
 *     private val stream = store.asScreenStream(
 *         key = clientId,
 *         networkMonitor = networkMonitor,
 *         scope = viewModelScope,
 *     )
 *     val uiState = stream.state
 *         .mapContent { data, _ -> transform(data) }
 *         .emptyIfContent { it.items.isEmpty() }
 *         .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), ScreenState.Loading)
 *     fun onRetry() = stream.retry()
 * }
 * ```
 */
class ScreenDataStream<T> internal constructor(
    /**
     * Cold Flow of ScreenState decisions. Consumer should call .stateIn() once.
     * Intentionally cold Flow (not StateFlow) to avoid double-sharing
     * when consumer applies mapContent/combineContent before stateIn.
     */
    val state: Flow<ScreenState<T>>,
    private val refreshTrigger: MutableSharedFlow<Unit>,
) {
    /** Trigger a network refresh. Preserves existing content while loading. */
    fun refresh() {
        refreshTrigger.tryEmit(Unit)
    }

    /** Retry loading (semantic alias for refresh — used on error/no-network screens). */
    fun retry() = refresh()
}

/**
 * Creates a [ScreenDataStream] from this Store, fusing network state via cmp-network-monitor.
 *
 * Features:
 * - Auto-refreshes when network reconnects (offline→online, debounced 300ms)
 * - Preserves last known content during refresh (no flicker to Loading)
 * - DecisionEngine maps all StoreData + NetworkStatus combinations to ScreenState
 * - Handles captive portal detection
 * - Single refresh/retry entry point
 *
 * @param key Store key to stream data for.
 * @param networkMonitor cmp-network-monitor's NetworkMonitor (injected via Koin).
 * @param scope CoroutineScope (typically viewModelScope) for auto-refresh coroutine.
 * @param isEmpty Optional predicate for "no data has arrived yet from Store".
 *   NOT for "empty list" detection — use [emptyIfContent] for that.
 */
@OptIn(ExperimentalCoroutinesApi::class)
fun <Key : Any, Output : Any> Store<Key, Output>.asScreenStream(
    key: Key,
    networkMonitor: NetworkMonitor,
    scope: CoroutineScope,
    isEmpty: (Output) -> Boolean = { false },
): ScreenDataStream<Output> {
    val refreshTrigger = MutableSharedFlow<Unit>(extraBufferCapacity = 1)

    // Auto-refresh when network reconnects (debounced to avoid WiFi↔Cell flicker)
    scope.launch {
        networkMonitor.isOnlineDebounced(300L)
            .distinctUntilChanged()
            .filter { it }
            .drop(1) // Skip initial emission (don't double-load on start)
            .collect { refreshTrigger.tryEmit(Unit) }
    }

    // Track last known content to preserve during refresh
    var lastContent: StoreData<Output>? = null

    val storeFlow: Flow<StoreData<Output>> = refreshTrigger
        .onStart { emit(Unit) } // Initial load on subscription
        .flatMapLatest {
            streamDataNoFallback(key = key, isEmpty = isEmpty)
        }
        .map { storeData ->
            if (!storeData.isEmpty) {
                lastContent = storeData
                storeData
            } else if (storeData.isEmpty && lastContent != null && storeData.error == null) {
                // Refresh in progress — preserve last content with UPDATING
                lastContent!!.copy(isRefreshing = true)
            } else {
                storeData
            }
        }

    // Combine with FULL NetworkStatus (not just Boolean) for captive portal detection
    val screenStateFlow: Flow<ScreenState<Output>> = combine(
        storeFlow,
        networkMonitor.networkStatus,
    ) { storeData, status ->
        DecisionEngine.decide(storeData, status)
    }

    return ScreenDataStream(
        state = screenStateFlow,
        refreshTrigger = refreshTrigger,
    )
}

/**
 * Overload accepting a Flow<Key> for dynamic keys (e.g., selected client from DataStore).
 * Re-streams from Store when key changes. Resets lastContent on key change.
 */
@OptIn(ExperimentalCoroutinesApi::class)
fun <Key : Any, Output : Any> Store<Key, Output>.asScreenStream(
    keyFlow: Flow<Key>,
    networkMonitor: NetworkMonitor,
    scope: CoroutineScope,
    isEmpty: (Output) -> Boolean = { false },
): ScreenDataStream<Output> {
    val refreshTrigger = MutableSharedFlow<Unit>(extraBufferCapacity = 1)

    scope.launch {
        networkMonitor.isOnlineDebounced(300L)
            .distinctUntilChanged()
            .filter { it }
            .drop(1)
            .collect { refreshTrigger.tryEmit(Unit) }
    }

    var lastContent: StoreData<Output>? = null

    val storeFlow: Flow<StoreData<Output>> = combine(
        keyFlow,
        refreshTrigger.onStart { emit(Unit) },
    ) { key, _ -> key }
        .flatMapLatest { key ->
            lastContent = null // Reset on key change
            streamDataNoFallback(key = key, isEmpty = isEmpty)
        }
        .map { storeData ->
            if (!storeData.isEmpty) {
                lastContent = storeData
                storeData
            } else if (storeData.isEmpty && lastContent != null && storeData.error == null) {
                lastContent!!.copy(isRefreshing = true)
            } else {
                storeData
            }
        }

    val screenStateFlow: Flow<ScreenState<Output>> = combine(
        storeFlow,
        networkMonitor.networkStatus,
    ) { storeData, status ->
        DecisionEngine.decide(storeData, status)
    }

    return ScreenDataStream(
        state = screenStateFlow,
        refreshTrigger = refreshTrigger,
    )
}
```

---

### Phase 3: Paging Variant (core-base/store)

#### Task 3.1: PagingScreenStream

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/PagingScreenStream.kt`

```kotlin
package template.core.base.store

import io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkMonitor
import io.github.mobilebytelabs.kmptoolkit.networkmonitor.NetworkStatus
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import org.mobilenativefoundation.store.store5.Store

/**
 * Paginated variant of [ScreenDataStream].
 * Manages page loading, appending, error surfacing, and unified state for infinite lists.
 *
 * Usage:
 * ```
 * val pagingStream = clientStore.asPagingScreenStream(
 *     networkMonitor = networkMonitor,
 *     scope = viewModelScope,
 *     pageSize = 20,
 * )
 * val uiState = pagingStream.state  // Flow<ScreenState<List<Client>>>
 * fun loadMore() = pagingStream.loadNextPage()
 * ```
 */
class PagingScreenStream<T : Any> internal constructor(
    val state: Flow<ScreenState<List<T>>>,
    val hasMore: StateFlow<Boolean>,
    val isLoadingMore: StateFlow<Boolean>,
    private val scope: CoroutineScope,
    private val store: Store<PageKey, List<T>>,
    private val networkMonitor: NetworkMonitor,
    private val pageSize: Int,
    private val query: String?,
    private val _items: MutableStateFlow<List<T>>,
    private val _hasMore: MutableStateFlow<Boolean>,
    private val _isLoadingMore: MutableStateFlow<Boolean>,
    private val _isInitialLoading: MutableStateFlow<Boolean>,
    private val _error: MutableStateFlow<Throwable?>,
    private val _currentPage: MutableStateFlow<Int>,
) {
    /** Load the next page. No-op if already loading or no more pages. */
    fun loadNextPage() {
        if (_isLoadingMore.value || !_hasMore.value) return
        scope.launch {
            _isLoadingMore.value = true
            _error.value = null
            val nextPage = _currentPage.value + 1
            val pageKey = PageKey(page = nextPage, pageSize = pageSize, query = query)
            when (val result = store.loadPage(pageKey)) {
                is StorePageResult.Success -> {
                    _items.update { it + result.items }
                    _currentPage.value = nextPage
                    _hasMore.value = result.nextKey != null
                }
                is StorePageResult.Error -> {
                    _error.value = result.error
                }
            }
            _isLoadingMore.value = false
        }
    }

    /** Refresh from page 0, clearing all loaded pages. */
    fun refresh() {
        scope.launch {
            _currentPage.value = 0
            _items.value = emptyList()
            _hasMore.value = true
            _error.value = null
            _isInitialLoading.value = true
            loadInitialPage()
        }
    }

    fun retry() = refresh()

    internal fun loadInitialPage() {
        scope.launch {
            val pageKey = PageKey.first(pageSize = pageSize, query = query)
            when (val result = store.loadPage(pageKey)) {
                is StorePageResult.Success -> {
                    _items.value = result.items
                    _hasMore.value = result.nextKey != null
                }
                is StorePageResult.Error -> {
                    _error.value = result.error
                }
            }
            _isInitialLoading.value = false
        }
    }
}

/**
 * Creates a [PagingScreenStream] with network-fused state via cmp-network-monitor.
 */
fun <Value : Any> Store<PageKey, List<Value>>.asPagingScreenStream(
    networkMonitor: NetworkMonitor,
    scope: CoroutineScope,
    pageSize: Int = PageKey.DEFAULT_PAGE_SIZE,
    query: String? = null,
): PagingScreenStream<Value> {
    val items = MutableStateFlow<List<Value>>(emptyList())
    val hasMore = MutableStateFlow(true)
    val isLoadingMore = MutableStateFlow(false)
    val isInitialLoading = MutableStateFlow(true)
    val error = MutableStateFlow<Throwable?>(null)
    val currentPage = MutableStateFlow(0)

    val screenState: Flow<ScreenState<List<Value>>> = combine(
        items,
        networkMonitor.networkStatus,
        isInitialLoading,
        error,
    ) { itemList, status, loading, err ->
        val isOnline = status is NetworkStatus.Available
        val isCaptive = status is NetworkStatus.CaptivePortal
        when {
            loading && itemList.isEmpty() && (!isOnline || isCaptive) ->
                ScreenState.NoNetwork(isCaptivePortal = isCaptive)
            loading && itemList.isEmpty() -> ScreenState.Loading
            err != null && itemList.isEmpty() && !isOnline ->
                ScreenState.NoNetwork()
            err != null && itemList.isEmpty() -> ScreenState.Error(err)
            itemList.isEmpty() && !loading -> ScreenState.Empty
            !isOnline || isCaptive -> ScreenState.Content(itemList, DataFreshness.STALE)
            loading -> ScreenState.Content(itemList, DataFreshness.UPDATING)
            else -> ScreenState.Content(itemList, DataFreshness.FRESH)
        }
    }

    return PagingScreenStream(
        state = screenState,
        hasMore = hasMore.asStateFlow(),
        isLoadingMore = isLoadingMore.asStateFlow(),
        scope = scope,
        store = this,
        networkMonitor = networkMonitor,
        pageSize = pageSize,
        query = query,
        _items = items,
        _hasMore = hasMore,
        _isLoadingMore = isLoadingMore,
        _isInitialLoading = isInitialLoading,
        _error = error,
        _currentPage = currentPage,
    ).also { it.loadInitialPage() }
}
```

---

### Phase 4: UI Layer (core-base/ui)

#### Task 4.1: Add dependencies

**File:** `core-base/ui/build.gradle.kts`
```kotlin
commonMain.dependencies {
    api(project(":core-base:store"))                // ScreenState, DataFreshness types
    api(libs.cmp.network.monitor.compose)          // ConnectivityBanner, collectIsOnlineAsState
    // ... existing compose deps
}
```

#### Task 4.2: ScreenContent Composable

**File:** `core-base/ui/src/commonMain/kotlin/template/core/base/ui/ScreenContent.kt`

```kotlin
package template.core.base.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.runtime.Composable
import io.github.mobilebytelabs.kmptoolkit.networkmonitor.compose.ConnectivityBanner
import template.core.base.store.DataFreshness
import template.core.base.store.ScreenState

/**
 * Generic composable that renders any [ScreenState] with sensible defaults.
 * Integrates cmp-network-monitor-compose's [ConnectivityBanner] for STALE state.
 *
 * Usage:
 * ```
 * @Composable
 * fun SavingsScreen(vm: SavingsViewModel) {
 *     val state by vm.uiState.collectAsStateWithLifecycle()
 *     ScreenContent(state = state, onRetry = vm::onRetry) { data, freshness ->
 *         SavingsList(data.accounts)
 *     }
 * }
 * ```
 */
@Composable
fun <T> ScreenContent(
    state: ScreenState<T>,
    onRetry: () -> Unit,
    showFreshnessIndicator: Boolean = true,
    loading: @Composable () -> Unit = { DefaultLoadingContent() },
    empty: @Composable () -> Unit = { DefaultEmptyContent() },
    noNetwork: @Composable (isCaptivePortal: Boolean) -> Unit = { captive ->
        DefaultNoNetworkContent(onRetry, isCaptivePortal = captive)
    },
    error: @Composable (Throwable) -> Unit = { DefaultErrorContent(it, onRetry) },
    content: @Composable (data: T, freshness: DataFreshness) -> Unit,
) {
    when (state) {
        is ScreenState.Loading -> loading()
        is ScreenState.Empty -> empty()
        is ScreenState.NoNetwork -> noNetwork(state.isCaptivePortal)
        is ScreenState.Error -> error(state.error)
        is ScreenState.Content -> {
            Column {
                if (showFreshnessIndicator) {
                    DataFreshnessIndicator(freshness = state.freshness)
                }
                content(state.data, state.freshness)
            }
        }
    }
}
```

#### Task 4.3: DataFreshnessIndicator (uses ConnectivityBanner)

**File:** `core-base/ui/src/commonMain/kotlin/template/core/base/ui/DataFreshnessIndicator.kt`

```kotlin
package template.core.base.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import template.core.base.store.DataFreshness

/**
 * Shows freshness status above content:
 * - FRESH → nothing (hidden)
 * - STALE → "Offline — showing cached data" banner
 * - UPDATING → "Updating..." with progress indicator
 */
@Composable
fun DataFreshnessIndicator(
    freshness: DataFreshness,
    modifier: Modifier = Modifier,
) {
    AnimatedVisibility(
        visible = freshness != DataFreshness.FRESH,
        enter = expandVertically(expandFrom = Alignment.Top),
        exit = shrinkVertically(shrinkTowards = Alignment.Top),
        modifier = modifier,
    ) {
        when (freshness) {
            DataFreshness.STALE -> {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(horizontal = 16.dp, vertical = 6.dp),
                    contentAlignment = Alignment.Center,
                ) {
                    Text(
                        text = "Offline — showing cached data",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            DataFreshness.UPDATING -> {
                LinearProgressIndicator(
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.primary,
                )
            }
            DataFreshness.FRESH -> { /* hidden */ }
        }
    }
}
```

---

### Phase 5: Tests

#### Task 5.1: DecisionEngine exhaustive tests

**File:** `core-base/store/src/commonTest/kotlin/template/core/base/store/DecisionEngineTest.kt`

```kotlin
class DecisionEngineTest {
    // No data + NetworkStatus variants
    @Test fun `no data + Available + no error = Loading`()
    @Test fun `no data + Unavailable + no error = NoNetwork`()
    @Test fun `no data + CaptivePortal + no error = NoNetwork(captive=true)`()
    @Test fun `no data + Available + IOException = NoNetwork`()
    @Test fun `no data + Unavailable + IOException = NoNetwork`()
    @Test fun `no data + Available + other error = Error`()

    // Has data + NetworkStatus variants
    @Test fun `has data + Available + no error + not refreshing = Content FRESH`()
    @Test fun `has data + Unavailable = Content STALE`()
    @Test fun `has data + CaptivePortal = Content STALE`()
    @Test fun `has data + refreshing = Content UPDATING`()
    @Test fun `has data + error (refresh failed) = Content STALE`()
    @Test fun `has data + refreshing + Unavailable = Content UPDATING (refreshing wins)`()

    // isNetworkError detection
    @Test fun `isNetworkError - IOException direct`()
    @Test fun `isNetworkError - IOException as cause`()
    @Test fun `isNetworkError - class name contains Connect`()
    @Test fun `isNetworkError - class name contains Timeout`()
    @Test fun `isNetworkError - other exception = false`()
}
```

#### Task 5.2: ScreenDataStream integration tests (Turbine)

#### Task 5.3: ScreenStateExtensions tests

#### Task 5.4: PagingScreenStream tests

(Same test cases as plan v2 — validated correct)

---

### Phase 6: Documentation & Patterns

#### Task 6.1: Fetcher retry pattern (leveraging cmp-network-monitor)

```kotlin
// RECOMMENDED: Wrap Store Fetchers with network-aware retry
val accountsStore = StoreFactory.createStore(
    fetcher = Fetcher.of { clientId: Long ->
        networkMonitor.executeWithRetry(
            RetryPolicy {
                maxAttempts = 3
                backoff = BackoffStrategy.Exponential(baseMs = 1000, maxMs = 10_000)
            }
        ) {
            api.getClientAccounts(clientId)
        }
    },
    sourceOfTruth = ...,
)
```

#### Task 6.2: Migration pattern — single-store screen

**BEFORE** (~200 lines): Manual network observation + DataState mapping + retry logic
**AFTER** (~50 lines): `asScreenStream()` + `mapContent` + `emptyIfContent` + `stateIn`

#### Task 6.3: Multi-store composition pattern

```kotlin
val screenState = combine(savingsStream.state, loansStream.state) { savings, loans ->
    when {
        savings is ScreenState.Loading || loans is ScreenState.Loading -> ScreenState.Loading
        savings is ScreenState.NoNetwork -> savings
        savings is ScreenState.Content && loans is ScreenState.Content -> {
            val freshness = maxOf(savings.freshness, loans.freshness)
            ScreenState.Content(DashboardData(savings.data, loans.data), freshness)
        }
        else -> ScreenState.Loading
    }
}
```

#### Task 6.4: Captive portal UI pattern

```kotlin
// In DefaultNoNetworkContent:
@Composable
fun DefaultNoNetworkContent(onRetry: () -> Unit, isCaptivePortal: Boolean = false) {
    Column(horizontalAlignment = CenterHorizontally) {
        Icon(if (isCaptivePortal) Icons.WifiLock else Icons.WifiOff)
        Text(if (isCaptivePortal) "Sign in to WiFi network" else "No internet connection")
        Button(onClick = onRetry) { Text("Retry") }
    }
}
```

---

## File Manifest

| # | Path | Type | Description |
|---|------|------|-------------|
| 1 | `core/data/build.gradle.kts` | Modified | Remove connectivity deps, add cmp-network-monitor |
| 2 | `core/data/.../ConnectivityProvider.kt` (×3) | DELETE | Removed (jordond library) |
| 3 | `core/data/.../NetworkMonitor.kt` | Modified | Typealias to library |
| 4 | `core/data/.../NetworkMonitorImpl.kt` | Modified | Delegates to library singleton |
| 5 | `core/data/.../RepositoryModule.kt` | Modified | Updated Koin binding |
| 6 | `gradle/libs.versions.toml` | Modified | Remove connectivity entries |
| 7 | `core-base/store/build.gradle.kts` | Modified | Add `api(libs.cmp.network.monitor)` |
| 8 | `core-base/store/.../ScreenState.kt` | New | Sealed interface + DataFreshness |
| 9 | `core-base/store/.../DecisionEngine.kt` | New | Pure decision function (NetworkStatus-aware) |
| 10 | `core-base/store/.../ScreenStateExtensions.kt` | New | mapContent, combineContent, emptyIfContent, mapError |
| 11 | `core-base/store/.../ScreenDataStream.kt` | New | Stream combinator + asScreenStream() factories |
| 12 | `core-base/store/.../PagingScreenStream.kt` | New | Paginated variant |
| 13 | `core-base/store/.../StoreDataExtensions.kt` | Modified | Add streamDataNoFallback |
| 14 | `core-base/store/.../StoreDataMapper.kt` | Modified | Add mapToStoreDataNoFallback |
| 15 | `core-base/ui/build.gradle.kts` | Modified | Add core-base:store + cmp-network-monitor-compose |
| 16 | `core-base/ui/.../ScreenContent.kt` | New | Generic composable renderer |
| 17 | `core-base/ui/.../DataFreshnessIndicator.kt` | New | Freshness banner |
| 18 | `core-base/store/src/commonTest/.../DecisionEngineTest.kt` | New | 17 tests |
| 19 | `core-base/store/src/commonTest/.../ScreenDataStreamTest.kt` | New | Integration tests |
| 20 | `core-base/store/src/commonTest/.../ScreenStateExtensionsTest.kt` | New | Extension tests |
| 21 | `core-base/store/src/commonTest/.../PagingScreenStreamTest.kt` | New | Paging tests |
| 22 | `cmp-navigation/.../AuthenticatedNavbarNavigationViewModel.kt` | Modified | Remove .stateIn() (already StateFlow) |
| 23 | `cmp-android/.../MainActivity.kt` | Modified | StateFlow direct usage |

---

## Gaps Fixed (v3 vs v2)

| # | v2 Gap | v3 Fix |
|---|--------|--------|
| 1 | Interface mismatch (Flow vs StateFlow) | Use library's interface directly — no wrapper |
| 2 | Unnecessary Phase 1 (interface move) | Eliminated — depend on cmp-network-monitor directly |
| 3 | Ignores cmp-network-monitor-compose | Phase 4 integrates ConnectivityBanner + compose extensions |
| 4 | DecisionEngine only uses Boolean | Now uses full `NetworkStatus` (handles CaptivePortal) |
| 5 | No captive portal state | Added `ScreenState.NoNetwork(isCaptivePortal)` |
| 6 | WiFi↔Cell handoff flicker | Uses `isOnlineDebounced(300L)` for reconnect trigger |
| 7 | jordond/connectivity removal missing | Phase 0 handles complete migration |
| 8 | Koin wiring undefined | Task 0.4 explicit Koin binding |
| 9 | Build deps not declared | Tasks 1.1, 4.1 explicit |
| 10 | Retry utilities unused | Phase 6.1 documents Fetcher retry pattern |
| 11 | `streamDataWithErrors` needs no-fallback | Task 2.1: `streamDataNoFallback` + `mapToStoreDataNoFallback` |
| 12 | isNetworkError misses Timeout | Added `Timeout` class name check |

---

## Execution Order

```
Phase 0 (migration)      → Phase 1 (types)           → Phase 2 (stream)
     │                         │                            │
  Remove jordond/            ScreenState                 ScreenDataStream
  connectivity               DecisionEngine(Status)      streamDataNoFallback
  Wire cmp-network-monitor   Extensions                  asScreenStream()
  Update 2 consumers                                     lastContent + debounce
                                                              │
Phase 3 (paging)         → Phase 4 (UI)              → Phase 5 (tests)
     │                         │                            │
  PagingScreenStream       ScreenContent               DecisionEngineTest (17)
  (NetworkStatus-aware)    FreshnessIndicator          ScreenDataStreamTest
  error surfacing          ConnectivityBanner reuse    ExtensionsTest
                                                       PagingStreamTest
                                                            │
                                                      Phase 6 (docs)
                                                            │
                                                       Fetcher retry pattern
                                                       Migration guide
                                                       Multi-store + Captive portal
```

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Lines per ViewModel (network/state) | < 10 (from ~150) |
| Decision logic duplication | 0 (centralized in DecisionEngine) |
| NetworkMonitor observation boilerplate | 0 (fused + auto-reconnect) |
| Pull-to-refresh flicker | 0 (lastContent preserves display) |
| WiFi↔Cell handoff flicker | 0 (debounced 300ms) |
| Captive portal detection | ✅ (distinct UI state) |
| External connectivity deps | 1 (cmp-network-monitor, down from 3 jordond libs) |
| Filter reactivity | Immediate (combineContent) |
| Unit test coverage (DecisionEngine) | 100% of matrix (17 cases) |
| Breaking changes to consumers | 0 (typealias backward compat) |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| `cmp-network-monitor` not published to Maven Central yet | lib-integrate composite build handles local source; Maven fallback when published |
| `lastContent` holding stale ref after Store invalidation | `flatMapLatest` resets per-stream; Store TTL handles cache expiry |
| `drop(1)` on debounced reconnect might miss | Only drops initial emission; first load via `onStart` handles startup |
| `combineContent` + `emptyIfContent` ordering matters | Document: always `emptyIfContent` AFTER content transforms |
| 300ms debounce delays legitimate reconnect | Acceptable tradeoff — 300ms delay vs multiple flickers |
| `null as Output` in no-fallback mapper | Safe: guarded by `isEmpty=true` — data never accessed |
| `core-base/ui` now depends on `core-base/store` | Only composable files — types-only dependency, no heavy transitives |

---

## Phase 7: Demo Feature — Fintech Dashboard (E2E Proof)

Implements a complete fintech feature module in `kmp-project-template` exercising every ScreenState variant, proving the pipeline works end-to-end before syncing to consumer projects.

### APIs (Free, No Auth)

| API | Base URL | Purpose |
|-----|----------|---------|
| **Frankfurter** | `https://api.frankfurter.dev/v1/` | Currency exchange rates (30 currencies, ECB data) |
| **CoinGecko** | `https://api.coingecko.com/api/v3/` | Crypto market data (paginated, real-time prices) |

### API Contracts

#### Frankfurter — Exchange Rates

```
GET /v1/latest?from=USD
Response:
{
  "amount": 1.0,
  "base": "USD",
  "date": "2026-04-30",
  "rates": { "EUR": 0.85, "GBP": 0.74, "INR": 94.92, "JPY": 156.56, ... }  // 29 currencies
}

GET /v1/currencies
Response:
{ "AUD": "Australian Dollar", "EUR": "Euro", "GBP": "British Pound", ... }  // 30 entries

GET /v1/2026-01-01..2026-04-30?from=USD&to=INR
Response:
{
  "amount": 1.0,
  "base": "USD",
  "start_date": "2026-01-01",
  "end_date": "2026-04-30",
  "rates": { "2026-01-02": { "INR": 85.12 }, "2026-01-03": { "INR": 85.30 }, ... }
}
```

#### CoinGecko — Crypto Market

```
GET /v3/coins/markets?vs_currency=usd&per_page=20&page=1&order=market_cap_desc
Response: [
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "image": "https://coin-images.coingecko.com/.../bitcoin.png",
    "current_price": 78236,
    "market_cap": 1566577948727,
    "market_cap_rank": 1,
    "price_change_percentage_24h": 1.60,
    "high_24h": 78773,
    "low_24h": 77003,
    "total_volume": 34708022335,
    "circulating_supply": 20023521.0,
    "max_supply": 21000000.0,
    "last_updated": "2026-05-02T07:41:42.327Z"
  },
  ...
]

GET /v3/coins/{id}
Response: { "id": "bitcoin", "name": "Bitcoin", "description": {...}, "market_data": {...}, ... }

GET /v3/coins/{id}/market_chart?vs_currency=usd&days=30
Response: { "prices": [[timestamp, price], ...], "market_caps": [...], "total_volumes": [...] }
```

### Feature Module: `feature/fintech-demo`

#### Screens & ScreenState Coverage

| Screen | API | Store Type | ScreenState Exercised |
|--------|-----|-----------|----------------------|
| **Currency Rates** | frankfurter `/latest` | `Store<String, ExchangeRates>` | Loading → Content(FRESH) → Content(STALE) → Content(UPDATING) |
| **Rate History** | frankfurter historical | `Store<RateHistoryKey, RateHistory>` (dynamic key) | Loading → Content + keyFlow variant |
| **Crypto Watchlist** | coingecko `/markets` | `Store<PageKey, List<CoinMarket>>` | Loading → PagingScreenStream → loadMore → Empty (search) |
| **Coin Detail** | coingecko `/coins/{id}` | `Store<String, CoinDetail>` | Loading → Content → Error (rate limited) |
| **EMI Calculator** | Local computation | None (pure UI state) | N/A — proves non-Store screens coexist |
| **Offline Mode** | All | All | NoNetwork → Content(STALE) → auto-reconnect |

#### Module Structure

```
feature/fintech-demo/
├── src/commonMain/kotlin/org/mifos/feature/fintechdemo/
│   ├── di/
│   │   └── FintechDemoModule.kt              // Koin: stores + ViewModels
│   ├── data/
│   │   ├── api/
│   │   │   ├── FrankfurterApi.kt             // Ktorfit service
│   │   │   └── CoinGeckoApi.kt              // Ktorfit service
│   │   ├── model/
│   │   │   ├── ExchangeRatesDto.kt          // API response DTOs
│   │   │   ├── CoinMarketDto.kt
│   │   │   ├── CoinDetailDto.kt
│   │   │   └── RateHistoryDto.kt
│   │   ├── store/
│   │   │   ├── ExchangeRatesStore.kt        // Store<String, ExchangeRates> (base currency key)
│   │   │   ├── RateHistoryStore.kt          // Store<RateHistoryKey, RateHistory>
│   │   │   ├── CoinMarketsStore.kt          // Store<PageKey, List<CoinMarket>> (paging)
│   │   │   └── CoinDetailStore.kt           // Store<String, CoinDetail> (coin id key)
│   │   └── db/
│   │       ├── ExchangeRatesEntity.kt       // Room entity (SOT for cache)
│   │       ├── CoinMarketEntity.kt
│   │       └── FintechDemoDao.kt
│   ├── domain/
│   │   ├── model/
│   │   │   ├── ExchangeRates.kt             // Domain model
│   │   │   ├── CoinMarket.kt
│   │   │   ├── CoinDetail.kt
│   │   │   ├── RateHistory.kt
│   │   │   └── EmiResult.kt                 // EMI calculation result
│   │   └── usecase/
│   │       └── CalculateEmiUseCase.kt        // Pure computation
│   ├── ui/
│   │   ├── rates/
│   │   │   ├── CurrencyRatesViewModel.kt    // asScreenStream() demo
│   │   │   └── CurrencyRatesScreen.kt       // ScreenContent + pull-to-refresh
│   │   ├── history/
│   │   │   ├── RateHistoryViewModel.kt      // asScreenStream(keyFlow) demo
│   │   │   └── RateHistoryScreen.kt         // Line chart + currency picker
│   │   ├── crypto/
│   │   │   ├── CryptoWatchlistViewModel.kt  // asPagingScreenStream() demo
│   │   │   ├── CryptoWatchlistScreen.kt     // Infinite scroll + ScreenContent
│   │   │   ├── CoinDetailViewModel.kt       // Single-item stream demo
│   │   │   └── CoinDetailScreen.kt
│   │   ├── emi/
│   │   │   ├── EmiCalculatorViewModel.kt    // Pure local state (no Store)
│   │   │   └── EmiCalculatorScreen.kt       // Sliders + result display
│   │   └── dashboard/
│   │       ├── FintechDashboardViewModel.kt  // Multi-store combine pattern
│   │       └── FintechDashboardScreen.kt     // Combined rates + top coins
│   └── navigation/
│       └── FintechDemoNavigation.kt          // Nav graph
└── src/commonTest/kotlin/org/mifos/feature/fintechdemo/
    ├── CurrencyRatesViewModelTest.kt         // Verifies ScreenState transitions
    ├── CryptoWatchlistViewModelTest.kt       // Verifies paging behavior
    └── EmiCalculatorTest.kt                  // Pure logic test
```

#### ViewModel Examples (Proving the Pattern)

**1. Currency Rates — `asScreenStream()` (simplest case)**

```kotlin
class CurrencyRatesViewModel(
    private val exchangeRatesStore: Store<String, ExchangeRates>,
    private val networkMonitor: NetworkMonitor,
) : BaseViewModel<RatesLocalState, RatesEvent, RatesAction>(RatesLocalState()) {

    private val stream = exchangeRatesStore.asScreenStream(
        key = "USD",
        networkMonitor = networkMonitor,
        scope = viewModelScope,
    )

    val screenState: StateFlow<ScreenState<RatesDisplay>> = stream.state
        .combineContent(stateFlow) { rates, local, _ ->
            RatesDisplay(
                base = rates.base,
                date = rates.date,
                rates = rates.rates.filter { local.searchQuery.isEmpty() || it.key.contains(local.searchQuery, true) },
                favoriteRates = rates.rates.filter { it.key in local.favorites },
            )
        }
        .emptyIfContent { it.rates.isEmpty() }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), ScreenState.Loading)

    fun onRetry() = stream.retry()
    fun onRefresh() = stream.refresh()

    override fun handleAction(action: RatesAction) = when (action) {
        is RatesAction.Search -> updateState { copy(searchQuery = action.query) }
        is RatesAction.ToggleFavorite -> updateState {
            copy(favorites = if (action.code in favorites) favorites - action.code else favorites + action.code)
        }
    }
}

data class RatesLocalState(val searchQuery: String = "", val favorites: Set<String> = emptySet())
data class RatesDisplay(val base: String, val date: String, val rates: Map<String, Double>, val favoriteRates: Map<String, Double>)
```

**2. Crypto Watchlist — `asPagingScreenStream()` (infinite scroll)**

```kotlin
class CryptoWatchlistViewModel(
    private val coinMarketsStore: Store<PageKey, List<CoinMarket>>,
    private val networkMonitor: NetworkMonitor,
) : BaseViewModel<Unit, CryptoEvent, CryptoAction>(Unit) {

    private val pagingStream = coinMarketsStore.asPagingScreenStream(
        networkMonitor = networkMonitor,
        scope = viewModelScope,
        pageSize = 20,
    )

    val screenState = pagingStream.state
    val hasMore = pagingStream.hasMore
    val isLoadingMore = pagingStream.isLoadingMore

    fun onLoadMore() = pagingStream.loadNextPage()
    fun onRetry() = pagingStream.retry()
    fun onRefresh() = pagingStream.refresh()
}
```

**3. Rate History — `asScreenStream(keyFlow)` (dynamic key)**

```kotlin
class RateHistoryViewModel(
    private val rateHistoryStore: Store<RateHistoryKey, RateHistory>,
    private val networkMonitor: NetworkMonitor,
) : BaseViewModel<HistoryLocalState, HistoryEvent, HistoryAction>(HistoryLocalState()) {

    private val keyFlow: Flow<RateHistoryKey> = stateFlow.map { local ->
        RateHistoryKey(from = "USD", to = local.targetCurrency, days = local.periodDays)
    }.distinctUntilChanged()

    private val stream = rateHistoryStore.asScreenStream(
        keyFlow = keyFlow,
        networkMonitor = networkMonitor,
        scope = viewModelScope,
    )

    val screenState: StateFlow<ScreenState<RateHistory>> = stream.state
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), ScreenState.Loading)

    fun onRetry() = stream.retry()

    override fun handleAction(action: HistoryAction) = when (action) {
        is HistoryAction.SelectCurrency -> updateState { copy(targetCurrency = action.code) }
        is HistoryAction.SelectPeriod -> updateState { copy(periodDays = action.days) }
    }
}

data class HistoryLocalState(val targetCurrency: String = "INR", val periodDays: Int = 30)
```

**4. Dashboard — Multi-store combine**

```kotlin
class FintechDashboardViewModel(
    private val exchangeRatesStore: Store<String, ExchangeRates>,
    private val coinMarketsStore: Store<PageKey, List<CoinMarket>>,
    private val networkMonitor: NetworkMonitor,
) : BaseViewModel<Unit, DashboardEvent, DashboardAction>(Unit) {

    private val ratesStream = exchangeRatesStore.asScreenStream("USD", networkMonitor, viewModelScope)
    private val coinsStream = coinMarketsStore.asScreenStream(PageKey.first(5), networkMonitor, viewModelScope)

    val screenState: StateFlow<ScreenState<DashboardData>> = combine(
        ratesStream.state,
        coinsStream.state,
    ) { rates, coins ->
        when {
            rates is ScreenState.Loading || coins is ScreenState.Loading -> ScreenState.Loading
            rates is ScreenState.NoNetwork -> rates
            rates is ScreenState.Content && coins is ScreenState.Content -> {
                val freshness = maxOf(rates.freshness, coins.freshness)
                ScreenState.Content(DashboardData(rates.data, coins.data), freshness)
            }
            rates is ScreenState.Error -> rates
            coins is ScreenState.Error -> coins
            else -> ScreenState.Loading
        }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), ScreenState.Loading)

    fun onRetry() { ratesStream.retry(); coinsStream.retry() }
}

data class DashboardData(val rates: ExchangeRates, val topCoins: List<CoinMarket>)
```

**5. EMI Calculator — Pure local (proves non-Store coexistence)**

```kotlin
class EmiCalculatorViewModel : BaseViewModel<EmiState, Nothing, EmiAction>(EmiState()) {

    val emiResult: StateFlow<EmiResult?> = stateFlow.map { state ->
        if (state.principal > 0 && state.ratePercent > 0 && state.tenureMonths > 0) {
            CalculateEmiUseCase(state.principal, state.ratePercent, state.tenureMonths)
        } else null
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)

    override fun handleAction(action: EmiAction) = when (action) {
        is EmiAction.UpdatePrincipal -> updateState { copy(principal = action.value) }
        is EmiAction.UpdateRate -> updateState { copy(ratePercent = action.value) }
        is EmiAction.UpdateTenure -> updateState { copy(tenureMonths = action.value) }
    }
}

data class EmiState(val principal: Double = 100000.0, val ratePercent: Double = 8.5, val tenureMonths: Int = 12)
data class EmiResult(val emi: Double, val totalPayment: Double, val totalInterest: Double)
```

### Store Examples (with Fetcher retry)

```kotlin
// ExchangeRatesStore — Network + Room cache
fun provideExchangeRatesStore(
    api: FrankfurterApi,
    dao: FintechDemoDao,
    networkMonitor: NetworkMonitor,
): Store<String, ExchangeRates> = StoreFactory.createStore(
    fetcher = Fetcher.of { baseCurrency: String ->
        networkMonitor.executeWithRetry(RetryPolicy { maxAttempts = 3 }) {
            api.getLatestRates(from = baseCurrency).toDomain()
        }
    },
    sourceOfTruth = SourceOfTruth.of(
        reader = { base -> dao.observeRates(base).map { it?.toDomain() } },
        writer = { base, rates -> dao.upsertRates(rates.toEntity(base)) },
        delete = { base -> dao.deleteRates(base) },
        deleteAll = { dao.deleteAllRates() },
    ),
    validator = DefaultValidator.withTtl(5.minutes),
)
```

### E2E ScreenState Coverage Matrix

| Scenario | How to Trigger | Expected State |
|----------|---------------|----------------|
| Fresh load | Open Currency Rates | `Loading` → `Content(FRESH)` |
| Cached + online | Reopen after 1 min | `Content(FRESH)` (TTL not expired) |
| Cached + offline | Toggle airplane mode | `Content(STALE)` + banner |
| No cache + offline | Clear data + airplane | `NoNetwork` + retry button |
| Pull to refresh | Swipe down | `Content(UPDATING)` + progress |
| Auto reconnect | Turn WiFi back on | `Content(STALE)` → auto → `Content(FRESH)` |
| Captive portal | Connect to hotel WiFi | `NoNetwork(captive=true)` + "Sign in" |
| Error (rate limited) | Hit CoinGecko 50+/min | `Error` + retry button |
| Error with cache | Rate limited after cache | `Content(STALE)` (preserves data) |
| Empty search | Type "ZZZZZ" in rates | `Empty` |
| Paging | Scroll crypto list | Page 1 → loadMore → Page 2 appended |
| Paging offline | Scroll + airplane | `Content(STALE)` with loaded pages |
| Dynamic key | Switch INR→EUR in history | `Loading` → `Content(FRESH)` (new key) |

### Navigation Graph

```kotlin
// feature/fintech-demo navigation
fun NavGraphBuilder.fintechDemoNavGraph(navController: NavController) {
    navigation(startDestination = "fintech_dashboard", route = "fintech_demo") {
        composable("fintech_dashboard") { FintechDashboardScreen(navController) }
        composable("currency_rates") { CurrencyRatesScreen(navController) }
        composable("rate_history/{currency}") { RateHistoryScreen(navController) }
        composable("crypto_watchlist") { CryptoWatchlistScreen(navController) }
        composable("coin_detail/{coinId}") { CoinDetailScreen(navController) }
        composable("emi_calculator") { EmiCalculatorScreen(navController) }
    }
}
```

---

## Updated Execution Order (Full)

```
Phase 0 (migration)      → Phase 1 (types)           → Phase 2 (stream)
     │                         │                            │
  Remove jordond/            ScreenState                 ScreenDataStream
  Wire cmp-network-monitor   DecisionEngine              streamDataNoFallback
  Update 2 consumers         Extensions                  asScreenStream()
                                                              │
Phase 3 (paging)         → Phase 4 (UI)              → Phase 5 (tests)
     │                         │                            │
  PagingScreenStream       ScreenContent               DecisionEngineTest
  (NetworkStatus-aware)    FreshnessIndicator          StreamTest
                           ConnectivityBanner           ExtensionsTest
                                                            │
Phase 6 (docs)           → Phase 7 (demo feature)
     │                         │
  Patterns guide            feature/fintech-demo
  Migration guide           Frankfurter + CoinGecko APIs
                            5 screens × all ScreenState variants
                            Store + Room + Fetcher retry
                            EMI local computation
                            E2E proof before consumer sync
```

---

## Updated File Manifest (Phase 7 additions)

| # | Path | Type |
|---|------|------|
| 24 | `feature/fintech-demo/build.gradle.kts` | New |
| 25 | `feature/fintech-demo/.../di/FintechDemoModule.kt` | New |
| 26 | `feature/fintech-demo/.../data/api/FrankfurterApi.kt` | New |
| 27 | `feature/fintech-demo/.../data/api/CoinGeckoApi.kt` | New |
| 28 | `feature/fintech-demo/.../data/model/*.kt` (4 DTOs) | New |
| 29 | `feature/fintech-demo/.../data/store/*.kt` (4 stores) | New |
| 30 | `feature/fintech-demo/.../data/db/*.kt` (3 files) | New |
| 31 | `feature/fintech-demo/.../domain/model/*.kt` (5 models) | New |
| 32 | `feature/fintech-demo/.../domain/usecase/CalculateEmiUseCase.kt` | New |
| 33 | `feature/fintech-demo/.../ui/rates/*.kt` (2 files) | New |
| 34 | `feature/fintech-demo/.../ui/history/*.kt` (2 files) | New |
| 35 | `feature/fintech-demo/.../ui/crypto/*.kt` (4 files) | New |
| 36 | `feature/fintech-demo/.../ui/emi/*.kt` (2 files) | New |
| 37 | `feature/fintech-demo/.../ui/dashboard/*.kt` (2 files) | New |
| 38 | `feature/fintech-demo/.../navigation/FintechDemoNavigation.kt` | New |
| 39 | `feature/fintech-demo/src/commonTest/*.kt` (3 test files) | New |
| 40 | `settings.gradle.kts` | Modified (include `:feature:fintech-demo`) |
| 41 | `gradle/libs.versions.toml` | Modified (add cmp-network-monitor-compose entry) |

**Total: 41 files** (17 new in Phase 7, 23 from Phases 0-6, 1 settings update)
