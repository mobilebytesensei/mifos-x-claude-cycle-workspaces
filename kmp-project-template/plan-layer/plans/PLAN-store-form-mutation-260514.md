# PLAN-store-form-mutation-260514: Form/Mutation Submission Capability

| Field | Value |
|-------|-------|
| ID | store-form-mutation-260514 |
| Status | Completed |
| Priority | P0 |
| Scope | `core-base/store` + `core-base/ui` |
| Created | 2026-05-14 |
| Updated | 2026-05-14 |
| Prerequisites | PLAN-store5-full-capability-260502 (completed) |
| Effort | ~4–5 hours (5 phases) |
| Naming convention | `SubmitState` / `SubmitHandler` (see naming audit below) |
| DI Framework | Koin |

---

## Naming Convention Decision

Audited all 18 files in `core-base/store`. Three naming families exist:

| Family | Used for | Examples |
|--------|----------|---------|
| `Screen*` | UI-level state concepts | `ScreenState`, `ScreenDataStream`, `ScreenStateExtensions` |
| `Store*` | Store5 infrastructure | `StoreData`, `StoreFactory`, `StorePagingSource` |
| `Paging*` | Paging modifier | `PagingScreenStream` |

**Chosen: `Submit*`** — state type + `Handler` suffix for executor.

```
SubmitState<R>   ← sealed interface  (not "Mutation" — GraphQL connotation)
  Idle           ←  no submission in flight
  Submitting     ←  API call executing
  Submitted<R>   ←  success  (past-tense mirrors "Submitting")
  Failed         ←  error

SubmitHandler<R> ← executor class   (not "Stream" — writes are one-shot, not Flow)
  .submit { }
  .retry()
  .reset()

CoroutineScope.submitHandler<R>()   ← factory extension
```

`Handler` over `Stream` because `*Stream` in this module is always a continuous `Flow` wrapper
(`ScreenDataStream`, `PagingScreenStream`). A write is a single execution — `Handler` makes
the architectural distinction explicit.

---

## Problem Statement

`core-base/store` covers two of the three core data interaction patterns:
- ✅ **Detail** — `Store.asScreenStream()` → `ScreenDataStream<T>` → `ScreenState`
- ✅ **Listing/Paging** — `Store.asPagingScreenStream()` → `PagingScreenStream<T>`
- ❌ **Form/Submit** — POST · PUT · DELETE lifecycle (COMPLETELY ABSENT)

Any screen where a user **fills in data and submits** (create entity, update profile, delete record,
confirm action) has no framework support. Each ViewModel hand-rolls the same boilerplate:

```kotlin
// CURRENT — repeated in every write ViewModel
private val _isLoading = MutableStateFlow(false)
private val _error    = MutableStateFlow<String?>(null)

fun onSubmit(data: FormData) {
    viewModelScope.launch {
        _isLoading.value = true
        try   { repository.create(data); sendEvent(NavigateBack) }
        catch (e: Exception) { _error.value = e.message }
        finally { _isLoading.value = false }
    }
}
```

Problems:
1. No standardised state type — `isLoading + error?` is not exhaustive (no Idle/Success distinction)
2. No retry — caller must re-implement
3. `ErrorCategory` ignored for writes (no network/auth/server routing)
4. No standard progress overlay or result-handler composable

After this plan, any write ViewModel becomes:

```kotlin
private val submit = viewModelScope.submitHandler<Unit>()
val submitState    = submit.state   // StateFlow<SubmitState<Unit>>

fun onSave(data: FormData) = submit.submit { repository.create(data) }
fun onRetry()              = submit.retry()
fun onDismiss()            = submit.reset()
```

---

## Gap Summary

| Gap | Module | Priority |
|-----|--------|----------|
| F1: `SubmitState` sealed type | core-base/store | P0 |
| F2: `SubmitHandler` + factory | core-base/store | P0 |
| F3: `SubmitStateExtensions` | core-base/store | P1 |
| F4: Tests | core-base/store | P1 |
| UI1: `SubmitProgressOverlay` composable | core-base/ui | P1 |
| UI2: `SubmitResultHandler` composable | core-base/ui | P1 |
| DOC: `STORE_DATA_API.md` submit section | docs | P2 |

---

## Phase 1 — `SubmitState.kt` (core-base/store)

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/SubmitState.kt`

State machine: `Idle → Submitting → Submitted<R>` or `Idle → Submitting → Failed`

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

/**
 * State machine for a single form/action submission lifecycle.
 *
 * Transitions:
 *   Idle       ──submit()──▶  Submitting  ──success──▶  Submitted<R>
 *                                         ──failure──▶  Failed
 *   Submitted / Failed  ──reset()──▶  Idle
 *   Failed              ──retry()──▶  Submitting  (re-runs last block)
 *
 * Analogous to [ScreenState] for reads — one sealed type, zero ad-hoc booleans.
 *
 * @param R The result type produced by a successful submission (use [Unit] for fire-and-forget).
 */
sealed interface SubmitState<out R> {

    /** No submission in flight. Initial state; restored by [SubmitHandler.reset]. */
    data object Idle : SubmitState<Nothing>

    /** API call is executing. Disable submit button, show progress overlay. */
    data object Submitting : SubmitState<Nothing>

    /**
     * API call completed successfully.
     * @param result The value returned by the suspend block.
     */
    data class Submitted<out R>(val result: R) : SubmitState<R>

    /**
     * API call failed. [SubmitHandler.retry] is available.
     * @param error    The original throwable.
     * @param category High-level category for UI routing (Network/Auth/Server/Generic).
     */
    data class Failed(
        val error: Throwable,
        val category: ErrorCategory,
    ) : SubmitState<Nothing>
}
```

---

## Phase 2 — `SubmitHandler.kt` (core-base/store)

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/SubmitHandler.kt`

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

import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * Reusable executor for a single form/action submission lifecycle.
 *
 * Unlike [ScreenDataStream] (continuous Flow), [SubmitHandler] is a one-shot executor:
 * each [submit] call performs one API call and transitions [state] to a terminal state.
 *
 * Usage in ViewModel:
 * ```kotlin
 * private val submit = viewModelScope.submitHandler<ClientId>()
 * val submitState    = submit.state
 *     .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), SubmitState.Idle)
 *
 * fun onSave(form: ClientForm) = submit.submit { repository.createClient(form) }
 * fun onRetry()               = submit.retry()
 * fun onDismiss()             = submit.reset()
 * ```
 */
class SubmitHandler<R> internal constructor(
    private val scope: CoroutineScope,
) {
    private val _state = MutableStateFlow<SubmitState<R>>(SubmitState.Idle)

    /** Observable state. Expose via `.stateIn()` in the ViewModel. */
    val state: StateFlow<SubmitState<R>> = _state.asStateFlow()

    private var lastBlock: (suspend () -> R)? = null
    private var activeJob: Job? = null

    /**
     * Execute [block] as a submission.
     *
     * - No-op if already [SubmitState.Submitting] (idempotent — safe on rapid button taps).
     * - Transitions: any state → Submitting → Submitted | Failed.
     */
    fun submit(block: suspend () -> R) {
        if (_state.value is SubmitState.Submitting) return
        lastBlock = block
        execute(block)
    }

    /**
     * Re-run the last submitted block.
     * No-op if no prior block or currently [SubmitState.Submitting].
     */
    fun retry() {
        val block = lastBlock ?: return
        if (_state.value is SubmitState.Submitting) return
        execute(block)
    }

    /**
     * Return to [SubmitState.Idle]. Call after consuming [SubmitState.Submitted]
     * or [SubmitState.Failed] (e.g. user dismisses error dialog, or after navigating away).
     */
    fun reset() {
        activeJob?.cancel()
        _state.value = SubmitState.Idle
    }

    private fun execute(block: suspend () -> R) {
        activeJob?.cancel()
        _state.value = SubmitState.Submitting
        activeJob = scope.launch {
            _state.value = try {
                SubmitState.Submitted(block())
            } catch (e: CancellationException) {
                throw e  // never swallow cancellation as a failure
            } catch (e: Exception) {
                SubmitState.Failed(
                    error = e,
                    category = categorize(e),
                )
            }
        }
    }
}

/**
 * Creates a [SubmitHandler] bound to this [CoroutineScope] (typically `viewModelScope`).
 *
 * ```kotlin
 * private val submit = viewModelScope.submitHandler<Unit>()
 * ```
 */
fun <R> CoroutineScope.submitHandler(): SubmitHandler<R> = SubmitHandler(this)
```

**Key behaviours:**
- `CancellationException` re-thrown — scope cancellation never appears as `Failed`
- `execute()` cancels any prior active job before starting — no races on rapid re-submit
- `categorize(e)` is the existing top-level function in `ErrorCategory.kt` — no new dep

---

## Phase 3 — `SubmitStateExtensions.kt` (core-base/store)

**File:** `core-base/store/src/commonMain/kotlin/template/core/base/store/SubmitStateExtensions.kt`

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

/** True while the API call is in-flight. Use to disable the submit button. */
val <R> SubmitState<R>.isSubmitting: Boolean
    get() = this is SubmitState.Submitting

/** True when in the initial or post-reset state. */
val <R> SubmitState<R>.isIdle: Boolean
    get() = this is SubmitState.Idle

/** True when the last submission succeeded. */
val <R> SubmitState<R>.isSubmitted: Boolean
    get() = this is SubmitState.Submitted

/** True when the last submission failed. */
val <R> SubmitState<R>.isFailed: Boolean
    get() = this is SubmitState.Failed

/** Returns the result payload, or null for all other states. */
val <R> SubmitState<R>.resultOrNull: R?
    get() = (this as? SubmitState.Submitted)?.result

/** Returns the error, or null for all other states. */
val <R> SubmitState<R>.errorOrNull: Throwable?
    get() = (this as? SubmitState.Failed)?.error

/** Returns the error category, or null for all other states. */
val <R> SubmitState<R>.categoryOrNull: ErrorCategory?
    get() = (this as? SubmitState.Failed)?.category
```

---

## Phase 4 — Tests (core-base/store)

### `SubmitHandlerTest.kt`

**File:** `core-base/store/src/commonTest/kotlin/template/core/base/store/SubmitHandlerTest.kt`

| # | Scenario | Expected |
|---|----------|----------|
| T1 | submit success | `Idle → Submitting → Submitted(result)` |
| T2 | submit failure | `Idle → Submitting → Failed(categorized)` |
| T3 | double-tap while Submitting | second call is no-op (single job) |
| T4 | retry after Failed | `Failed → Submitting → Submitted` |
| T5 | retry with no prior block | no-op, stays in current state |
| T6 | reset from Submitted | returns to `Idle` |
| T7 | reset from Failed | returns to `Idle` |
| T8 | reset while Submitting | cancels job, returns to `Idle` |
| T9 | CancellationException | not caught as `Failed`, propagates |
| T10 | network error | `category == ErrorCategory.Network` |
| T11 | HTTP 401 message | `category == ErrorCategory.Auth` |
| T12 | HTTP 500 message | `category == ErrorCategory.Server` |

Use `runTest` + `StandardTestDispatcher`. No fakes needed — pure coroutines.

### `SubmitStateExtensionsTest.kt`

**File:** `core-base/store/src/commonTest/kotlin/template/core/base/store/SubmitStateExtensionsTest.kt`

Exhaustive property assertions across all 4 states for each extension property.

---

## Phase 5 — UI Composables (core-base/ui)

### `SubmitProgressOverlay.kt`

**File:** `core-base/ui/src/commonMain/kotlin/template/core/base/ui/SubmitProgressOverlay.kt`

```kotlin
/*
 * Copyright 2025 Mifos Initiative — MPL-2.0
 */
package template.core.base.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color

/**
 * Semi-transparent scrim + centered [CircularProgressIndicator] shown while
 * [SubmitState.Submitting]. Render above form content inside a [Box].
 *
 * ```kotlin
 * Box(Modifier.fillMaxSize()) {
 *     FormContent(…)
 *     SubmitProgressOverlay(visible = submitState.isSubmitting)
 * }
 * ```
 */
@Composable
fun SubmitProgressOverlay(
    visible: Boolean,
    modifier: Modifier = Modifier,
    scrimColor: Color = Color.Black.copy(alpha = 0.38f),
) {
    AnimatedVisibility(
        visible = visible,
        enter = fadeIn(),
        exit = fadeOut(),
        modifier = modifier,
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(scrimColor),
            contentAlignment = Alignment.Center,
        ) {
            CircularProgressIndicator()
        }
    }
}
```

### `SubmitResultHandler.kt`

**File:** `core-base/ui/src/commonMain/kotlin/template/core/base/ui/SubmitResultHandler.kt`

```kotlin
/*
 * Copyright 2025 Mifos Initiative — MPL-2.0
 */
package template.core.base.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import template.core.base.store.ErrorCategory
import template.core.base.store.SubmitState

/**
 * Side-effect composable that fires callbacks when [state] reaches a terminal state.
 *
 * - [onSubmitted] fires once on [SubmitState.Submitted].
 * - [onFailed] fires once on [SubmitState.Failed].
 *
 * Call [SubmitHandler.reset] inside the callback to return to [SubmitState.Idle]
 * so the handler can be used again.
 *
 * ```kotlin
 * SubmitResultHandler(
 *     state = submitState,
 *     onSubmitted = { onNavigateBack() },
 *     onFailed = { error, category ->
 *         when (category) {
 *             ErrorCategory.Network -> showNoNetworkSheet()
 *             ErrorCategory.Auth    -> onNavigateToLogin()
 *             else                  -> showErrorDialog(error.message)
 *         }
 *         viewModel.onDismiss()   // calls submit.reset()
 *     },
 * )
 * ```
 *
 * Uses [LaunchedEffect] keyed on [state] — fires exactly once per terminal state transition.
 * Works correctly because [SubmitState.Submitted] and [SubmitState.Failed] are data classes
 * with distinct structural equality.
 */
@Composable
fun <R> SubmitResultHandler(
    state: SubmitState<R>,
    onSubmitted: (result: R) -> Unit,
    onFailed: ((error: Throwable, category: ErrorCategory) -> Unit)? = null,
) {
    LaunchedEffect(state) {
        when (state) {
            is SubmitState.Submitted -> onSubmitted(state.result)
            is SubmitState.Failed    -> onFailed?.invoke(state.error, state.category)
            else                     -> Unit
        }
    }
}
```

---

## Phase 6 — Doc Update (`STORE_DATA_API.md`)

Add after the "UX Scenario Matrix" section:

````markdown
## Form / Submit

### State machine

```
Idle  ──submit()──▶  Submitting  ──success──▶  Submitted<R>
                                 ──failure──▶  Failed(error, category)
Submitted / Failed  ──reset()──▶  Idle
Failed              ──retry()──▶  Submitting
```

### ViewModel

```kotlin
private val submit = viewModelScope.submitHandler<Unit>()
val submitState    = submit.state
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), SubmitState.Idle)

fun onSave(data: FormData) = submit.submit { repository.create(data) }
fun onRetry()              = submit.retry()
fun onDismiss()            = submit.reset()
```

### Screen

```kotlin
Box(Modifier.fillMaxSize()) {
    FormContent(
        enabled = !submitState.isSubmitting,
        onSubmit = { viewModel.onSave(it) },
    )
    SubmitProgressOverlay(visible = submitState.isSubmitting)
    SubmitResultHandler(
        state = submitState,
        onSubmitted = { onNavigateBack() },
        onFailed = { error, category ->
            viewModel.onDismiss()
            when (category) {
                ErrorCategory.Network -> showNoNetworkSheet()
                ErrorCategory.Auth    -> onNavigateToLogin()
                else                  -> showErrorDialog(error.message)
            }
        },
    )
}
```
````

Update module structure table to add the 3 new `core-base/store` files.

---

## File Checklist

### `core-base/store` — 5 new files

| File | Phase | Est. lines |
|------|-------|-----------|
| `SubmitState.kt` | 1 | ~50 |
| `SubmitHandler.kt` | 2 | ~85 |
| `SubmitStateExtensions.kt` | 3 | ~35 |
| `SubmitHandlerTest.kt` | 4 | ~150 |
| `SubmitStateExtensionsTest.kt` | 4 | ~80 |

### `core-base/ui` — 2 new files

| File | Phase | Est. lines |
|------|-------|-----------|
| `SubmitProgressOverlay.kt` | 5 | ~45 |
| `SubmitResultHandler.kt` | 5 | ~55 |

### `docs` — 1 update

| File | Change |
|------|--------|
| `STORE_DATA_API.md` | Add submit section + update module structure |

**Total: 5 new source files, 2 new test files, 1 doc update**

---

## Dependency Graph

```
Phase 1: SubmitState         ←── ErrorCategory (existing)
Phase 2: SubmitHandler       ←── SubmitState, categorize() (existing)
Phase 3: SubmitStateExts     ←── SubmitState
Phase 4: Tests               ←── SubmitHandler, SubmitStateExtensions
Phase 5: UI composables      ←── SubmitState (cross-module import)
Phase 6: Doc                 ←── all phases complete
```

No circular deps. Phases are strictly ordered and independently compilable.

---

## UX Scenario Matrix

| Scenario | SubmitState | UI behaviour |
|----------|-------------|-------------|
| Form idle, not yet submitted | `Idle` | Button enabled |
| User taps Submit | `Submitting` | Button disabled + scrim overlay |
| API succeeds | `Submitted(result)` | Navigate / toast (via `SubmitResultHandler`) |
| API fails (network) | `Failed(Network)` | No-network bottom sheet |
| API fails (auth) | `Failed(Auth)` | Navigate to login |
| API fails (server/generic) | `Failed(Server/Generic)` | Error dialog + retry button |
| User taps Retry | `Submitting` again | Same overlay appears |
| User dismisses error | `Idle` (via reset) | Dialog hidden |

---

## Execution Log

| Phase | Status | Notes |
|-------|--------|-------|
| 1. SubmitState | ✅ Done | SubmitState.kt — 54 lines |
| 2. SubmitHandler | ✅ Done | SubmitHandler.kt — 125 lines |
| 3. SubmitStateExtensions | ✅ Done | SubmitStateExtensions.kt — 47 lines |
| 4. Tests | ✅ Done | SubmitHandlerTest.kt (220L), SubmitStateExtensionsTest.kt (128L) |
| 5. UI composables | ✅ Done | SubmitProgressOverlay.kt (83L), SubmitResultHandler.kt (67L) |
| 6. Doc update | ✅ Done | STORE_DATA_API.md — module structure + Submit section |

---

## What's Next

```
Run: /gap-implement-project plan current
```
