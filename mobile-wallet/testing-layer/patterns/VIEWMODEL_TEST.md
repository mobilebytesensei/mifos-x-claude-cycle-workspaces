# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/testing-layer/patterns/VIEWMODEL_TEST.md"
# last_modified: "2026-03-19"

# ViewModel Test Pattern

> Detailed instructions for testing ViewModels

---

## Overview

ViewModel tests verify:
- State transitions (Loading -> Success/Error)
- Action handling (user interactions)
- Event emission (navigation, dialogs)
- Business logic correctness

---

## File Location

```
feature/${feature}/src/commonTest/kotlin/org/mifos/mobile/feature/${feature}/${Feature}ViewModelTest.kt
```

---

## Dependencies

```kotlin
// build.gradle.kts
kotlin {
    sourceSets {
        commonTest.dependencies {
            implementation(kotlin("test"))
            implementation(libs.kotlinx.coroutines.test)
            implementation(libs.turbine)  // Flow testing (for eventFlow only)
        }
    }
}
```

---

## Test Structure

```kotlin
class ${Feature}ViewModelTest {
    // ===============================================================
    // SETUP
    // ===============================================================

    private val testDispatcher = StandardTestDispatcher()

    private lateinit var viewModel: ${Feature}ViewModel
    private lateinit var fakeRepository: Fake${Feature}Repository

    @BeforeTest
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        fakeRepository = Fake${Feature}Repository()
        viewModel = ${Feature}ViewModel(
            repository = fakeRepository
        )
    }

    @AfterTest
    fun tearDown() {
        Dispatchers.resetMain()
    }

    // ===============================================================
    // INITIAL STATE TESTS
    // ===============================================================

    @Test
    fun givenNewViewModel_whenCreated_thenInitialStateIsLoading() {
        assertEquals(
            ${Feature}ScreenState.Loading,
            viewModel.stateFlow.value.uiState
        )
    }

    // ===============================================================
    // SUCCESS STATE TESTS
    // ===============================================================

    @Test
    fun givenSuccessResponse_whenDataLoaded_thenStateIsSuccess() = runTest {
        val testData = ${Feature}Fixtures.createList(5)
        fakeRepository.setItems(testData)

        advanceUntilIdle()

        assertEquals(
            ${Feature}ScreenState.Success,
            viewModel.stateFlow.value.uiState
        )
        assertEquals(testData, viewModel.stateFlow.value.items)
    }

    @Test
    fun givenEmptyResponse_whenDataLoaded_thenStateIsEmpty() = runTest {
        fakeRepository.setItems(emptyList())

        advanceUntilIdle()

        assertEquals(
            ${Feature}ScreenState.Empty,
            viewModel.stateFlow.value.uiState
        )
    }

    // ===============================================================
    // ERROR STATE TESTS
    // ===============================================================

    @Test
    fun givenErrorResponse_whenDataLoaded_thenStateIsError() = runTest {
        fakeRepository.setShouldFail(true)

        advanceUntilIdle()

        assertIs<${Feature}ScreenState.Error>(viewModel.stateFlow.value.uiState)
    }

    // ===============================================================
    // ACTION TESTS
    // ===============================================================

    @Test
    fun givenLoadedData_whenRefreshAction_thenReloadsData() = runTest {
        fakeRepository.setItems(listOf(testItem))
        advanceUntilIdle()

        viewModel.trySendAction(${Feature}Action.OnRefresh)
        advanceUntilIdle()

        assertEquals(
            ${Feature}ScreenState.Success,
            viewModel.stateFlow.value.uiState
        )
    }

    // ===============================================================
    // EVENT TESTS (use Turbine for eventFlow only)
    // ===============================================================

    @Test
    fun givenItem_whenItemClicked_thenNavigationEventEmitted() = runTest {
        viewModel.trySendAction(${Feature}Action.OnItemClick(id = 1L))
        advanceUntilIdle()

        viewModel.eventFlow.test {
            assertEquals(${Feature}Event.NavigateToDetail(1L), awaitItem())
        }
    }

    // ===============================================================
    // DIALOG TESTS
    // ===============================================================

    @Test
    fun givenDialogVisible_whenDismissed_thenDialogStateIsNull() = runTest {
        viewModel.trySendAction(${Feature}Action.OnDismissDialog)
        advanceUntilIdle()

        assertNull(viewModel.stateFlow.value.dialogState)
    }
}
```

---

## Test Categories

### 1. Initial State Tests

Verify the ViewModel starts with correct default state.

```kotlin
@Test
fun givenNewViewModel_whenCreated_thenHasDefaultState() {
    assertEquals(${Feature}ScreenState.Loading, viewModel.stateFlow.value.uiState)
    assertNull(viewModel.stateFlow.value.dialogState)
}
```

### 2. Data Loading Tests

Test success, error, and empty scenarios.

```kotlin
@Test
fun givenPaginatedData_whenLoadMore_thenAppendsData() = runTest {
    fakeRepository.setItems(page1Data)
    advanceUntilIdle()

    fakeRepository.setItems(page1Data + page2Data)
    viewModel.trySendAction(Action.OnLoadMore)
    advanceUntilIdle()

    assertEquals(page1Data + page2Data, viewModel.stateFlow.value.items)
}
```

### 3. User Action Tests

Test all actions defined in the Action sealed interface.

```kotlin
@Test
fun givenAction_whenDispatched_thenStateUpdated() = runTest {
    viewModel.trySendAction(${Feature}Action.OnSomeAction)
    advanceUntilIdle()

    // Verify state change via stateFlow.value
    assertEquals(expected, viewModel.stateFlow.value.someField)
}
```

### 4. Event Tests (Turbine)

Test navigation and one-time events. Use Turbine ONLY for `eventFlow`.

```kotlin
@Test
fun givenSubmitSuccess_whenCompleted_thenNavigateBack() = runTest {
    fakeRepository.setShouldFail(false)

    viewModel.trySendAction(Action.OnSubmit)
    advanceUntilIdle()

    viewModel.eventFlow.test {
        assertEquals(Event.NavigateBack, awaitItem())
    }
}
```

### 5. Validation Tests

Test form validation logic.

```kotlin
@Test
fun givenEmptyInput_whenSubmitted_thenShowsValidationError() = runTest {
    viewModel.trySendAction(Action.OnNameChanged(""))
    viewModel.trySendAction(Action.OnSubmit)
    advanceUntilIdle()

    assertNotNull(viewModel.stateFlow.value.validationError)
}
```

---

## Coroutine Setup (StandardTestDispatcher)

Use `StandardTestDispatcher` with explicit `Dispatchers.setMain/resetMain`:

```kotlin
private val testDispatcher = StandardTestDispatcher()

@BeforeTest
fun setup() {
    Dispatchers.setMain(testDispatcher)
    // Create fakes and ViewModel
}

@AfterTest
fun tearDown() {
    Dispatchers.resetMain()
}
```

**Why StandardTestDispatcher (not UnconfinedTestDispatcher)?**
- `StandardTestDispatcher` gives precise control over coroutine execution
- Requires `advanceUntilIdle()` to process pending coroutines
- Matches the reference project (mobile-wallet) test patterns

---

## State vs Event Assertions

### State: Use `stateFlow.value` directly

```kotlin
// CORRECT: Direct value access for state
assertEquals(expected, viewModel.stateFlow.value.field)
assertNull(viewModel.stateFlow.value.dialogState)
```

### Events: Use Turbine `test { }` block

```kotlin
// CORRECT: Turbine for eventFlow (Channel-based, one-shot)
viewModel.eventFlow.test {
    assertEquals(expectedEvent, awaitItem())
}
```

### Common Turbine Methods (for eventFlow only)

| Method | Purpose |
|--------|---------|
| `awaitItem()` | Wait for next emission |
| `awaitComplete()` | Wait for flow completion |
| `cancelAndIgnoreRemainingEvents()` | Clean up |
| `expectNoEvents()` | Verify no emissions |

---

## Test Coverage Checklist

For each ViewModel, test:

- [ ] Initial state
- [ ] Load success with data
- [ ] Load success with empty data
- [ ] Load error
- [ ] Each action in Action sealed interface
- [ ] Each event in Event sealed interface
- [ ] Validation (if applicable)
- [ ] Dialog states (if applicable)
- [ ] Refresh/Retry
- [ ] Pagination (if applicable)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not using `runTest` | Wrap all tests in `runTest { }` |
| Using `MainDispatcherRule` | Use `StandardTestDispatcher` with `Dispatchers.setMain/resetMain` |
| Using Turbine for stateFlow | Use `viewModel.stateFlow.value.field` instead |
| Using backtick test names | Use `givenX_whenY_thenZ` (works in Kotlin/Native) |
| Missing `advanceUntilIdle()` | Always call after `trySendAction` with `StandardTestDispatcher` |
| Not resetting fakes | Call `reset()` in `@AfterTest` |
