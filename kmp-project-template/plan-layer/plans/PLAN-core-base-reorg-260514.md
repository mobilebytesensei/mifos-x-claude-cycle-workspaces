# Implementation Plan: core-base/store + core-base/ui Sub-Package Re-organisation + Mutation Screen Pattern

## Metadata

| Field | Value |
|---|---|
| Plan ID | PLAN-core-base-reorg-260514 |
| Generated | 2026-05-14 |
| Status | Completed |
| Scope | framework — core-base/store + core-base/ui |
| Type | Refactor (package re-org) + New Features (mutation screen pattern gaps) |
| Branch | `feat/core-base-reorg-260514` from `origin/dev` |
| Target PR | `openMF/kmp-project-template` base `dev` |

---

## Part A — Re-organisation (Phases 1–6)

Both `core-base/store` and `core-base/ui` have grown to 18–23 production files in a
single flat package. Three distinct concerns (screen/detail read, paging/list read,
submit/write) plus infrastructure all live at the same level with no structural signal
to guide consumers.

### Target Structure

#### core-base/store → `template.core.base.store.*`

| Sub-package | Files |
|---|---|
| `screen` | `ScreenState`, `ScreenStateExtensions`, `ScreenDataStream`, `StoreData`, `StoreDataExtensions`, `StoreDataMapper`, `StoreResponseMapper` |
| `paging` | `PagingScreenStream`, `StorePagingSource` |
| `submit` | `SubmitState`, `SubmitHandler`, `SubmitStateExtensions` |
| `error` | `ErrorCategory`, `OfflineException` |
| `infra` | `StoreFactory`, `StoreRegistry`, `InMemoryBookkeeper`, `FetchedAtRepository`, `DecisionEngine`, `DefaultValidator` |
| `di` | `StoreModule` (**already a sub-package — no file move**) |

> `DataFreshness` enum lives in `ScreenState.kt` → moves with it to `screen/`.  
> `PageKey` type → moves to `paging/`.  
> Top-level extension functions (`categorize`, `asScreenStream`, `asPagingScreenStream`,
> `combineContent`, `emptyIfContent`) move with their home file.

#### core-base/ui → `template.core.base.ui.*`

| Sub-package | Files (commonMain unless noted) |
|---|---|
| `screen` | `ScreenContent`, `ScreenStateDefaults`, `DataFreshnessIndicator` |
| `paging` | `PagingScreenContent`, `LoadMoreFooter`, `LoadMoreTrigger` |
| `submit` | `SubmitProgressOverlay`, `SubmitResultHandler` |
| `viewmodel` | `BaseViewModel`, `BackgroundEvent` |
| `effects` | `EventsEffect`, `LifecycleEventEffect`, `ReportDrawnExt` (+ `.android.kt`, `.jvmJs.kt`) |
| `nav` | `NavGraphBuilderExtensions` |
| `util` | `ImageLoaderExt`, `JankStatsExtension` (+ android/jvmJs variants), `SharedElementExt`, `ShareUtils` (+ android/native/desktop/jsCommon variants), `StringExt`, `Transition` |

---

### Consumer Impact Map

#### core-base/store consumers (28 files)

| Module | File | Types imported |
|---|---|---|
| `core-base/ui` | `ScreenContent.kt` | `DataFreshness`, `ScreenState` |
| `core-base/ui` | `PagingScreenContent.kt` | `DataFreshness`, `PagingScreenStream`, `ScreenState` |
| `core-base/ui` | `LoadMoreFooter.kt` | `ErrorCategory`, `PagingScreenStream`, `categorize` |
| `core-base/ui` | `DataFreshnessIndicator.kt` | `DataFreshness` |
| `core-base/ui` | `ScreenStateDefaults.kt` | `ErrorCategory`, `categorize` |
| `core-base/ui` | `SubmitProgressOverlay.kt` | `SubmitState` |
| `core-base/ui` | `SubmitResultHandler.kt` | `SubmitState`, `ErrorCategory` |
| `core-base/ui` (test) | `DataFreshnessIndicatorStateTest.kt` | `DataFreshness` |
| `core-base/ui` (test) | `LoadMoreFooterCopyTest.kt` | `OfflineException` |
| `core/store` | `AppErrorMapper.kt` | `ErrorCategory`, `categorize` |
| `core/store` | `AppStoreRegistry.kt` | `StoreRegistry` |
| `core/ui` | `KptPullToRefreshState.kt` | `DataFreshness`, `PagingScreenStream`, `ScreenDataStream`, `ScreenState` |
| `core/data` | `RateHistoryStore.kt` | `DefaultValidator`, `StoreFactory` |
| `core/data` | `CoinDetailStore.kt` | `DefaultValidator`, `StoreFactory` |
| `core/data` | `ExchangeRatesStore.kt` | `DefaultValidator`, `StoreFactory` |
| `core/data` | `CoinMarketsStore.kt` | `DefaultValidator`, `PageKey`, `StoreFactory` |
| `core/data` | `RepositoryModule.kt` | `FetchedAtRepository` |
| `core/data` | `RoomFetchedAtRepository.kt` | `FetchedAtRepository` |
| `core/data` | `CryptoRepositoryImpl.kt` | `FetchedAtRepository`, `PageKey`, `PagingScreenStream`, `ScreenDataStream`, `asPagingScreenStream`, `asScreenStream` |
| `core/data` | `ApplicationStoreRegistry.kt` | `StoreRegistry` |
| `core/data` | `StoreCacheManagerImpl.kt` | `PageKey` |
| `core/data` | `CurrencyRepositoryImpl.kt` | `FetchedAtRepository`, `ScreenDataStream`, `asScreenStream` |
| `core/data` | `CryptoRepository.kt` | `PagingScreenStream`, `ScreenDataStream` |
| `core/data` | `CurrencyRepository.kt` | `ScreenDataStream` |
| `feature/crypto` | `CryptoWatchlistViewModel.kt` | `PagingScreenStream` |
| `feature/crypto` | `CoinDetailViewModel.kt` | `ScreenState` |
| `feature/currency-rates` | `CurrencyRatesViewModel.kt` | `ScreenState`, `combineContent`, `emptyIfContent` |
| `feature/currency-rates` | `RateHistoryViewModel.kt` | `ScreenState` |

#### core-base/ui consumers (27 files)

| Module | File | Types imported |
|---|---|---|
| `core/store` | `AppScreenStateDefaults.kt` | `ScreenStateDefaults`, `ScreenStateEmpty`, `ScreenStateError`, `ScreenStateLoading`, `ScreenStateNoNetwork` |
| `core/designsystem` | `Theme.kt` | `LocalScreenStateDefaults` |
| `cmp-android` | `AndroidApp.kt` | `getDefaultImageLoader` |
| `cmp-android` | `MainActivity.kt` | `ShareUtils` |
| `cmp-shared` | `SharedApp.kt` | `LocalImageLoaderProvider`, `getDefaultImageLoader` |
| `cmp-navigation` | `AppViewModel.kt` | `BaseViewModel` |
| `cmp-navigation` | `ComposeApp.kt` | `EventsEffect` |
| `cmp-navigation` | `RootNavViewModel.kt` | `BaseViewModel` |
| `cmp-navigation` | `RootNavScreen.kt` | `NonNullEnterTransitionProvider`, `NonNullExitTransitionProvider`, `RootTransitionProviders` |
| `cmp-navigation` | `AuthenticatedNavbarNavigationViewModel.kt` | `BaseViewModel` |
| `cmp-navigation` | `AuthenticatedNavbarNavigationScreen.kt` | `EventsEffect`, `RootTransitionProviders` |
| `cmp-navigation` | `AuthenticatedNavbarNavigation.kt` | `composableWithStayTransitions` |
| `feature/crypto` | `CryptoNavigation.kt` | `composableWithPushTransitions` |
| `feature/crypto` | `CryptoWatchlistScreen.kt` | `PagingScreenContent` |
| `feature/crypto` | `CryptoWatchlistViewModel.kt` | `BaseViewModel` |
| `feature/crypto` | `CoinDetailScreen.kt` | `ScreenContent` |
| `feature/crypto` | `CoinDetailViewModel.kt` | `BaseViewModel` |
| `feature/currency-rates` | `CurrencyRatesNavigation.kt` | `composableWithPushTransitions` |
| `feature/currency-rates` | `CurrencyRatesViewModel.kt` | `BaseViewModel` |
| `feature/currency-rates` | `CurrencyRatesScreen.kt` | `ScreenContent` |
| `feature/currency-rates` | `RateHistoryScreen.kt` | `ScreenContent` |
| `feature/currency-rates` | `RateHistoryViewModel.kt` | `BaseViewModel` |
| `feature/emi-calculator` | `EmiCalculatorNavigation.kt` | `composableWithPushTransitions` |
| `feature/emi-calculator` | `EmiCalculatorViewModel.kt` | `BaseViewModel` |
| `feature/home` | `HomeDestination.kt` | `composableWithStayTransitions` |
| `feature/profile` | `ProfileRoute.kt` | `composableWithStayTransitions` |
| `feature/settings` | `SettingsRoute.kt` | `composableWithPushTransitions` |

---

### Phase 1 — core-base/store: move files + update package declarations (18 files)

For each file: create sub-directory, move file, change `package template.core.base.store`
→ `package template.core.base.store.<sub>`, update any cross-references within the module.

```
store/src/commonMain/kotlin/template/core/base/store/
  screen/
    ScreenState.kt           (was root)
    ScreenStateExtensions.kt (was root)
    ScreenDataStream.kt      (was root)
    StoreData.kt             (was root)
    StoreDataExtensions.kt   (was root)
    StoreDataMapper.kt       (was root)
    StoreResponseMapper.kt   (was root)
  paging/
    PagingScreenStream.kt    (was root)
    StorePagingSource.kt     (was root)
  submit/
    SubmitState.kt           (was root)
    SubmitHandler.kt         (was root)
    SubmitStateExtensions.kt (was root)
  error/
    ErrorCategory.kt         (was root)
    OfflineException.kt      (was root)
  infra/
    StoreFactory.kt          (was root)
    StoreRegistry.kt         (was root)
    InMemoryBookkeeper.kt    (was root)
    FetchedAtRepository.kt   (was root)
    DecisionEngine.kt        (was root)
    DefaultValidator.kt      (was root)
  di/
    StoreModule.kt           (no move — update imports only)
```

### Phase 2 — core-base/store: update test package declarations (12 test files)

Update `package` declaration only. Files stay in their current `commonTest/` directories.

| Test file | New package |
|---|---|
| `ScreenStateExtensionsTest.kt` | `template.core.base.store.screen` |
| `StoreDataMapperTest.kt` | `template.core.base.store.screen` |
| `StorePagingSourceTest.kt` | `template.core.base.store.paging` |
| `PagingScreenStreamDecisionParityTest.kt` | `template.core.base.store.paging` |
| `PagingScreenStreamOfflineTest.kt` | `template.core.base.store.paging` |
| `LoadPageRefreshSemanticsTest.kt` | `template.core.base.store.paging` |
| `SubmitHandlerTest.kt` | `template.core.base.store.submit` |
| `SubmitStateExtensionsTest.kt` | `template.core.base.store.submit` |
| `ErrorCategoryTest.kt` | `template.core.base.store.error` |
| `DecisionEngineTest.kt` | `template.core.base.store.infra` |
| `DefaultValidatorTest.kt` | `template.core.base.store.infra` |
| `FakeFetchedAtRepository.kt` + `FakeFetchedAtRepositoryTest.kt` | `template.core.base.store.infra` |

### Phase 3 — core-base/ui: move files + update package declarations (25 files)

```
ui/src/commonMain/kotlin/template/core/base/ui/
  screen/
    ScreenContent.kt
    ScreenStateDefaults.kt
    DataFreshnessIndicator.kt
  paging/
    PagingScreenContent.kt
    LoadMoreFooter.kt
    LoadMoreTrigger.kt
  submit/
    SubmitProgressOverlay.kt
    SubmitResultHandler.kt
  viewmodel/
    BaseViewModel.kt
    BackgroundEvent.kt
  effects/
    EventsEffect.kt
    LifecycleEventEffect.kt
    ReportDrawnExt.kt
  nav/
    NavGraphBuilderExtensions.kt
  util/
    ImageLoaderExt.kt
    JankStatsExtension.kt
    SharedElementExt.kt
    ShareUtils.kt
    StringExt.kt
    Transition.kt

# Platform-specific source sets — same sub-package, mirrored directory
ui/src/androidMain/kotlin/template/core/base/ui/util/
    JankStatsExtensions.kt
    ShareUtils.android.kt
ui/src/androidMain/kotlin/template/core/base/ui/effects/
    ReportDrawnExt.android.kt
ui/src/nativeMain/kotlin/template/core/base/ui/util/
    ShareUtils.native.kt
ui/src/desktopMain/java/template/core/base/ui/util/
    ShareUtils.desktop.kt
ui/src/jsCommonMain/kotlin/template/core/base/ui/util/
    ShareUtils.kt
ui/src/nonAndroidMain/kotlin/template/core/base/ui/util/
    JankStatsExtension.jvmJs.kt
ui/src/nonAndroidMain/kotlin/template/core/base/ui/effects/
    ReportDrawnExt.jvmJs.kt
```

### Phase 4 — core-base/ui: update test package declarations (4 test files)

| Test file | New package |
|---|---|
| `ScreenStateDefaultsTest.kt` | `template.core.base.ui.screen` |
| `DataFreshnessIndicatorStateTest.kt` | `template.core.base.ui.screen` |
| `DataFreshnessTextTest.kt` | `template.core.base.ui.screen` |
| `LoadMoreFooterCopyTest.kt` | `template.core.base.ui.paging` |

### Phase 5 — Update all consumer imports (55 files)

Mechanical `import` line updates only. Group by module for a single compile/verify pass:

1. `core-base/ui` internal (7 production + 2 test files) — store imports
2. `core-base/store` internal — `di/StoreModule.kt` (imports from infra/error/screen)
3. `core/store` (2 files) — store + ui imports
4. `core/ui` (1 file) — store imports
5. `core/data` (12 files) — store imports
6. `core/designsystem` (1 file) — ui imports
7. `cmp-android` (2 files) — ui imports
8. `cmp-shared` (1 file) — ui imports
9. `cmp-navigation` (7 files) — ui imports
10. `feature/crypto` (5 files) — store + ui imports
11. `feature/currency-rates` (5 files) — store + ui imports
12. `feature/emi-calculator` (2 files) — ui imports
13. `feature/home` (1 file) — ui imports
14. `feature/profile` (1 file) — ui imports
15. `feature/settings` (1 file) — ui imports

### Phase 6 — Verify re-org compiles

```bash
./gradlew :core-base:store:allTests
./gradlew :core-base:ui:allTests
./gradlew :core:store:compileCommonMainKotlinMetadata
./gradlew :core:data:compileCommonMainKotlinMetadata
./gradlew :feature:crypto:compileCommonMainKotlinMetadata
./gradlew :feature:currency-rates:compileCommonMainKotlinMetadata
./gradlew spotlessCheck detekt
```

---

## Part B — Mutation Screen Pattern Gaps (Phases 7–12)

End-to-end gap analysis of `ScreenDataStream (load) + SubmitHandler (write)` combined
in a ViewModel identified 8 gaps across store, UI, and test layers.

### Gap Summary

| # | Gap | Severity | Phase |
|---|---|---|---|
| 1 | No `asLoadOnceStream()` — stream stops after first Content (edit-mode safety) | **High** | 7 |
| 2 | No `submitWhenContent` guard — semantic coupling of submit to loaded state | Medium | 8 |
| 3 | No `canInteract` — combined ScreenState + SubmitState derived boolean | Medium | 8 |
| 4 | No `MutationUiState<T,R>` — single wrapper collapsing both StateFlows | Medium | 9 |
| 5 | `ScreenContent` content lambda has no `isSubmitting` thread | Medium | 10 (via MutationScreenContent) |
| 6 | No `SubmitButton` — self-disabling button with inline progress | **High** | 11 |
| 7 | No `MutationScreenContent` — combined ScreenContent + overlay + result handler | **High** | 10 |
| 8 | No `FakeScreenDataStream` + combined-VM test helpers | Medium | 12 |

---

### Phase 7 — `asLoadOnceStream()` in `store.screen` (Gap 1)

**File:** `store/src/commonMain/kotlin/template/core/base/store/screen/LoadOnceStream.kt`

**Problem:** `ScreenDataStream` continuously re-emits on Store refreshes. An edit screen
using it will silently reset in-progress user edits when a background refresh arrives.

**Solution:** New extension + wrapper that captures the first `Content` emission and
stops tracking the Store, preserving the snapshot for the edit session.

```kotlin
/**
 * Load-once variant of [asScreenStream] for edit/mutation screens.
 *
 * Transitions: Loading → Content(initialData) — then stops. Further Store updates
 * are ignored so in-progress user edits are never overwritten by background refreshes.
 * Error / NoNetwork states still propagate (user can retry to reach Content).
 */
fun <Key : Any, Output : Any> Store<Key, Output>.asLoadOnceStream(
    key: Key,
    networkMonitor: NetworkMonitor,
    scope: CoroutineScope,
): ScreenDataStream<Output>
```

**Tests:** `LoadOnceStreamTest` — verify second Store emission is swallowed after first
Content, Error still propagates before Content arrives, retry reaches Content.

---

### Phase 8 — ScreenState + SubmitHandler coordination helpers (Gaps 2 + 3)

**File:** `store/src/commonMain/kotlin/template/core/base/store/screen/ScreenStateExtensions.kt`
(add to existing file post re-org)

**Gap 2 — `submitWhenContent` guard**

```kotlin
/**
 * Execute [block] only when [screenState] has loaded content.
 * No-op (and safe to call) when state is Loading / Error / NoNetwork / Empty.
 * Guards against premature submits before data arrives.
 */
fun <T, R> SubmitHandler<R>.submitWhenContent(
    screenState: ScreenState<T>,
    block: suspend (data: T) -> R,
) {
    val data = screenState.dataOrNull ?: return
    submit { block(data) }
}
```

**Gap 3 — `canInteract`**

```kotlin
/**
 * True when the screen has content available AND [submitState] is not in-flight.
 * Use to enable/disable a submit button: `enabled = screenState.canInteract(submitState)`.
 */
fun <T, R> ScreenState<T>.canInteract(submitState: SubmitState<R>): Boolean =
    hasContent && !submitState.isSubmitting
```

**Tests:** `ScreenStateMutationExtensionsTest` — 6 cases covering all state combinations.

---

### Phase 9 — `MutationUiState<T, R>` combined wrapper (Gap 4)

**File:** `store/src/commonMain/kotlin/template/core/base/store/submit/MutationUiState.kt`

**Problem:** Edit-screen ViewModels expose two independent StateFlows. The Screen collects
both separately, making the relationship between them implicit and harder to test.

```kotlin
/**
 * Combined state for screens that load data then allow mutation.
 *
 * Collapse two StateFlows into one in the ViewModel:
 * ```kotlin
 * val uiState: StateFlow<MutationUiState<Data, Result>> = combine(
 *     screenState, submitState, ::MutationUiState
 * ).stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), MutationUiState())
 * ```
 */
data class MutationUiState<out T, out R>(
    val screen: ScreenState<T> = ScreenState.Loading,
    val submit: SubmitState<R> = SubmitState.Idle,
) {
    val canInteract: Boolean get() = screen.hasContent && !submit.isSubmitting
    val isSubmitting: Boolean get() = submit.isSubmitting
    val dataOrNull: T? get() = screen.dataOrNull
}
```

**Tests:** `MutationUiStateTest` — `canInteract` truth table across all state combinations.

---

### Phase 10 — `MutationScreenContent` composable (Gaps 5 + 7)

**File:** `ui/src/commonMain/kotlin/template/core/base/ui/submit/MutationScreenContent.kt`

**Problem:** Every edit screen manually assembles `Box { ScreenContent + SubmitProgressOverlay + SubmitResultHandler }`.
Addresses Gap 5 by threading `isSubmitting` through the content lambda signature.

```kotlin
/**
 * Composable for screens that load data then submit a mutation.
 *
 * Bundles:
 * - [ScreenContent] for the load phase (Loading / Error / NoNetwork / Content)
 * - [SubmitProgressOverlay] over the content while submitting
 * - [SubmitResultHandler] for terminal-state side effects
 *
 * The [content] lambda receives both the loaded [data] and [isSubmitting] so
 * form fields can disable themselves without a separate collect.
 *
 * ```kotlin
 * MutationScreenContent(
 *     screenState  = uiState.screen,
 *     submitState  = uiState.submit,
 *     onRetry      = vm::onRetry,
 *     onSubmitted  = { result -> onNavigateBack() },
 *     onFailed     = { _, _ -> vm.onDismiss() },
 * ) { data, isSubmitting ->
 *     ClientForm(data = data, enabled = !isSubmitting, onSave = vm::onSave)
 * }
 * ```
 */
@Composable
fun <T, R> MutationScreenContent(
    screenState: ScreenState<T>,
    submitState: SubmitState<R>,
    onRetry: () -> Unit,
    onSubmitted: (result: R) -> Unit,
    modifier: Modifier = Modifier,
    onFailed: ((error: Throwable, category: ErrorCategory) -> Unit)? = null,
    content: @Composable (data: T, isSubmitting: Boolean) -> Unit,
)
```

**`MutationUiState<T,R>` overload:**
```kotlin
@Composable
fun <T, R> MutationScreenContent(
    state: MutationUiState<T, R>,
    onRetry: () -> Unit,
    onSubmitted: (result: R) -> Unit,
    modifier: Modifier = Modifier,
    onFailed: ((error: Throwable, category: ErrorCategory) -> Unit)? = null,
    content: @Composable (data: T, isSubmitting: Boolean) -> Unit,
)
```

**Tests:** Compose UI test — Loading renders spinner, Content renders form with isSubmitting=false,
Submitting renders form with isSubmitting=true + overlay visible, terminal states fire callbacks.

---

### Phase 11 — `SubmitButton` composable (Gap 6)

**File:** `ui/src/commonMain/kotlin/template/core/base/ui/submit/SubmitButton.kt`

**Problem:** Every form screen writes a Button that self-disables, swaps label ↔ progress
indicator, and re-enables on failure. Identical boilerplate on every screen today.

```kotlin
/**
 * A [Button] that automatically reflects [SubmitState]:
 * - Idle / Failed  → shows [text], enabled
 * - Submitting     → shows inline [CircularProgressIndicator], disabled
 * - Submitted      → disabled (navigation/reset is caller's responsibility)
 *
 * ```kotlin
 * SubmitButton(
 *     state   = submitState,
 *     text    = "Save Client",
 *     onClick = { vm.onSave(form) },
 * )
 * ```
 */
@Composable
fun <R> SubmitButton(
    state: SubmitState<R>,
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,               // caller can add extra guard (e.g., form valid)
)

/** Boolean overload for callers already holding `submitState.isSubmitting`. */
@Composable
fun SubmitButton(
    isSubmitting: Boolean,
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
)
```

**Tests:** `SubmitButtonStateTest` — enabled/disabled semantics for each SubmitState variant.

---

### Phase 12 — Test helpers: `FakeScreenDataStream` + combined-VM fixtures (Gap 8)

**File:** `store/src/commonTest/kotlin/template/core/base/store/screen/FakeScreenDataStream.kt`

**Problem:** Testing a ViewModel that owns both `ScreenDataStream` and `SubmitHandler`
requires controlled emission of `ScreenState` sequences with no real Store/network.

```kotlin
/**
 * Test double for [ScreenDataStream]. Emits states programmatically.
 *
 * ```kotlin
 * val fakeStream = FakeScreenDataStream<ClientDetail>()
 * fakeStream.emit(ScreenState.Loading)
 * fakeStream.emit(ScreenState.Content(client, DataFreshness.FRESH))
 * ```
 */
class FakeScreenDataStream<T> : ScreenDataStream<T>(
    state = MutableSharedFlow<ScreenState<T>>().also { _flow = it },
    refreshTrigger = MutableSharedFlow(),
) {
    suspend fun emit(state: ScreenState<T>)
    fun tryEmit(state: ScreenState<T>)
    val refreshCount: Int
}
```

**Combined-VM fixture pattern documented in KDoc** — shows how to test:
1. Submit is blocked while `ScreenState.Loading`
2. Background stream refresh during `SubmitState.Submitting` doesn't corrupt state
3. `submitWhenContent` fires only after `Content` arrives

**Tests:** `FakeScreenDataStreamTest` — verifies the fake itself behaves like the real stream.

---

## Naming Convention Reference (canonical after re-org)

| Concern | Store package | UI package |
|---|---|---|
| Detail / single read | `store.screen.*` | `ui.screen.*` |
| Paginated list | `store.paging.*` | `ui.paging.*` |
| Single-step write | `store.submit.*` | `ui.submit.*` |
| Load-once (edit mode) | `store.screen.asLoadOnceStream` | — |
| Combined mutation state | `store.submit.MutationUiState` | — |
| Mutation coordination | `store.screen.canInteract`, `submitWhenContent` | — |
| Error classification | `store.error.*` | — |
| Infrastructure | `store.infra.*` | — |
| ViewModel base | — | `ui.viewmodel.*` |
| Lifecycle effects | — | `ui.effects.*` |
| Navigation helpers | — | `ui.nav.*` |
| Utilities | — | `ui.util.*` |
| Mutation screen shell | — | `ui.submit.MutationScreenContent` |
| Mutation submit button | — | `ui.submit.SubmitButton` |

**Edit screen pattern** (load data → edit → submit → navigate):
- ViewModel: `store.asLoadOnceStream()` + `submitHandler()` → expose `MutationUiState`
- Screen: `MutationScreenContent(state, onRetry, onSubmitted) { data, isSubmitting → … }`
- Button: `SubmitButton(state = uiState.submit, text = "Save", onClick = vm::onSave)`

**Create screen pattern** (no pre-load, just submit):
- ViewModel: `submitHandler()` only — `ScreenDataStream` not needed
- Screen: `Box { FormBody() + SubmitProgressOverlay(state) + SubmitResultHandler(...) }`
- Or: `SubmitButton` + `SubmitResultHandler` inline

---

## Execution Log

| Phase | Status | Notes |
|---|---|---|
| 1 — store file moves | ✅ Done | |
| 2 — store test package updates | ✅ Done | |
| 3 — ui file moves | ✅ Done | |
| 4 — ui test package updates | ✅ Done | |
| 5 — consumer import updates | ✅ Done | |
| 6 — verify re-org | ✅ Done | tests pass on Android JVM | |
| 7 — `asLoadOnceStream()` + tests | ✅ Done | `store.screen.LoadOnceStream.kt` + `LoadOnceStreamTest.kt` |
| 8 — `submitWhenContent` + `canInteract` + tests | ⬜ Todo | `store.screen` — extend ScreenStateExtensions |
| 9 — `MutationUiState<T,R>` + tests | ⬜ Todo | `store.submit` — new file |
| 10 — `MutationScreenContent` + tests | ⬜ Todo | `ui.submit` — new file, 2 overloads |
| 11 — `SubmitButton` + tests | ⬜ Todo | `ui.submit` — new file, 2 overloads |
| 12 — `FakeScreenDataStream` + combined-VM tests | ✅ Done | `FakeScreenDataStream.kt` + `FakeScreenDataStreamTest.kt`; yield() fix for SharedFlow replay |

---

## What's Next

```
Run: /gap-implement-project plan PLAN-core-base-reorg-260514
```
