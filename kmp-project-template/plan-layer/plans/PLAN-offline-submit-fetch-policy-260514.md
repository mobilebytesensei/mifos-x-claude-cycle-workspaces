# Implementation Plan: Offline Submit Outbox + FetchPolicy + Full KDoc

## Metadata

| Field | Value |
|---|---|
| Plan ID | PLAN-offline-submit-fetch-policy-260514 |
| Generated | 2026-05-14 (v2 — revised after gap audit) |
| Status | Completed — all GAPs implemented (GAP-8: DraftEntity TTL, GAP-9: KDoc, GAP-10: docs) |
| Scope | core-base/store · core/database · core/data · docs |
| Type | New Feature + Documentation |
| Branch | `feat/offline-submit-fetch-policy-260514` from `origin/development` |
| Target PR | `openMF/kmp-project-template` base `development` |

---

## Architectural Decisions (REVISED)

### A. Single database — `core/database/AppDatabase`

**Previous plan** proposed a separate `FrameworkDatabase`.
**Revised decision: ONE database.**

Rationale:
- `BookkeeperEntity` + `FetchedAtEntity` already live in `AppDatabase`. The draft table belongs alongside them.
- Two databases = two file handles, two KSP compilation passes, two migration histories.
- `core-base/database` module already provides `AppDatabaseFactory` for platform-specific creation — that role is unchanged. No new `@Database` class there.
- Template consumers add `DraftEntity` to their own `AppDatabase` the same way they already include `BookkeeperEntity` — it is documented in CLAUDE.md.

**Change:** Add `DraftEntity` + `DraftDao` to `core/database/AppDatabase`, bump to v5.

---

### B. `submitWithDraft` out-of-box via `DraftSubmitHandler<P, R>`

**Previous plan** added `submitWithDraft` as an extension on `SubmitHandler<R>` — still requires consumer to call a different API.
**Revised decision: new `DraftSubmitHandler<P, R>` class.**

`SubmitHandler<R>` is unchanged (existing consumers unaffected).
`DraftSubmitHandler<P, R>` wraps it and auto-saves on `ErrorCategory.Network`:

```kotlin
// ViewModel — fully out of box, no manual draft wiring:
private val submit = viewModelScope.draftSubmitHandler<LoanForm, Unit>(
    outbox = outbox,  // injected by DI
    formKey = "loanApplication:templateId=${templateId}",
)

fun onSave(form: LoanForm) = submit.submit(form) { api.createLoan(it) }
// ↑ If network fails → form saved to DraftDao automatically.
//   If non-network error → no draft saved (no stale drafts from validation errors).
```

`DraftSubmitHandler` delegates `state`, `retry()`, `reset()` to the inner `SubmitHandler`
so `MutationScreenContent` + `SubmitButton` need zero changes.

---

## Gaps Closed by This Plan

| Gap | Priority | Root Cause |
|-----|----------|------------|
| GAP-1 | P0 | No durable submit outbox — form data lost on process death |
| GAP-2 | P0 | No auto-retry of pending submissions on reconnect |
| GAP-3 | P1 | `FetchPolicy` missing — no "always fresh" or "cache only" option |
| GAP-4 | P1 | `FetchPolicy` not added to `PagingScreenStream` (missed in original plan) |
| GAP-5 | P1 | No draft-resume stream — screen can't know there's a pending draft |
| GAP-6 | P1 | `StoreCacheManager.clearAll()` doesn't clear drafts → cross-user data leak on logout |
| GAP-7 | P1 | `DraftDao` missing `getById` — `markSubmitted` can't function |
| GAP-8 | P1 | `DraftEntity` has no TTL / expiry — old drafts accumulate forever |
| GAP-9 | P2 | Zero KDoc on store public API — 50+ files undocumented |
| GAP-10 | P2 | CLAUDE.md store section missing new types from phases 8-11 |

---

## Gaps NOT in This Plan (deferred)

| Deferred Gap | Reason |
|---|---|
| Serialization DI coupling for `RoomSubmitOutbox<P>` | Needs kotlinx-serialization strategy doc; separate plan |
| `OfflineSubmitSyncer` WorkManager integration for long-lived sync | Separate infrastructure plan |
| Draft conflict detection (server state changed while offline) | Product decision needed |
| Multi-step form draft (which step was user on) | Consumer-specific, not framework |

---

## Complete Target File Map

```
core/database/
  entity/
    DraftEntity.kt              NEW — @Entity(framework_draft_submissions)
    DraftStatus.kt              NEW — enum PENDING / SUBMITTED / FAILED
  dao/
    DraftDao.kt                 NEW — CRUD + Flow<List<>> + getById + count
  AppDatabase.kt                MODIFIED — + DraftEntity, bump v5, AutoMigration(4→5)

core-base/store/
  submit/
    SubmitOutbox.kt             NEW — interface + SubmitOutboxEntry<P> + SubmitOutboxStatus
    DraftSubmitHandler.kt       NEW — wraps SubmitHandler, auto-saves on Network failure
    OfflineSubmitSyncer.kt      NEW — reconnect → retry all PENDING outbox entries
    DraftResumeStream.kt        NEW — observePendingDraft(formKey): Flow<DraftResumeState>
  screen/
    FetchPolicy.kt              NEW — CACHE_THEN_NETWORK / NETWORK_ONLY / CACHE_ONLY
    ScreenDataStream.kt         MODIFIED — + fetchPolicy param
    LoadOnceStream.kt           MODIFIED — + fetchPolicy param
  paging/
    PagingScreenStream.kt       MODIFIED — + fetchPolicy param on asPagingScreenStream()

core/data/
  store/
    RoomSubmitOutbox.kt         NEW — RoomSubmitOutbox<P> implementing SubmitOutbox<P>
  di/
    RepositoryModule.kt         MODIFIED — + DraftDao + RoomSubmitOutbox bindings
  repositoryImpl/
    StoreCacheManagerImpl.kt    MODIFIED — clearAll() also clears DraftDao

docs/
  store-implementation.md      NEW — full KDoc-level narrative for all store files
  CLAUDE.md                    MODIFIED — store section updated with new types
```

---

## Phases

### Phase 1 — `DraftEntity` + `DraftDao` + `AppDatabase` v5 ⬜

**`entity/DraftStatus.kt`**
```kotlin
enum class DraftStatus { PENDING, SUBMITTED, FAILED }
```

**`entity/DraftEntity.kt`**
```kotlin
@Entity(tableName = "framework_draft_submissions")
data class DraftEntity(
    @PrimaryKey val id: String,
    val formKey: String,
    val payloadJson: String,
    val status: DraftStatus = DraftStatus.PENDING,
    val createdAt: Long,
    val lastAttemptAt: Long? = null,
    val retryCount: Int = 0,
    val failureReason: String? = null,
)
```

**`dao/DraftDao.kt`**
```kotlin
@Dao
interface DraftDao {
    @Upsert
    suspend fun upsert(entry: DraftEntity)

    @Query("SELECT * FROM framework_draft_submissions WHERE id = :id LIMIT 1")
    suspend fun getById(id: String): DraftEntity?

    @Query("SELECT * FROM framework_draft_submissions WHERE formKey = :key AND status = 'PENDING'")
    fun observePending(key: String): Flow<List<DraftEntity>>

    @Query("SELECT COUNT(*) FROM framework_draft_submissions WHERE formKey = :key AND status = 'PENDING'")
    fun observePendingCount(key: String): Flow<Int>

    @Query("SELECT * FROM framework_draft_submissions WHERE status = 'PENDING'")
    suspend fun getAllPending(): List<DraftEntity>

    @Query("DELETE FROM framework_draft_submissions WHERE id = :id")
    suspend fun delete(id: String)

    @Query("DELETE FROM framework_draft_submissions WHERE createdAt < :beforeEpochMs")
    suspend fun deleteOlderThan(beforeEpochMs: Long)

    @Query("DELETE FROM framework_draft_submissions")
    suspend fun deleteAll()
}
```

**`AppDatabase.kt`** — add `DraftEntity::class`, add `draftDao()`, bump to VERSION = 5,
add `AutoMigration(from = 4, to = 5)`.

**build.gradle.kts** — add `room.schemaLocation` argument if not set.

Verify: `./gradlew :core:database:compileKotlinDesktop`

---

### Phase 2 — `SubmitOutbox<P>` interface in `core-base/store` ⬜

**`submit/SubmitOutbox.kt`**
```kotlin
/**
 * Durable outbox for form submissions that failed with a network error.
 *
 * Persists the submission payload to local storage so the user can resume the
 * flow after process death, navigation away, or app restart.
 *
 * Lifecycle of a draft entry:
 *   submit(payload) → network fails → save(PENDING)
 *   user returns    → observePendingDraft emits HasDraft
 *   user confirms   → DraftSubmitHandler retries → success → delete
 *
 * Obtain a [RoomSubmitOutbox] from DI for production use.
 *
 * @param P The payload type (must be serializable to JSON by [RoomSubmitOutbox]).
 */
interface SubmitOutbox<P : Any> {
    suspend fun save(entry: SubmitOutboxEntry<P>)
    suspend fun getById(id: String): SubmitOutboxEntry<P>?
    fun observePending(formKey: String): Flow<List<SubmitOutboxEntry<P>>>
    fun observePendingCount(formKey: String): Flow<Int>
    suspend fun getAllPending(): List<SubmitOutboxEntry<P>>
    suspend fun markSubmitted(id: String)
    suspend fun markFailed(id: String, reason: String)
    suspend fun delete(id: String)
    suspend fun deleteAll()
    /**
     * Delete drafts older than [before]. Call periodically for housekeeping.
     * Default: delete entries older than 30 days.
     */
    suspend fun purgeExpired(before: Instant = Clock.System.now() - 30.days)
}

/**
 * Status of a [SubmitOutboxEntry].
 */
enum class SubmitOutboxStatus { PENDING, SUBMITTED, FAILED }

/**
 * A single pending or historical submission entry in the outbox.
 */
@OptIn(ExperimentalTime::class)
data class SubmitOutboxEntry<out P : Any>(
    val id: String,
    val formKey: String,
    val payload: P,
    val status: SubmitOutboxStatus = SubmitOutboxStatus.PENDING,
    val createdAt: Instant,
    val lastAttemptAt: Instant? = null,
    val retryCount: Int = 0,
    val failureReason: String? = null,
)
```

Verify: `./gradlew :core-base:store:compileKotlinDesktop`

---

### Phase 3 — `DraftResumeStream` in `core-base/store` ⬜

**`submit/DraftResumeStream.kt`**

```kotlin
/**
 * State for a screen that may have a resumable pending draft.
 */
sealed interface DraftResumeState<out P : Any> {
    /** No pending draft for this form key. Show the empty form. */
    data object NoDraft : DraftResumeState<Nothing>
    /**
     * A pending draft exists. Prompt the user: "Resume from Xh ago?" or
     * pre-populate the form fields with [entry.payload].
     */
    data class HasDraft<P : Any>(val entry: SubmitOutboxEntry<P>) : DraftResumeState<P>
}

/**
 * Returns a reactive [DraftResumeState] stream for the given [formKey].
 *
 * Emits [DraftResumeState.HasDraft] when a PENDING entry exists in [outbox],
 * [DraftResumeState.NoDraft] otherwise.
 *
 * Typical ViewModel usage:
 * ```kotlin
 * val draftState: StateFlow<DraftResumeState<LoanForm>> =
 *     outbox.resumeStateFor("loanApplication:templateId=$id")
 *         .stateIn(viewModelScope, WhileSubscribed(5000), NoDraft)
 * ```
 */
fun <P : Any> SubmitOutbox<P>.resumeStateFor(formKey: String): Flow<DraftResumeState<P>> =
    observePending(formKey).map { entries ->
        val latest = entries.maxByOrNull { it.createdAt }
        if (latest != null) DraftResumeState.HasDraft(latest) else DraftResumeState.NoDraft
    }
```

Verify: compile.

---

### Phase 4 — `DraftSubmitHandler<P, R>` — out-of-box draft saving ⬜

**`submit/DraftSubmitHandler.kt`**

```kotlin
/**
 * Drop-in complement to [SubmitHandler] that automatically saves the submission
 * payload to a [SubmitOutbox] when the submission fails with a [ErrorCategory.Network]
 * error. Non-network failures (auth, server, validation) are NOT saved — they
 * require user action and should not auto-retry.
 *
 * Usage is identical to [SubmitHandler] except [submit] takes the payload explicitly:
 * ```kotlin
 * private val submit = viewModelScope.draftSubmitHandler<LoanForm, Unit>(
 *     outbox = outbox,
 *     formKey = "loanApplication:templateId=${templateId}",
 * )
 * val submitState = submit.state
 *
 * fun onSave(form: LoanForm) = submit.submit(form) { api.createLoan(it) }
 * fun onRetry()              = submit.retry()
 * fun onDismiss()            = submit.reset()
 * ```
 *
 * The [state], [retry], [reset] surface is identical to [SubmitHandler] so
 * [MutationScreenContent] + [SubmitButton] + [SubmitResultHandler] need zero changes.
 *
 * @param P The form payload type (what the user filled in).
 * @param R The submission result type.
 */
class DraftSubmitHandler<P : Any, R>(
    private val scope: CoroutineScope,
    private val outbox: SubmitOutbox<P>,
    private val formKey: String,
) {
    private val inner = SubmitHandler<R>(scope)

    /** Observable [SubmitState]. Expose via `.stateIn()` in the ViewModel. */
    val state: StateFlow<SubmitState<R>> = inner.state

    /**
     * Submit [payload] via [block].
     *
     * On [ErrorCategory.Network] failure: saves [payload] to [outbox] automatically.
     * On any other failure: propagates to [SubmitState.Failed] without saving.
     * On success: no draft interaction — caller should call [outbox.delete] if
     *   this was a resume of an existing draft.
     */
    @OptIn(ExperimentalTime::class)
    fun submit(payload: P, block: suspend (P) -> R) {
        inner.submit {
            try {
                block(payload)
            } catch (e: Exception) {
                if (categorize(e) == ErrorCategory.Network) {
                    scope.launch {
                        outbox.save(
                            SubmitOutboxEntry(
                                id = randomUuid(),
                                formKey = formKey,
                                payload = payload,
                                createdAt = Clock.System.now(),
                            )
                        )
                    }
                }
                throw e
            }
        }
    }

    /** Resume a specific draft by re-submitting its payload. */
    fun resumeDraft(entry: SubmitOutboxEntry<P>, block: suspend (P) -> R) {
        submit(entry.payload, block)
    }

    fun retry() = inner.retry()
    fun reset() = inner.reset()
}

/** Creates a [DraftSubmitHandler] bound to this [CoroutineScope]. */
fun <P : Any, R> CoroutineScope.draftSubmitHandler(
    outbox: SubmitOutbox<P>,
    formKey: String,
): DraftSubmitHandler<P, R> = DraftSubmitHandler(this, outbox, formKey)
```

**Tests — `DraftSubmitHandlerTest.kt`:**
- Network failure → `outbox.save` called with correct payload
- Non-network failure → `outbox.save` NOT called
- `resumeDraft` re-submits stored payload
- Already submitting → idempotent no-op

Verify: `./gradlew :core-base:store:desktopTest`

---

### Phase 5 — `OfflineSubmitSyncer` in `core-base/store` ⬜

**`submit/OfflineSubmitSyncer.kt`**

```kotlin
/**
 * Watches network connectivity and retries all [SubmitOutboxStatus.PENDING] entries
 * in [outbox] whenever the device comes back online.
 *
 * Intended for short-lived ViewModel-scope sync (user is actively in the form flow).
 * For long-lived background sync across sessions use a WorkManager worker at the
 * application layer — see `docs/store-implementation.md` → "Background Sync".
 *
 * ```kotlin
 * private val syncer = viewModelScope.offlineSubmitSyncer(
 *     outbox = outbox,
 *     networkMonitor = networkMonitor,
 * ) { payload -> api.createLoan(payload) }
 * ```
 */
class OfflineSubmitSyncer<P : Any, R>(
    private val outbox: SubmitOutbox<P>,
    private val networkMonitor: NetworkMonitor,
    private val scope: CoroutineScope,
    private val submitBlock: suspend (P) -> R,
    val onSynced: ((id: String, result: R) -> Unit)? = null,
    val onFailed: ((id: String, error: Throwable) -> Unit)? = null,
) {
    init { start() }

    private fun start() {
        scope.launch {
            networkMonitor.isOnlineDebounced(300L)
                .distinctUntilChanged()
                .filter { it }
                .drop(1) // skip initial — don't double-fire on first subscription
                .collect { syncAll() }
        }
    }

    suspend fun syncAll() {
        outbox.getAllPending().forEach { retry(it) }
    }

    @OptIn(ExperimentalTime::class)
    private suspend fun retry(entry: SubmitOutboxEntry<P>) {
        try {
            val result = submitBlock(entry.payload)
            outbox.delete(entry.id)
            onSynced?.invoke(entry.id, result)
        } catch (e: Exception) {
            outbox.markFailed(entry.id, e.message.orEmpty())
            onFailed?.invoke(entry.id, e)
        }
    }
}

fun <P : Any, R> CoroutineScope.offlineSubmitSyncer(
    outbox: SubmitOutbox<P>,
    networkMonitor: NetworkMonitor,
    onSynced: ((id: String, result: R) -> Unit)? = null,
    onFailed: ((id: String, error: Throwable) -> Unit)? = null,
    submitBlock: suspend (P) -> R,
): OfflineSubmitSyncer<P, R> = OfflineSubmitSyncer(
    outbox, networkMonitor, this, submitBlock, onSynced, onFailed
)
```

**Tests:** reconnect triggers `syncAll`; success deletes entry; failure calls `markFailed`.

---

### Phase 6 — `FetchPolicy` across all three stream types ⬜

**`screen/FetchPolicy.kt`**
```kotlin
/**
 * Controls how [ScreenDataStream], [LoadOnceStream], and [PagingScreenStream]
 * balance local cache against network freshness.
 *
 * | Policy             | First emission     | Network fetch triggered |
 * |--------------------|--------------------|-------------------------|
 * | CACHE_THEN_NETWORK | cached data (fast) | Yes, when TTL expires   |
 * | NETWORK_ONLY       | network data       | Always — bypasses TTL   |
 * | CACHE_ONLY         | cached data        | Never                   |
 */
enum class FetchPolicy {
    CACHE_THEN_NETWORK,
    NETWORK_ONLY,
    CACHE_ONLY,
}
```

**Modifications:**

`ScreenDataStream.kt` — `Store<Key, Output>.asScreenStream(...)`:
- Add `fetchPolicy: FetchPolicy = FetchPolicy.CACHE_THEN_NETWORK`
- `CACHE_THEN_NETWORK`: current behaviour (no code change inside)
- `NETWORK_ONLY`: use `StoreRequest.fresh(key)` instead of `StoreRequest.cached(key)`;
  skip auto-reconnect launch (no stale-then-fresh flicker needed)
- `CACHE_ONLY`: use `StoreRequest.cached(key, fallBackToSourceOfTruth = false)`;
  skip the auto-reconnect launch entirely

`LoadOnceStream.kt` — `Store<Key, Output>.asLoadOnceStream(...)`:
- Same `fetchPolicy` parameter with identical semantics.

`PagingScreenStream.kt` — `Store<PageKey, List<T>>.asPagingScreenStream(...)`:
- Add `fetchPolicy: FetchPolicy = FetchPolicy.CACHE_THEN_NETWORK`
- `NETWORK_ONLY`: initial load always uses `refresh = true`; TTL bypass
- `CACHE_ONLY`: never call fetcher; load only from SourceOfTruth

**Tests — `FetchPolicyTest.kt`:**
- `NETWORK_ONLY` → fetcher always called, no cached emission before network
- `CACHE_ONLY` → fetcher never called, SoT data emitted

Verify: `./gradlew :core-base:store:allTests`

---

### Phase 7 — `RoomSubmitOutbox<P>` in `core/data` ⬜

**`store/RoomSubmitOutbox.kt`**

```kotlin
/**
 * [SubmitOutbox] backed by Room's [DraftDao]. Serializes [P] to/from JSON via
 * kotlinx.serialization.
 *
 * Create one instance per form type:
 * ```kotlin
 * val loanOutbox: SubmitOutbox<LoanForm> = RoomSubmitOutbox(
 *     dao = db.draftDao(),
 *     serializer = LoanForm.serializer(),
 * )
 * ```
 */
@OptIn(ExperimentalTime::class)
class RoomSubmitOutbox<P : Any>(
    private val dao: DraftDao,
    private val serializer: KSerializer<P>,
    private val json: Json = Json { ignoreUnknownKeys = true },
) : SubmitOutbox<P> {

    override suspend fun save(entry: SubmitOutboxEntry<P>) =
        dao.upsert(entry.toEntity(json, serializer))

    override suspend fun getById(id: String): SubmitOutboxEntry<P>? =
        dao.getById(id)?.toDomain(json, serializer)

    override fun observePending(formKey: String): Flow<List<SubmitOutboxEntry<P>>> =
        dao.observePending(formKey).map { it.map { e -> e.toDomain(json, serializer) } }

    override fun observePendingCount(formKey: String): Flow<Int> =
        dao.observePendingCount(formKey)

    override suspend fun getAllPending(): List<SubmitOutboxEntry<P>> =
        dao.getAllPending().map { it.toDomain(json, serializer) }

    override suspend fun markSubmitted(id: String) {
        dao.getById(id)?.let { dao.upsert(it.copy(status = DraftStatus.SUBMITTED)) }
    }

    override suspend fun markFailed(id: String, reason: String) {
        dao.getById(id)?.let {
            dao.upsert(it.copy(
                status = DraftStatus.FAILED,
                retryCount = it.retryCount + 1,
                lastAttemptAt = Clock.System.now().toEpochMilliseconds(),
                failureReason = reason,
            ))
        }
    }

    override suspend fun delete(id: String) = dao.delete(id)
    override suspend fun deleteAll() = dao.deleteAll()
    override suspend fun purgeExpired(before: Instant) =
        dao.deleteOlderThan(before.toEpochMilliseconds())
}

// Mapper functions in companion or private scope:
private fun <P : Any> SubmitOutboxEntry<P>.toEntity(json: Json, s: KSerializer<P>) =
    DraftEntity(
        id = id, formKey = formKey,
        payloadJson = json.encodeToString(s, payload),
        status = status.toDraftStatus(),
        createdAt = createdAt.toEpochMilliseconds(),
        lastAttemptAt = lastAttemptAt?.toEpochMilliseconds(),
        retryCount = retryCount, failureReason = failureReason,
    )

private fun <P : Any> DraftEntity.toDomain(json: Json, s: KSerializer<P>) =
    SubmitOutboxEntry(
        id = id, formKey = formKey,
        payload = json.decodeFromString(s, payloadJson),
        status = status.toOutboxStatus(),
        createdAt = Instant.fromEpochMilliseconds(createdAt),
        lastAttemptAt = lastAttemptAt?.let { Instant.fromEpochMilliseconds(it) },
        retryCount = retryCount, failureReason = failureReason,
    )
```

---

### Phase 8 — Logout safety: `StoreCacheManager` clears drafts ⬜

**`StoreCacheManagerImpl.kt`** — add `DraftDao` constructor param, add to `clearAll()`:
```kotlin
class StoreCacheManagerImpl(
    ...
    private val draftDao: DraftDao,   // NEW
) : StoreCacheManager {
    override suspend fun clearAll() {
        ...existing clears...
        draftDao.deleteAll()           // NEW — clears pending submissions on logout
    }
}
```

**`RepositoryModule.kt`** — wire `draftDao` into `StoreCacheManagerImpl` binding.

> **Security note:** This prevents user A's pending form submissions from being
> visible to user B on shared devices.

---

### Phase 9 — DI wiring ⬜

**`RepositoryModule.kt`** additions:
```kotlin
single { get<AppDatabase>().draftDao() }
// Note: RoomSubmitOutbox<P> is NOT a singleton here — each form type creates its own.
// Feature modules create their outbox instances in their own DI modules:
//
//   val loanFeatureModule = module {
//       single<SubmitOutbox<LoanForm>> {
//           RoomSubmitOutbox(dao = get(), serializer = LoanForm.serializer())
//       }
//   }
```

Add `draftDao()` abstract fun to `AppDatabase`.

---

### Phase 10 — Full KDoc documentation of store implementation ⬜

Add comprehensive KDoc to every public API surface across all store-related modules.

#### `core-base/store` (22 files)

| File | Doc status today | Target |
|------|-----------------|--------|
| `screen/ScreenState.kt` | Minimal | Full sealed class + each variant KDoc |
| `screen/DataFreshness` (in ScreenState.kt) | None | Each enum constant documented |
| `screen/ScreenDataStream.kt` | Partial | Full class + `asScreenStream` overloads |
| `screen/LoadOnceStream.kt` | Good | Minor additions for `fetchPolicy` param |
| `screen/ScreenStateExtensions.kt` | Partial | All extension functions |
| `screen/StoreData.kt` | Good | `DataOrigin` enum constants |
| `screen/StoreDataExtensions.kt` | None | Every extension function |
| `screen/StoreDataMapper.kt` | None | Class + all functions |
| `screen/StoreResponseMapper.kt` | None | Class + all functions |
| `paging/PagingScreenStream.kt` | Good | Add `fetchPolicy` param docs |
| `paging/StorePagingSource.kt` | Partial | Full class doc |
| `submit/SubmitState.kt` | Good | State transition diagram in KDoc |
| `submit/SubmitHandler.kt` | Good | Add cross-ref to `DraftSubmitHandler` |
| `submit/SubmitStateExtensions.kt` | Good | Minor: cross-refs |
| `submit/SubmitOutbox.kt` | NEW | Full interface + entry + status |
| `submit/DraftSubmitHandler.kt` | NEW | Full class + lifecycle diagram |
| `submit/DraftResumeStream.kt` | NEW | Full sealed + extension |
| `submit/OfflineSubmitSyncer.kt` | NEW | Full class |
| `submit/MutationUiState.kt` | Good | Cross-ref `DraftSubmitHandler` |
| `error/ErrorCategory.kt` | Good | `categorize()` matching rules in KDoc |
| `error/OfflineException.kt` | None | Class doc |
| `infra/StoreFactory.kt` | Good | Cross-ref read-only vs MutableStore |
| `infra/StoreRegistry.kt` | Good | N/A |
| `infra/DecisionEngine.kt` | Good | N/A |
| `infra/DefaultValidator.kt` | Good | `alwaysValid()` vs `withTtl()` guidance |
| `infra/InMemoryBookkeeper.kt` | Good | Note: dev/test only |
| `infra/FetchedAtRepository.kt` | Excellent | N/A |
| `screen/FetchPolicy.kt` | NEW | Full enum with table |

#### `core-base/ui` (8 submit/screen files)

| File | Target |
|------|--------|
| `submit/SubmitProgressOverlay.kt` | Doc `visible` + `SubmitState` overload usage |
| `submit/SubmitResultHandler.kt` | Full LaunchedEffect behaviour doc |
| `submit/MutationScreenContent.kt` | NEW — already has KDoc |
| `submit/SubmitButton.kt` | NEW — add usage patterns |
| `screen/ScreenContent.kt` | Override precedence chain documented |
| `screen/ScreenStateDefaults.kt` | LocalCompositionLocal pattern |
| `screen/DataFreshnessIndicator.kt` | When to show / hide |
| `paging/PagingScreenContent.kt` | Load-more trigger pattern |

#### `core/database` (key files)

| File | Target |
|------|--------|
| `AppDatabase.kt` | All tables listed with one-liner purpose |
| `entity/DraftEntity.kt` | NEW — full field docs |
| `dao/DraftDao.kt` | NEW — full query docs |
| `dao/BookkeeperDao.kt` | None today → full |
| `dao/FetchedAtDao.kt` | None today → full |

#### `core/data` (key files)

| File | Target |
|------|--------|
| `store/RoomSubmitOutbox.kt` | NEW — full |
| `store/RoomBookkeeper.kt` | Existing — verify |
| `repositoryImpl/RoomFetchedAtRepository.kt` | Existing — verify |
| `repository/StoreCacheManager.kt` | Add logout-safety note |
| `repositoryImpl/StoreCacheManagerImpl.kt` | Add draft clear mention |

#### New narrative doc: `docs/store-implementation.md`

Full prose covering:
1. Architecture overview (core-base/store → core/data → feature modules)
2. Read-side patterns: ScreenDataStream, LoadOnceStream, PagingScreenStream, FetchPolicy
3. Write-side patterns: SubmitHandler, DraftSubmitHandler, OfflineSubmitSyncer
4. State machines: ScreenState transitions, SubmitState transitions
5. Offline patterns: data-sync vs form-submission outbox (when to use what)
6. Background sync: ViewModel scope vs WorkManager guidance
7. Logout / cache clearing: StoreCacheManager, draft purge
8. How to add a new Store (step-by-step recipe)
9. How to add a new form with draft support (step-by-step recipe)

---

### Phase 11 — CLAUDE.md store section update ⬜

Update `CLAUDE.md` "Customization Points" section to include:

```markdown
### Store / Offline Layer

**Read-side** (data → screen):
- `ScreenDataStream.asScreenStream()` — continuous cache+network stream
- `Store.asLoadOnceStream()` — load-once for edit screens (no background overwrites)
- `PagingScreenStream.asPagingScreenStream()` — infinite scroll
- `FetchPolicy` param on all three: CACHE_THEN_NETWORK (default) | NETWORK_ONLY | CACHE_ONLY

**Write-side** (form → server):
- `SubmitHandler<R>` — one-shot submit, no draft persistence
- `DraftSubmitHandler<P, R>` — out-of-box draft saving on network failure
- `OfflineSubmitSyncer` — reconnect → auto-retry PENDING outbox entries
- `DraftResumeStream` — `outbox.resumeStateFor(formKey)` for "resume draft" UX

**Offline patterns** (see `docs/store-implementation.md`):
- Pattern A — data-sync: `MutableStore` + `RoomBookkeeper` (entities already in Room)
- Pattern B — form outbox: `DraftSubmitHandler` + `RoomSubmitOutbox` (one-shot payloads)
  DO NOT use MutableStore for form submissions — Bookkeeper stores only timestamps.

**New types (phases 8–11 of PLAN-core-base-reorg-260514)**:
- `MutationUiState<T,R>` — combined read+write state for edit screens
- `MutationScreenContent` — bundles ScreenContent + overlay + result handler
- `SubmitButton` (wraps `KptButton`) — auto-disables when Submitting
- `KptButton` / `KptOutlinedButton` / `KptTextButton` — design system buttons
```

---

## Execution Summary

| Phase | Module(s) | Key Deliverable |
|-------|-----------|-----------------|
| 1 | core/database | DraftEntity + DraftDao + AppDatabase v5 |
| 2 | core-base/store | SubmitOutbox<P> interface + SubmitOutboxEntry |
| 3 | core-base/store | DraftResumeStream + resumeStateFor() |
| 4 | core-base/store | DraftSubmitHandler — out-of-box draft saving |
| 5 | core-base/store | OfflineSubmitSyncer |
| 6 | core-base/store | FetchPolicy + all 3 stream types updated |
| 7 | core/data | RoomSubmitOutbox<P> |
| 8 | core/data | StoreCacheManager clears drafts on logout |
| 9 | core/data | DI wiring — DraftDao bound, DraftSubmitHandler factory documented |
| 10 | all | Full KDoc on 40+ files + store-implementation.md |
| 11 | docs | CLAUDE.md store section updated |

---

## Execution Log

| Phase | Status | Notes |
|-------|--------|-------|
| 1 | ⬜ Todo | |
| 2 | ⬜ Todo | |
| 3 | ⬜ Todo | |
| 4 | ⬜ Todo | |
| 5 | ⬜ Todo | |
| 6 | ⬜ Todo | |
| 7 | ⬜ Todo | |
| 8 | ⬜ Todo | |
| 9 | ⬜ Todo | |
| 10 | ⬜ Todo | |
| 11 | ⬜ Todo | |
