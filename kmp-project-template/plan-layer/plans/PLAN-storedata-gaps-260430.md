# PLAN-storedata-gaps-260430: StoreData API Gap Fixes

| Field | Value |
|-------|-------|
| ID | storedata-gaps-260430 |
| Status | Draft |
| Priority | P1 |
| Scope | `core-base/store` — fix 6 gaps + add 3 missing tests |
| Created | 2026-04-30 |
| Prerequisites | PLAN-storedata-api-260430 (completed) |
| Effort | ~2 hours |
| Parent Plan | PLAN-storedata-api-260430 |

---

## Problem Statement

Deep audit of the StoreData API implementation against Store 5 official source code (v5.1.0-alpha08) found 11 gaps: 0 blockers, 3 medium, 8 low. This plan addresses the 3 medium gaps, 3 code-quality low gaps, and 3 test coverage gaps.

---

## Gaps to Fix

### Medium Severity

| # | Gap | File | Issue |
|---|-----|------|-------|
| GAP-1 | `toThrowable()` doesn't unwrap `Custom<Throwable>` | StoreDataMapper.kt:163 | Official `doThrow()` checks `if (error is Throwable) error else RuntimeException(...)`. Ours always wraps in RuntimeException — loses original exception type for Custom errors. |
| GAP-3 | `mapToStoreData()` swallows errors silently | StoreDataMapper.kt:62-64 | After `Loading -> Data(Cache, refreshing=true) -> Error`, no emission is produced. ViewModel sees `isRefreshing=true` forever — perpetual loading indicator on stale cached data. |
| GAP-6 | `loadPage()` returns cached data for N+C stores | StorePagingSource.kt:79-85 | `.first()` takes first non-Loading emission which is `Data(SOT)` for cached stores, not `Data(Fetcher)`. Fresh network page is never returned. |

### Low Severity (Code Quality)

| # | Gap | File | Issue |
|---|-----|------|-------|
| GAP-2 | `toDataState()` never maps to `DataState.NoNetwork` | StoreData.kt:78-85 | DataState has 5 variants but bridge only produces 4. NoNetwork is never used. |
| GAP-7 | No test for `Error.Custom` variant | StoreDataMapperTest.kt | `toThrowable()` Custom branch is untested. |
| GAP-8 | No test for `mapData()` Flow extension | StoreDataMapperTest.kt | `Flow<StoreData>.mapData()` has zero test coverage. |
| GAP-9 | No test for `mapToStoreDataWithErrors` + `Error.Custom` | StoreDataMapperTest.kt | Error.Custom in error-forwarding mapper is untested. |

### Deferred (Not in Scope)

| # | Gap | Reason |
|---|-----|--------|
| GAP-4 | Mutable state thread safety | Theoretical only — Flow transform is sequential by contract. Add KDoc note. |
| GAP-5 | No `skipMemory` variant | Niche use case, add when needed. |
| GAP-10 | `isStale=true` on cold MEMORY hit | Correct behavior — first collection has no fetchedAt. Document in KDoc. |
| GAP-11 | `isEmpty` uses `!hasReceivedData` | By design — isEmpty means "no real data from Store" not "collection is empty". |

---

## Design Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Fix `toThrowable()` to match official `doThrow()` | Preserves original exception types for catch blocks and error UX |
| D2 | `mapToStoreData()` re-emits last data with `isRefreshing=false` on error | ViewModel needs to clear the loading indicator. Silent swallow leaves UI stuck. |
| D3 | `loadPage()` uses `fresh()` instead of `cached()` | Paging always wants the latest page from network. Cache hit for page 5 is usually stale. If caller wants cached, they can use `streamData()` directly. |
| D4 | `toDataState()` does NOT map to `NoNetwork` | Cannot reliably detect network errors in commonMain (no `java.net` on iOS/JS). Leave error type inspection to ViewModel. Add KDoc explaining this. |
| D5 | Add KDoc to `mapToStoreData` about thread safety | Document that Flow transform is sequential, shared flow before mapper needs care. |

---

## Files to Modify

### 1. `StoreDataMapper.kt` — Fix GAP-1 + GAP-3 + GAP-4 (KDoc)

**GAP-1 fix** — `toThrowable()` unwraps Custom<Throwable>:

```kotlin
internal fun StoreReadResponse.Error.toThrowable(): Throwable {
    return when (this) {
        is StoreReadResponse.Error.Exception -> error
        is StoreReadResponse.Error.Message -> RuntimeException(message)
        is StoreReadResponse.Error.Custom<*> ->
            if (error is Throwable) error as Throwable
            else RuntimeException("Store error: $error")
    }
}
```

**GAP-3 fix** — `mapToStoreData()` re-emits on error to clear refreshing state:

```kotlin
fun <Output : Any> Flow<StoreReadResponse<Output>>.mapToStoreData(
    isEmpty: (Output) -> Boolean = { false },
): Flow<StoreData<Output>> {
    var refreshing = false
    var lastFetchMark: TimeSource.Monotonic.ValueTimeMark? = null
    var lastData: Output? = null

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
                // Re-emit last data with isRefreshing=false so ViewModel
                // can clear loading indicators. Without this, after
                // Loading -> Data(Cache, refreshing=true) -> Error,
                // the ViewModel would show a perpetual loading state.
                lastData?.let { data ->
                    emit(
                        StoreData(
                            data = data,
                            origin = DataOrigin.CACHE,
                            isRefreshing = false,
                            fetchedAt = lastFetchMark,
                            isEmpty = isEmpty(data),
                        ),
                    )
                }
            }
        }
    }
}
```

**GAP-4 KDoc** — Add thread safety note to both mapper functions:

```kotlin
/**
 * ...existing KDoc...
 *
 * **Thread safety:** This function uses internal mutable state that is safe
 * under Flow's sequential emission contract. If the upstream flow is shared
 * (e.g., via `shareIn`), apply this mapper AFTER sharing, not before.
 */
```

### 2. `StorePagingSource.kt` — Fix GAP-6

**Change `cached(key, refresh=true)` to `fresh(key)`:**

```kotlin
suspend fun <Value : Any> Store<PageKey, List<Value>>.loadPage(
    key: PageKey,
): StorePageResult<Value> {
    val response = stream(StoreReadRequest.fresh(key, fallBackToSourceOfTruth = true))
        .filterNot {
            it is StoreReadResponse.Loading ||
                it is StoreReadResponse.NoNewData ||
                it is StoreReadResponse.Initial
        }
        .first()

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
```

### 3. `StoreData.kt` — Fix GAP-2 (KDoc only)

**Add KDoc explaining why NoNetwork is not mapped:**

```kotlin
/**
 * Converts [StoreData] to [DataState] for ViewModels using DataState patterns.
 *
 * Mapping:
 * - [isEmpty] + no error -> [DataState.Loading] (no data yet)
 * - [isRefreshing] + data -> [DataState.Pending] (cached data, refresh in progress)
 * - [error] != null -> [DataState.Error] (with optional stale data)
 * - data present, no error -> [DataState.Success]
 *
 * **Note:** [DataState.NoNetwork] is not produced by this bridge because
 * network error detection is platform-specific (no `java.net` in KMP commonMain).
 * ViewModels that need no-network distinction should inspect [StoreData.error]
 * directly or use a platform-specific error classifier.
 */
```

### 4. `StoreDataMapperTest.kt` — Fix GAP-7 + GAP-8 + GAP-9

**Add 4 new test cases:**

```kotlin
// --- Error.Custom tests (GAP-7, GAP-9) ---

class StoreDataMapperCustomErrorTest {

    @Test
    fun customThrowableErrorUnwrapsOriginal() = runTest {
        val original = IllegalStateException("custom")
        val flow = flowOf(
            StoreReadResponse.Error.Custom(
                error = original,
                origin = StoreReadResponseOrigin.Fetcher(),
            ),
        )
        flow.mapToStoreDataWithErrors(fallback = "fallback").test {
            val item = awaitItem()
            assertTrue(item.error is IllegalStateException)
            assertEquals("custom", item.error?.message)
            awaitComplete()
        }
    }

    @Test
    fun customNonThrowableErrorWrapsInRuntimeException() = runTest {
        val flow = flowOf(
            StoreReadResponse.Error.Custom(
                error = "string error",
                origin = StoreReadResponseOrigin.Fetcher(),
            ),
        )
        flow.mapToStoreDataWithErrors(fallback = "fallback").test {
            val item = awaitItem()
            assertTrue(item.error is RuntimeException)
            assertTrue(item.error?.message?.contains("string error") == true)
            awaitComplete()
        }
    }
}

// --- mapToStoreData error re-emission test (GAP-3) ---

class StoreDataMapperErrorReEmitTest {

    @Test
    fun errorAfterCacheReEmitsWithRefreshingFalse() = runTest {
        val flow = flowOf(
            StoreReadResponse.Loading(StoreReadResponseOrigin.Fetcher()),
            StoreReadResponse.Data("cached", StoreReadResponseOrigin.SourceOfTruth),
            StoreReadResponse.Error.Exception(
                error = RuntimeException("timeout"),
                origin = StoreReadResponseOrigin.Fetcher(),
            ),
        )
        flow.mapToStoreData().test {
            val cached = awaitItem()
            assertEquals("cached", cached.data)
            assertTrue(cached.isRefreshing)

            val reEmitted = awaitItem()
            assertEquals("cached", reEmitted.data)
            assertFalse(reEmitted.isRefreshing) // cleared
            assertNull(reEmitted.error)          // mapToStoreData doesn't carry error
            awaitComplete()
        }
    }

    @Test
    fun errorBeforeAnyDataProducesNoEmission() = runTest {
        // No data received yet, so nothing to re-emit
        val flow = flowOf(
            StoreReadResponse.Loading(StoreReadResponseOrigin.Fetcher()),
            StoreReadResponse.Error.Exception(
                error = RuntimeException("fail"),
                origin = StoreReadResponseOrigin.Fetcher(),
            ),
        )
        flow.mapToStoreData().test {
            awaitComplete() // no emissions
        }
    }
}

// --- mapData Flow extension test (GAP-8) ---

class StoreDataFlowExtensionsTest {

    @Test
    fun mapDataTransformsFlowPreservingMetadata() = runTest {
        val mark = kotlin.time.TimeSource.Monotonic.markNow()
        val original = StoreData(
            "42",
            DataOrigin.NETWORK,
            isRefreshing = false,
            fetchedAt = mark,
        )
        flowOf(original).mapData { it.toInt() }.test {
            val item = awaitItem()
            assertEquals(42, item.data)
            assertEquals(DataOrigin.NETWORK, item.origin)
            assertEquals(mark, item.fetchedAt)
            awaitComplete()
        }
    }
}
```

---

## Tasks

| ID | Task | Depends On | Effort |
|----|------|------------|--------|
| T1 | Fix `toThrowable()` — unwrap Custom<Throwable> (GAP-1) | — | 5 min |
| T2 | Fix `mapToStoreData()` — re-emit on error to clear refreshing (GAP-3) | — | 15 min |
| T3 | Fix `loadPage()` — use `fresh()` instead of `cached()` (GAP-6) | — | 5 min |
| T4 | Add KDoc to `toDataState()` re: NoNetwork (GAP-2) | — | 5 min |
| T5 | Add thread safety KDoc to mappers (GAP-4) | — | 5 min |
| T6 | Add tests: Error.Custom unwrap + non-Throwable Custom (GAP-7, GAP-9) | T1 | 10 min |
| T7 | Add tests: mapToStoreData error re-emission (GAP-3 regression) | T2 | 10 min |
| T8 | Add test: mapData Flow extension (GAP-8) | — | 5 min |
| T9 | Run spotlessApply + detekt | T1-T8 | 5 min |
| T10 | Run desktopTest — all tests green | T9 | 5 min |

**Total:** ~1.5 hours

---

## Execution Order

```
T1 (toThrowable) ──────┐
T2 (mapToStoreData) ────┤
T3 (loadPage) ──────────┤
T4 (NoNetwork KDoc) ────┼──► T9 (spotless+detekt) ──► T10 (desktopTest)
T5 (thread safety KDoc) ┤
T6 (Custom tests) ──────┤
T7 (error re-emit tests)┤
T8 (mapData test) ──────┘
```

T1-T8 are independent — can be done in parallel.

---

## What's NOT in scope

| Gap | Reason |
|-----|--------|
| GAP-4 thread safety fix | Theoretical — Flow contract guarantees sequential. KDoc is sufficient. |
| GAP-5 skipMemory variant | Niche. Add when consumer needs it. |
| GAP-10 isStale on MEMORY | Correct behavior. First cold collection has no prior fetch context. |
| GAP-11 isEmpty semantics | By design. "No real data received" is the intended meaning. |

---

## Verification

After all tasks complete:
1. All existing 20 tests still pass (no regressions)
2. 5 new tests pass (Error.Custom x2, error re-emit x2, mapData x1)
3. spotlessCheck clean
4. detekt clean
5. Zero warnings in desktopTest
