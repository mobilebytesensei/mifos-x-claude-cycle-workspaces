# PLAN-storedata-api-260430: StoreData<T> — Unified Store API with Source Selection & Paging

| Field | Value |
|-------|-------|
| ID | storedata-api-260430 |
| Status | Draft (v4 — BLOCKER fixed: loadPage, fresh API; + code documentation) |
| Priority | P1 |
| Scope | `core-base/store` module — 5 new files + tests (commonTest) |
| Created | 2026-04-30 |
| Prerequisites | core-base/store module exists (StoreFactory, StoreResponseMapper, DefaultValidator, InMemoryBookkeeper) |
| Effort | ~4-5 hours |
| Parent Plan | PLAN-store-offline-260429 (Phase 3 extension) |

---

## Problem Statement

Feature modules consuming Store-backed repositories need:

1. **Data origin visibility** — cache (Room), network (API), or in-memory
2. **Refresh status** — show subtle loading while serving cached data
3. **Staleness awareness** — age since last fetch, TTL remaining
4. **Error recovery** — show "couldn't refresh" while keeping cached data visible
5. **Source mode selection** — same API whether repository uses Network+DB or Network-only
6. **Paging support** — Room PagingSource integration via Store for large lists
7. **Complete status handling** — loading, success, empty, error, no-network for all modes

### Architecture Clarification (from audit)

```
Feature ViewModel
    │
    ├── calls core/data Repository directly (normal case)
    │
    └── calls core/domain UseCase (ONLY when transformation needed — e.g., paging, combining repos)

core/data Repository
    │
    └── uses Store (via core-base/store abstractions)
            │
            ├── Mode: NETWORK_AND_CACHE — Fetcher + SourceOfTruth (Room)
            │       emits: Loading → Data(Cache) → Data(Network)
            │
            └── Mode: NETWORK_ONLY — Fetcher only (no SOT)
                    emits: Loading → Data(Network) or Error
```

**Key user decisions:**
- `core/domain` is ONLY used when response transformation is needed (paging, combining multiple repos)
- ViewModels call `core/data` repositories directly for simple data
- Same `StoreData<T>` API regardless of source mode — ViewModel doesn't know/care

### Store 5 API (verified from 5.1.0-alpha08 bytecode)

**`StoreReadResponseOrigin`** — standalone top-level sealed class:
- `StoreReadResponseOrigin.Fetcher` — data class with optional `name: String?`
- `StoreReadResponseOrigin.SourceOfTruth` — object
- `StoreReadResponseOrigin.Cache` — object
- `StoreReadResponseOrigin.Initial` — object

**`StoreReadResponse`** — sealed class with `origin: StoreReadResponseOrigin`:
- `StoreReadResponse.Initial` — initial state (no data yet)
- `StoreReadResponse.Loading(origin)`
- `StoreReadResponse.Data(value, origin)`
- `StoreReadResponse.NoNewData(origin)`
- `StoreReadResponse.Error` (sealed): `.Exception(error, origin)`, `.Message(message, origin)`, `.Custom(error, origin)`

**Network-only Store emissions** (no SourceOfTruth):
- `Loading(Fetcher)` → `Data(Fetcher)` on success
- `Loading(Fetcher)` → `Error.*` on failure
- NO `SourceOfTruth` origin emissions — only `Fetcher` and `Cache` (in-memory)

**`StoreReadRequest` variants** (bytecode-verified):
- `cached(key, refresh)` — serve cache, optionally refresh
- `fresh(key, fallBackToSourceOfTruth)` — force network fetch
- `localOnly(key)` — cache/SOT only, no network
- `skipMemory(key, refresh)` — bypass in-memory cache

---

## Solution

### Part 1: `StoreData<T>` — Unified response type

A single data class that carries data + metadata. Works identically for both source modes.

### Part 2: `SourceMode` — Source selection

Repositories declare their source mode. The mapper handles differences internally.

### Part 3: `StorePagingSource<Key, Value>` — Room Paging integration

A PagingSource adapter in `core/domain` that wraps Store for paginated lists.

---

## Design Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | `StoreData` is a data class, not sealed | All emissions carry data — loading-without-data uses `DataState.Loading` before Store stream starts |
| D2 | Lives in `core-base/store` (synced) | Consumer apps get it via sync-dirs.sh |
| D3 | Uses `kotlin.time` not `kotlinx-datetime` | Avoids adding dependency (same as DefaultValidator) |
| D4 | `fetchedAt` is `TimeMark?` not `Long` | Monotonic time avoids clock skew, consistent with DefaultValidator |
| D5 | Coexists with `DataState<T>` | DataState for simple cases (datastore, one-shot). StoreData for Store-backed repos |
| D6 | `mapToStoreData()` uses `transform` | Track `isRefreshing` state across emissions, skip Loading |
| D7 | `StoreReadResponseOrigin` is top-level, not nested | Store 5 API fact. Import: `o.m.store.store5.StoreReadResponseOrigin` |
| D8 | Handle `StoreReadResponse.Initial` as no-op | Initial emitted before data — treat like Loading |
| D9 | `toDataState()` bridge extension | Convenience for VMs migrating from DataState |
| D10 | Tests in `commonTest` | build.gradle.kts declares commonTest.dependencies |
| D11 | MPL 2.0 license header on all files | Match existing core-base/store files |
| D12 | **Network-only mode: `isStale` always false** | No cache means no staleness concept — data is always fresh or error |
| D13 | **Network-only mode: `origin` always NETWORK** | Simplifies ViewModel logic — no cache/SOT origins possible |
| D14 | **Empty detection via `isEmpty` lambda** | StoreData carries `isEmpty` flag for empty list/null distinction |
| D15 | **Paging in core/domain, not core/data** | Paging adds transformation complexity — fits domain layer role. core/data stays clean. |
| D16 | **Paging deps optional** | `androidx.paging` added to libs.versions.toml but consumer apps opt-in |
| D17 | **Domain layer = transformation only** | ViewModels call repos directly. Use cases only when combining/paging/transforming |

---

## Files to Create

### 1. `StoreData.kt` — Data class + DataOrigin + empty/status helpers

**Path:** `core-base/store/src/commonMain/kotlin/template/core/base/store/StoreData.kt`

```kotlin
/*
 * Copyright 2025 Mifos Initiative
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * See https://github.com/openMF/kmp-project-template/blob/main/LICENSE
 */
package template.core.base.store

import template.core.base.common.DataState
import kotlin.time.Duration
import kotlin.time.TimeSource

/**
 * Wraps data with metadata about its origin, freshness, and refresh state.
 *
 * Works identically for both source modes:
 * - **Network + Cache**: emits cached data first (fast), then network data (updated)
 * - **Network only**: emits network data directly, no cache/staleness
 *
 * Feature modules collect `Flow<StoreData<T>>` from repositories and render
 * cache-then-refresh UX patterns without knowing the source mode.
 *
 * @param T The domain data type.
 * @param data The actual data payload.
 * @param origin Where this data emission came from.
 * @param isRefreshing True when a network fetch is in progress (cached data is being shown).
 * @param fetchedAt Monotonic time mark of the last successful network fetch, or null if never fetched.
 * @param error Non-null if the most recent refresh attempt failed. Data may still be valid (stale).
 * @param isEmpty True if the data represents an empty result (e.g., empty list, null-equivalent).
 */
data class StoreData<out T>(
    val data: T,
    val origin: DataOrigin,
    val isRefreshing: Boolean = false,
    val fetchedAt: TimeSource.Monotonic.ValueTimeMark? = null,
    val error: Throwable? = null,
    val isEmpty: Boolean = false,
) {
    /** True if data has never been fetched from network (only meaningful for cached stores). */
    val isStale: Boolean get() = fetchedAt == null && origin != DataOrigin.NETWORK

    /** Duration since last successful network fetch, or null if never fetched. */
    val staleDuration: Duration? get() = fetchedAt?.elapsedNow()

    /** True if this emission has data and no error. */
    val isSuccess: Boolean get() = error == null && !isEmpty

    /** True if this is a terminal error with no usable data. */
    val isError: Boolean get() = error != null && isEmpty
}

/**
 * Indicates where a [StoreData] emission originated.
 */
enum class DataOrigin {
    /** Data was read from local persistence (Room database). */
    CACHE,

    /** Data was freshly fetched from the network (API). */
    NETWORK,

    /** Data was served from Store's in-memory cache. */
    MEMORY,
}

/**
 * Converts [StoreData] to [DataState] for ViewModels using DataState patterns.
 *
 * Mapping:
 * - [isEmpty] + no error → [DataState.Loading] (no data yet)
 * - [isRefreshing] + data → [DataState.Pending] (cached data, refresh in progress)
 * - [error] != null → [DataState.Error] (with optional stale data)
 * - data present, no error → [DataState.Success]
 */
fun <T> StoreData<T>.toDataState(): DataState<T> {
    return when {
        isEmpty && error == null -> DataState.Loading
        error != null -> DataState.Error(error, if (isEmpty) null else data)
        isRefreshing -> DataState.Pending(data)
        else -> DataState.Success(data)
    }
}
```

### 2. `StoreDataMapper.kt` — Unified mapper for both source modes

**Path:** `core-base/store/src/commonMain/kotlin/template/core/base/store/StoreDataMapper.kt`

```kotlin
/*
 * Copyright 2025 Mifos Initiative
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * See https://github.com/openMF/kmp-project-template/blob/main/LICENSE
 */
package template.core.base.store

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.transform
import org.mobilenativefoundation.store.store5.StoreReadResponse
import org.mobilenativefoundation.store.store5.StoreReadResponseOrigin
import kotlin.time.TimeSource

/**
 * Maps a [StoreReadResponse] flow into `Flow<StoreData<Output>>`.
 *
 * Works for both source modes:
 * - **Network + Cache store**: Loading → Data(Cache, refreshing) → Data(Network)
 * - **Network-only store**: Loading → Data(Network) or Error
 *
 * @param isEmpty Optional predicate to detect empty results (e.g., `{ it.isEmpty() }` for lists).
 *   Defaults to false (all data is non-empty).
 */
fun <Output : Any> Flow<StoreReadResponse<Output>>.mapToStoreData(
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    var refreshing = false
    var lastFetchMark: TimeSource.Monotonic.ValueTimeMark? = null

    return transform { response ->
        when (response) {
            is StoreReadResponse.Initial,
            is StoreReadResponse.Loading,
            -> {
                refreshing = true
            }

            is StoreReadResponse.Data -> {
                val origin = response.origin.toDataOrigin()
                if (origin == DataOrigin.NETWORK) {
                    lastFetchMark = TimeSource.Monotonic.markNow()
                    refreshing = false
                }
                emit(
                    StoreData(
                        data = response.value,
                        origin = origin,
                        isRefreshing = refreshing && origin != DataOrigin.NETWORK,
                        fetchedAt = lastFetchMark,
                        isEmpty = isEmpty(response.value),
                    ),
                )
            }

            is StoreReadResponse.NoNewData -> {
                refreshing = false
            }

            is StoreReadResponse.Error -> {
                refreshing = false
            }
        }
    }
}

/**
 * Like [mapToStoreData] but also emits on errors, carrying the last known data.
 *
 * Handles all status scenarios:
 * - **Success**: Data arrives → emit with origin and staleness
 * - **Empty**: Data arrives but isEmpty predicate is true → emit with isEmpty=true
 * - **Error with stale data**: Error after cache → emit error with last known data
 * - **Error without data**: Error before any data → emit error with fallback (isEmpty=true)
 * - **No network**: Error type hints at connectivity → ViewModel can check error type
 *
 * @param fallback Value to use if an error arrives before any data.
 * @param isEmpty Predicate to detect empty results.
 */
fun <Output : Any> Flow<StoreReadResponse<Output>>.mapToStoreDataWithErrors(
    fallback: Output,
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    var refreshing = false
    var lastFetchMark: TimeSource.Monotonic.ValueTimeMark? = null
    var lastData: Output = fallback
    var hasReceivedData = false

    return transform { response ->
        when (response) {
            is StoreReadResponse.Initial,
            is StoreReadResponse.Loading,
            -> {
                refreshing = true
            }

            is StoreReadResponse.Data -> {
                val origin = response.origin.toDataOrigin()
                if (origin == DataOrigin.NETWORK) {
                    lastFetchMark = TimeSource.Monotonic.markNow()
                    refreshing = false
                }
                lastData = response.value
                hasReceivedData = true
                emit(
                    StoreData(
                        data = response.value,
                        origin = origin,
                        isRefreshing = refreshing && origin != DataOrigin.NETWORK,
                        fetchedAt = lastFetchMark,
                        isEmpty = isEmpty(response.value),
                    ),
                )
            }

            is StoreReadResponse.NoNewData -> {
                refreshing = false
            }

            is StoreReadResponse.Error -> {
                refreshing = false
                val error = response.toThrowable()
                emit(
                    StoreData(
                        data = lastData,
                        origin = if (hasReceivedData) DataOrigin.CACHE else DataOrigin.NETWORK,
                        isRefreshing = false,
                        fetchedAt = lastFetchMark,
                        error = error,
                        isEmpty = !hasReceivedData,
                    ),
                )
            }
        }
    }
}

/**
 * Maps [StoreReadResponseOrigin] to [DataOrigin].
 *
 * [StoreReadResponseOrigin] is a top-level sealed class (NOT nested in StoreReadResponse).
 * [StoreReadResponseOrigin.Fetcher] is a data class with optional `name: String?`,
 * while SourceOfTruth, Cache, and Initial are singleton objects.
 */
internal fun StoreReadResponseOrigin.toDataOrigin(): DataOrigin {
    return when (this) {
        is StoreReadResponseOrigin.Fetcher -> DataOrigin.NETWORK
        StoreReadResponseOrigin.SourceOfTruth -> DataOrigin.CACHE
        StoreReadResponseOrigin.Cache -> DataOrigin.MEMORY
        StoreReadResponseOrigin.Initial -> DataOrigin.MEMORY
    }
}

/**
 * Extracts a [Throwable] from any [StoreReadResponse.Error] variant.
 */
internal fun StoreReadResponse.Error.toThrowable(): Throwable {
    return when (this) {
        is StoreReadResponse.Error.Exception -> error
        is StoreReadResponse.Error.Message -> RuntimeException(message)
        is StoreReadResponse.Error.Custom<*> -> RuntimeException("Store error: $error")
    }
}
```

### 3. `StoreDataExtensions.kt` — Convenience extensions for common patterns

**Path:** `core-base/store/src/commonMain/kotlin/template/core/base/store/StoreDataExtensions.kt`

```kotlin
/*
 * Copyright 2025 Mifos Initiative
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * See https://github.com/openMF/kmp-project-template/blob/main/LICENSE
 */
package template.core.base.store

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import org.mobilenativefoundation.store.store5.Store
import org.mobilenativefoundation.store.store5.StoreReadRequest
import org.mobilenativefoundation.store.store5.StoreReadResponse

/**
 * Streams data from a [Store] with full [StoreData] metadata.
 *
 * This is the primary API for repositories. Source mode (network+cache vs network-only)
 * is determined by how the Store was created:
 * - [StoreFactory.createStore] → network + cache (Fetcher + SourceOfTruth)
 * - [StoreFactory.createMemoryStore] → network only (Fetcher only, in-memory cache)
 *
 * Both produce the same `Flow<StoreData<Output>>` — the ViewModel doesn't need to know.
 *
 * @param key The data identifier.
 * @param refresh Whether to trigger a network refresh. Default true.
 * @param isEmpty Predicate to detect empty results.
 */
fun <Key : Any, Output : Any> Store<Key, Output>.streamData(
    key: Key,
    refresh: Boolean = true,
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    return stream(StoreReadRequest.cached(key, refresh))
        .mapToStoreData(isEmpty)
}

/**
 * Like [streamData] but also emits on errors with last known data preserved.
 *
 * @param key The data identifier.
 * @param fallback Value to use if error arrives before any data.
 * @param refresh Whether to trigger a network refresh. Default true.
 * @param isEmpty Predicate to detect empty results.
 */
fun <Key : Any, Output : Any> Store<Key, Output>.streamDataWithErrors(
    key: Key,
    fallback: Output,
    refresh: Boolean = true,
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    return stream(StoreReadRequest.cached(key, refresh))
        .mapToStoreDataWithErrors(fallback, isEmpty)
}

/**
 * Forces a fresh network fetch, ignoring any cached data.
 * Useful for pull-to-refresh or explicit "reload" actions.
 */
fun <Key : Any, Output : Any> Store<Key, Output>.freshData(
    key: Key,
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    return stream(StoreReadRequest.fresh(key, fallBackToSourceOfTruth = true))
        .mapToStoreData(isEmpty)
}

/**
 * Reads only from local cache/database, no network.
 * Useful for offline-only screens or pre-fetched data.
 */
fun <Key : Any, Output : Any> Store<Key, Output>.localData(
    key: Key,
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    return stream(StoreReadRequest.localOnly(key))
        .mapToStoreData(isEmpty)
}

/**
 * Maps [StoreData] content while preserving all metadata.
 */
fun <T, R> StoreData<T>.map(transform: (T) -> R): StoreData<R> {
    return StoreData(
        data = transform(data),
        origin = origin,
        isRefreshing = isRefreshing,
        fetchedAt = fetchedAt,
        error = error,
        isEmpty = isEmpty,
    )
}

/**
 * Maps a Flow of [StoreData] content while preserving all metadata.
 */
fun <T, R> Flow<StoreData<T>>.mapData(transform: (T) -> R): Flow<StoreData<R>> {
    return map { it.map(transform) }
}
```

### 4. `StorePagingSource.kt` — Room Paging + Store integration (in core-base/store)

**Path:** `core-base/store/src/commonMain/kotlin/template/core/base/store/StorePagingSource.kt`

> **Note:** This file provides the pattern/interface. The actual `androidx.paging` dependency
> is optional — consumer apps that need paging add it. The base module provides the key pattern.

```kotlin
/*
 * Copyright 2025 Mifos Initiative
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * See https://github.com/openMF/kmp-project-template/blob/main/LICENSE
 */
package template.core.base.store

import kotlinx.coroutines.flow.filterNot
import kotlinx.coroutines.flow.first
import org.mobilenativefoundation.store.store5.Store
import org.mobilenativefoundation.store.store5.StoreReadRequest
import org.mobilenativefoundation.store.store5.StoreReadResponse

/**
 * Key for paginated Store requests.
 *
 * Use this as the Store key type when the data source supports pagination.
 * The Store will cache each page independently.
 *
 * @param page Zero-based page index.
 * @param pageSize Number of items per page.
 * @param query Optional search/filter query.
 */
data class PageKey(
    val page: Int,
    val pageSize: Int = DEFAULT_PAGE_SIZE,
    val query: String? = null,
) {
    companion object {
        const val DEFAULT_PAGE_SIZE = 20

        /** First page with default size. */
        fun first(pageSize: Int = DEFAULT_PAGE_SIZE, query: String? = null): PageKey =
            PageKey(page = 0, pageSize = pageSize, query = query)
    }

    /** Next page key. */
    fun next(): PageKey = copy(page = page + 1)

    /** Offset for SQL LIMIT/OFFSET queries. */
    val offset: Int get() = page * pageSize
}

/**
 * Triggers a Store refresh for a specific page and suspends until data arrives.
 *
 * Use this inside a PagingSource.load() implementation to let Store handle
 * caching while Paging handles the pagination UX.
 *
 * Usage in core/domain (where paging transformation lives):
 * ```
 * class ClientPagingSource(
 *     private val store: Store<PageKey, List<Client>>,
 * ) : PagingSource<Int, Client>() {
 *
 *     override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Client> {
 *         val page = params.key ?: 0
 *         val pageKey = PageKey(page = page, pageSize = params.loadSize)
 *         return store.loadPage(pageKey)
 *     }
 * }
 * ```
 *
 * **Important:** Store's `stream()` returns an infinite Flow (never completes).
 * This function uses `filterNot` + `first` to get the first Data or Error emission
 * and then cancel the flow. Do NOT use `collect { return@collect }` — `return@collect`
 * only returns from the lambda, it does not cancel the flow.
 *
 * @param key The page key to load.
 * @return Success with items and pagination keys, or Error.
 */
suspend fun <Value : Any> Store<PageKey, List<Value>>.loadPage(
    key: PageKey,
): StorePageResult<Value> {
    val response = stream(StoreReadRequest.cached(key, refresh = true))
        .filterNot { it is StoreReadResponse.Loading || it is StoreReadResponse.NoNewData || it is StoreReadResponse.Initial }
        .first() // Suspends until first Data or Error, then cancels the flow

    return when (response) {
        is StoreReadResponse.Data -> {
            val items = response.value
            StorePageResult.Success(
                items = items,
                prevKey = if (key.page > 0) key.page - 1 else null,
                nextKey = if (items.size >= key.pageSize) key.page + 1 else null,
            )
        }

        is StoreReadResponse.Error -> StorePageResult.Error(response.toThrowable())

        else -> StorePageResult.Error(RuntimeException("Unexpected store response: $response"))
    }
}

/**
 * Result of a paginated Store load, matching PagingSource.LoadResult shape.
 *
 * Consumer apps map this to `PagingSource.LoadResult` in their domain layer:
 * ```
 * when (result) {
 *     is StorePageResult.Success -> LoadResult.Page(result.items, result.prevKey, result.nextKey)
 *     is StorePageResult.Error -> LoadResult.Error(result.error)
 * }
 * ```
 */
sealed class StorePageResult<out T> {
    data class Success<T>(
        val items: List<T>,
        val prevKey: Int?,
        val nextKey: Int?,
    ) : StorePageResult<T>()

    data class Error(val error: Throwable) : StorePageResult<Nothing>()
}
```

### 5. Tests

**Path:** `core-base/store/src/commonTest/kotlin/template/core/base/store/StoreDataMapperTest.kt`

```kotlin
/*
 * Copyright 2025 Mifos Initiative
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * See https://github.com/openMF/kmp-project-template/blob/main/LICENSE
 */
package template.core.base.store

import app.cash.turbine.test
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.runTest
import org.mobilenativefoundation.store.store5.StoreReadResponse
import org.mobilenativefoundation.store.store5.StoreReadResponseOrigin
import template.core.base.common.DataState
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

// ─── Network + Cache mode tests ───

class StoreDataMapperCachedTest {

    @Test
    fun cacheDataEmitsWithCacheOrigin() = runTest {
        val flow = flowOf(
            StoreReadResponse.Data("cached", StoreReadResponseOrigin.SourceOfTruth),
        )
        flow.mapToStoreData().test {
            val item = awaitItem()
            assertEquals("cached", item.data)
            assertEquals(DataOrigin.CACHE, item.origin)
            assertFalse(item.isRefreshing)
            assertTrue(item.isStale)
            awaitComplete()
        }
    }

    @Test
    fun loadingThenCacheSetsRefreshing() = runTest {
        val flow = flowOf(
            StoreReadResponse.Loading(StoreReadResponseOrigin.Fetcher()),
            StoreReadResponse.Data("cached", StoreReadResponseOrigin.SourceOfTruth),
        )
        flow.mapToStoreData().test {
            val item = awaitItem()
            assertEquals("cached", item.data)
            assertTrue(item.isRefreshing)
            assertEquals(DataOrigin.CACHE, item.origin)
            awaitComplete()
        }
    }

    @Test
    fun cacheThenNetworkSequence() = runTest {
        val flow = flowOf(
            StoreReadResponse.Loading(StoreReadResponseOrigin.Fetcher()),
            StoreReadResponse.Data("cached", StoreReadResponseOrigin.SourceOfTruth),
            StoreReadResponse.Data("fresh", StoreReadResponseOrigin.Fetcher()),
        )
        flow.mapToStoreData().test {
            val cached = awaitItem()
            assertEquals("cached", cached.data)
            assertTrue(cached.isRefreshing)
            assertTrue(cached.isStale)

            val fresh = awaitItem()
            assertEquals("fresh", fresh.data)
            assertFalse(fresh.isRefreshing)
            assertFalse(fresh.isStale)
            assertNotNull(fresh.fetchedAt)
            assertEquals(DataOrigin.NETWORK, fresh.origin)
            awaitComplete()
        }
    }

    @Test
    fun errorAfterCacheKeepsLastData() = runTest {
        val flow = flowOf(
            StoreReadResponse.Data("cached", StoreReadResponseOrigin.SourceOfTruth),
            StoreReadResponse.Error.Exception(
                error = RuntimeException("timeout"),
                origin = StoreReadResponseOrigin.Fetcher(),
            ),
        )
        flow.mapToStoreDataWithErrors(fallback = "unused").test {
            val cached = awaitItem()
            assertEquals("cached", cached.data)
            assertNull(cached.error)
            assertTrue(cached.isSuccess)

            val errored = awaitItem()
            assertEquals("cached", errored.data)
            assertNotNull(errored.error)
            assertFalse(errored.isEmpty)  // has stale data
            assertFalse(errored.isError)  // not terminal — has data
            awaitComplete()
        }
    }
}

// ─── Network-only mode tests ───

class StoreDataMapperNetworkOnlyTest {

    @Test
    fun networkOnlySuccessEmitsWithNetworkOrigin() = runTest {
        // Network-only Store: Loading → Data(Fetcher) — no SourceOfTruth emissions
        val flow = flowOf(
            StoreReadResponse.Loading(StoreReadResponseOrigin.Fetcher()),
            StoreReadResponse.Data("fresh", StoreReadResponseOrigin.Fetcher()),
        )
        flow.mapToStoreData().test {
            val item = awaitItem()
            assertEquals("fresh", item.data)
            assertEquals(DataOrigin.NETWORK, item.origin)
            assertFalse(item.isRefreshing)
            assertFalse(item.isStale)  // network-only: always fresh
            assertNotNull(item.fetchedAt)
            awaitComplete()
        }
    }

    @Test
    fun networkOnlyErrorBeforeAnyData() = runTest {
        val flow = flowOf(
            StoreReadResponse.Loading(StoreReadResponseOrigin.Fetcher()),
            StoreReadResponse.Error.Message(
                message = "Network unavailable",
                origin = StoreReadResponseOrigin.Fetcher(),
            ),
        )
        flow.mapToStoreDataWithErrors(fallback = "none").test {
            val item = awaitItem()
            assertEquals("none", item.data)
            assertTrue(item.isEmpty)   // no real data received
            assertTrue(item.isError)   // terminal error
            assertNotNull(item.error)
            assertEquals("Network unavailable", item.error?.message)
            awaitComplete()
        }
    }

    @Test
    fun networkOnlyEmptyResult() = runTest {
        val flow = flowOf(
            StoreReadResponse.Data(emptyList<String>(), StoreReadResponseOrigin.Fetcher()),
        )
        flow.mapToStoreData(isEmpty = { it.isEmpty() }).test {
            val item = awaitItem()
            assertTrue(item.isEmpty)
            assertTrue(item.data.isEmpty())
            assertEquals(DataOrigin.NETWORK, item.origin)
            awaitComplete()
        }
    }
}

// ─── Shared behavior tests ───

class StoreDataMapperSharedTest {

    @Test
    fun initialResponseProducesNoEmissions() = runTest {
        flowOf(StoreReadResponse.Initial)
            .mapToStoreData().test { awaitComplete() }
    }

    @Test
    fun loadingAloneProducesNoEmissions() = runTest {
        flowOf(StoreReadResponse.Loading(StoreReadResponseOrigin.Fetcher()))
            .mapToStoreData().test { awaitComplete() }
    }

    @Test
    fun noNewDataProducesNoEmissions() = runTest {
        flowOf(StoreReadResponse.NoNewData(StoreReadResponseOrigin.Fetcher()))
            .mapToStoreData().test { awaitComplete() }
    }

    @Test
    fun memoryOriginMapsCorrectly() = runTest {
        flowOf(StoreReadResponse.Data("memory", StoreReadResponseOrigin.Cache))
            .mapToStoreData().test {
                assertEquals(DataOrigin.MEMORY, awaitItem().origin)
                awaitComplete()
            }
    }
}

// ─── StoreData property tests ───

class StoreDataTest {

    @Test
    fun isStaleWhenNeverFetched() {
        val data = StoreData("test", DataOrigin.CACHE, fetchedAt = null)
        assertTrue(data.isStale)
        assertNull(data.staleDuration)
    }

    @Test
    fun notStaleWhenFetched() {
        val mark = kotlin.time.TimeSource.Monotonic.markNow()
        val data = StoreData("test", DataOrigin.NETWORK, fetchedAt = mark)
        assertFalse(data.isStale)
        assertNotNull(data.staleDuration)
    }

    @Test
    fun networkOriginNeverStale() {
        // Network-only mode: origin=NETWORK, fetchedAt=null → NOT stale
        val data = StoreData("test", DataOrigin.NETWORK, fetchedAt = null)
        assertFalse(data.isStale)  // D12: network origin = never stale
    }

    @Test
    fun isSuccessWhenNoErrorAndNotEmpty() {
        val data = StoreData("test", DataOrigin.NETWORK)
        assertTrue(data.isSuccess)
        assertFalse(data.isError)
    }

    @Test
    fun isErrorWhenErrorAndEmpty() {
        val data = StoreData("", DataOrigin.NETWORK, error = RuntimeException("fail"), isEmpty = true)
        assertTrue(data.isError)
        assertFalse(data.isSuccess)
    }

    @Test
    fun mapPreservesMetadata() {
        val mark = kotlin.time.TimeSource.Monotonic.markNow()
        val original = StoreData("42", DataOrigin.NETWORK, isRefreshing = true, fetchedAt = mark)
        val mapped = original.map { it.toInt() }
        assertEquals(42, mapped.data)
        assertEquals(DataOrigin.NETWORK, mapped.origin)
        assertTrue(mapped.isRefreshing)
        assertEquals(mark, mapped.fetchedAt)
    }
}

// ─── DataState bridge tests ───

class StoreDataBridgeTest {

    @Test
    fun toDataStateSuccess() {
        val data = StoreData("test", DataOrigin.NETWORK)
        assertTrue(data.toDataState() is DataState.Success)
    }

    @Test
    fun toDataStatePendingWhenRefreshing() {
        val data = StoreData("cached", DataOrigin.CACHE, isRefreshing = true)
        val state = data.toDataState()
        assertTrue(state is DataState.Pending)
        assertEquals("cached", state.data)
    }

    @Test
    fun toDataStateErrorWithData() {
        val data = StoreData("stale", DataOrigin.CACHE, error = RuntimeException("fail"))
        val state = data.toDataState()
        assertTrue(state is DataState.Error)
        assertEquals("stale", state.data)
    }

    @Test
    fun toDataStateLoadingWhenEmpty() {
        val data = StoreData("", DataOrigin.NETWORK, isEmpty = true)
        assertTrue(data.toDataState() is DataState.Loading)
    }

    @Test
    fun toDataStateErrorWithNoData() {
        val data = StoreData("", DataOrigin.NETWORK, error = RuntimeException("fail"), isEmpty = true)
        val state = data.toDataState()
        assertTrue(state is DataState.Error)
        assertNull(state.data)
    }
}
```

---

## How Consumer Apps Use It

### Pattern 1: Network + Cache (offline-first)

```kotlin
// core/data — Repository uses Store with Fetcher + SourceOfTruth (Room)
class ClientRepository(
    private val store: Store<ClientKey, List<Client>>,  // createStore(fetcher, sourceOfTruth)
) : ClientRepositoryApi {

    override fun getClients(key: ClientKey): Flow<StoreData<List<Client>>> =
        store.streamDataWithErrors(key, fallback = emptyList(), isEmpty = { it.isEmpty() })

    override fun refreshClients(key: ClientKey): Flow<StoreData<List<Client>>> =
        store.freshData(key, isEmpty = { it.isEmpty() })
}

// feature/ — ViewModel calls repository directly (no use case needed)
class ClientListViewModel(private val repository: ClientRepositoryApi) : ViewModel() {
    val state = repository.getClients(ClientKey(0))
        .mapData { clients -> clients.sortedBy { it.name } }  // transform preserving metadata
        .map { it.toDataState() }  // or use StoreData directly
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), DataState.Loading)
}
```

### Pattern 2: Network only (no database)

```kotlin
// core/data — Same API, Store created with createMemoryStore (no SOT)
class ExchangeRateRepository(
    private val store: Store<CurrencyKey, ExchangeRate>,  // createMemoryStore(fetcher)
) : ExchangeRateRepositoryApi {

    override fun getRate(key: CurrencyKey): Flow<StoreData<ExchangeRate>> =
        store.streamDataWithErrors(key, fallback = ExchangeRate.EMPTY, isEmpty = { it == ExchangeRate.EMPTY })
}

// feature/ — ViewModel code is IDENTICAL to Pattern 1
// It doesn't know or care that this is network-only
class ExchangeViewModel(private val repository: ExchangeRateRepositoryApi) : ViewModel() {
    val state = repository.getRate(CurrencyKey("USD"))
        .map { it.toDataState() }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), DataState.Loading)
}
```

### Pattern 3: Paging via core/domain (transformation needed)

```kotlin
// core/domain — UseCase creates PagingSource wrapping Store
// (Only used when transformation/paging is needed — VMs usually call repos directly)
class GetClientsPaginatedUseCase(
    private val store: Store<PageKey, List<Client>>,
) {
    operator fun invoke(query: String? = null): Flow<PagingData<Client>> {
        return Pager(
            config = PagingConfig(pageSize = PageKey.DEFAULT_PAGE_SIZE),
            pagingSourceFactory = {
                object : PagingSource<Int, Client>() {
                    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Client> {
                        val page = params.key ?: 0
                        val pageKey = PageKey(page, params.loadSize, query)
                        return when (val result = store.loadPage(pageKey)) {
                            is StorePageResult.Success -> LoadResult.Page(
                                data = result.items,
                                prevKey = result.prevKey,
                                nextKey = result.nextKey,
                            )
                            is StorePageResult.Error -> LoadResult.Error(result.error)
                        }
                    }

                    override fun getRefreshKey(state: PagingState<Int, Client>): Int? {
                        return state.anchorPosition?.let { state.closestPageToPosition(it)?.prevKey?.plus(1) }
                    }
                }
            }
        ).flow
    }
}

// feature/ — ViewModel calls use case (domain layer — because paging is a transformation)
class ClientListViewModel(
    private val getClientsPaginated: GetClientsPaginatedUseCase,
) : ViewModel() {
    val pagingData = getClientsPaginated(query = null)
        .cachedIn(viewModelScope)
}
```

---

## UX Scenarios (all source modes)

| Scenario | Source Mode | StoreData State | UI |
|----------|-----------|-----------------|-----|
| First load, no cache | N+C | Loading → Data(Network) | Spinner → data |
| Cached + refresh | N+C | Data(Cache, refreshing) → Data(Network) | Data instantly + progress → updated |
| Cache hit, no changes | N+C | Data(Cache) → NoNewData | Data shown, no indicator |
| Network fails, has cache | N+C | Data(Cache) → Error(stale data) | Stale data + snackbar |
| Network fails, no cache | N+C | Error(empty, isEmpty=true) | Error screen + retry |
| Network success | N-only | Loading → Data(Network) | Spinner → data |
| Network fails | N-only | Loading → Error(isEmpty=true) | Error screen + retry |
| Empty result | Both | Data(isEmpty=true) | Empty state UI |
| TTL expired | N+C | Data(Cache, isStale) + refreshing | "Outdated" badge + auto-refresh |
| Pull-to-refresh | Both | freshData() → Data(Network) | Refresh indicator → data |
| Paginated list | N+C | PagingData via domain use case | Lazy list + page loading |

---

## Tasks

| ID | Task | Depends On | Effort |
|----|------|------------|--------|
| T1 | Verify `StoreReadResponseOrigin` sealed class (bytecode-verified ✅) | — | Done |
| T2 | Add `implementation(project(":core-base:common"))` to store build.gradle.kts | — | 5 min |
| T3 | Create `StoreData.kt` — data class + DataOrigin + toDataState() + isEmpty | T2 | 20 min |
| T4 | Create `StoreDataMapper.kt` — mapToStoreData + mapToStoreDataWithErrors + toThrowable | T3 | 30 min |
| T5 | Create `StoreDataExtensions.kt` — streamData, freshData, localData, map, mapData | T4 | 20 min |
| T6 | Create `StorePagingSource.kt` — PageKey + loadPage + StorePageResult | T4 | 25 min |
| T7 | Create `src/commonTest/kotlin/template/core/base/store/` directory | — | 2 min |
| T8 | Write tests — 20+ cases: cached, network-only, shared, properties, bridge | T5, T6, T7 | 40 min |
| T9 | Run spotlessCheck + detekt | T8 | 10 min |
| T10 | Run desktopTest + verify KMP targets compile | T9 | 10 min |

**Total:** ~3 hours

---

## Execution Order

```
T1 (done ✅) ─► T2 (gradle) ─► T3 (StoreData) ─► T4 (Mapper) ─► T5 (Extensions) ─┐
                                                                                     │
T7 (create dir) ────────────────────────────────────────────────────────────────────┤
                                                                 T6 (Paging) ──────┤
                                                                                     │
                                                                                     ├─► T8 (tests) ─► T9+T10 (CI)
```

---

## What's NOT in scope

- Concrete Fetcher/SourceOfTruth implementations (per-feature, per-app)
- Concrete PagingSource implementations (per-feature in core/domain)
- Koin DI wiring for stores (per-app)
- Adding `androidx.paging` to libs.versions.toml (consumer apps add when needed)
- Consumer app adoption (separate Phase 4 tasks)

---

## Relationship to Parent Plan

Extends **PLAN-store-offline-260429 Phase 3**:
- T3.1-T3.2: Module scaffold ✅
- T3.3: StoreFactory ✅ (createStore + createMemoryStore + createMutableStore)
- T3.4: StoreResponseMapper ✅ (mapToResult, mapToData)
- T3.5: DefaultValidator ✅
- T3.6: InMemoryBookkeeper ✅
- **T3.4b: StoreData + StoreDataMapper + Extensions + Paging** ← THIS PLAN
- T3.7+: DI, sample repo (future)

---

## Gap Analysis Log

### v1 → v2 (8 gaps)

| Gap | Severity | Fix |
|-----|----------|-----|
| GAP-01 | Critical | `StoreReadResponse.Origin` → `StoreReadResponseOrigin` |
| GAP-02 | High | Added `StoreReadResponse.Initial` handling |
| GAP-03 | High | Added `StoreReadResponseOrigin.Initial → MEMORY` |
| GAP-04 | Medium | `StoreReadResponseOrigin.Fetcher()` constructor in tests |
| GAP-05 | Medium | Added T5/T7 to create commonTest directory |
| GAP-06 | Medium | Added MPL 2.0 headers to all code |
| GAP-07 | Low | Verified `Error.Custom` exists in bytecode |
| GAP-08 | Low | Added `toDataState()` bridge |

### v2 → v3 (deep audit — 6 new gaps)

| Gap | Severity | Issue | Fix |
|-----|----------|-------|-----|
| GAP-09 | Critical | No network-only mode support — `isStale` always true without fetchedAt | Added D12: `isStale` now checks `origin != NETWORK`, not just `fetchedAt == null` |
| GAP-10 | Critical | No empty state detection — can't distinguish empty list from no-data | Added `isEmpty` field + lambda parameter on mappers |
| GAP-11 | High | No convenience Store extensions — repos have to call `.stream(StoreReadRequest.cached(...)).mapToStoreData()` every time | Added `StoreDataExtensions.kt`: `streamData()`, `freshData()`, `localData()` |
| GAP-12 | High | No paging support — Store 5 has no built-in paging artifact | Added `StorePagingSource.kt`: `PageKey`, `loadPage()`, `StorePageResult` |
| GAP-13 | High | Domain layer role unclear — plan assumed VMs always use repos | Added D15/D17: domain layer = transformation only (paging, combining). VMs call repos directly for simple data. |
| GAP-14 | Medium | No `map()` function to transform StoreData contents preserving metadata | Added `StoreData.map()` + `Flow<StoreData>.mapData()` in Extensions |

### v3 → v4 (final audit — 2 gaps)

| Gap | Severity | Issue | Fix |
|-----|----------|-------|-----|
| GAP-15 | **Blocker** | `loadPage()` uses `stream().collect { return@collect }` — `return@collect` does NOT break the infinite Store flow. Function hangs forever. | Rewrote using `filterNot { Loading/NoNewData/Initial }.first()` — suspends until first Data/Error, then cancels flow. |
| GAP-16 | Warning | `StoreReadRequest.fresh(key)` — second param `fallBackToSourceOfTruth` may not have a default value in alpha08 bytecode | Changed to explicit `StoreReadRequest.fresh(key, fallBackToSourceOfTruth = true)` |

**Verified no-issue (from bytecode audit):**
- `Store.stream()` returns infinite `Flow` (confirmed — never completes)
- `StoreReadRequest.localOnly(key)` exists with single param (confirmed)
- `StoreReadResponse.Error` has abstract `origin` accessible without casting (confirmed)
- `DataState<out T>` covariance makes `DataState.Loading` assignable to `DataState<T>` (confirmed)
- `internal` visibility in commonMain is accessible from commonTest (same module — confirmed)
- Multiple test classes per file — detekt `MaximumClassesPerFile` is inactive (confirmed)
- `StoreData<out T>.map()` extension compiles with covariant T (confirmed)
- `core-base/store` does NOT depend on `core-base/common` — T2 task adds it (confirmed)

---

## References

- [Store 5 StoreReadResponse](https://github.com/MobileNativeFoundation/Store/blob/main/store/src/commonMain/kotlin/org/mobilenativefoundation/store/store5/StoreReadResponse.kt)
- [Parent Plan: PLAN-store-offline-260429](./PLAN-store-offline-260429.md)
- [Existing StoreFactory](../../source/kmp-project-template/core-base/store/src/commonMain/kotlin/template/core/base/store/StoreFactory.kt)
- [Existing StoreResponseMapper](../../source/kmp-project-template/core-base/store/src/commonMain/kotlin/template/core/base/store/StoreResponseMapper.kt)
- [Existing DataState](../../source/kmp-project-template/core-base/common/src/commonMain/kotlin/template/core/base/common/DataState.kt)
- [Existing ResultExtensions](../../source/kmp-project-template/core/data/src/commonMain/kotlin/org/mifos/core/data/util/ResultExtensions.kt)
