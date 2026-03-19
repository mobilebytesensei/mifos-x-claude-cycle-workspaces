# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/testing-layer/TEST_PATTERNS.md"
# last_modified: "2026-03-19"

# Test Patterns - O(1) Reference

> Quick lookup for test patterns used in ${PROJECT_NAME}

---

## Pattern Quick Reference

| # | Pattern | Use Case | Location | Details |
|:-:|---------|----------|----------|---------|
| 1 | ViewModel Test | Test state, actions, events | `commonTest/` | [VIEWMODEL_TEST.md](./patterns/VIEWMODEL_TEST.md) |
| 2 | Screen Test | Test UI composition | `androidInstrumentedTest/` | [SCREEN_TEST.md](./patterns/SCREEN_TEST.md) |
| 3 | Fake Repository | Test isolation | `commonTest/fake/` | [FAKE_REPOSITORY.md](./patterns/FAKE_REPOSITORY.md) |
| 4 | Integration Test | Test user flows | `cmp-android/androidTest/` | [INTEGRATION_TEST.md](./patterns/INTEGRATION_TEST.md) |
| 5 | Screenshot Test | Visual regression | `test/` (Roborazzi) | [SCREENSHOT_TEST.md](./patterns/SCREENSHOT_TEST.md) |

---

## 1. ViewModel Test Pattern

### When to Use
- Testing state transitions (Loading -> Success -> Error)
- Testing action handling
- Testing event emission (navigation, dialogs)

### Quick Template

```kotlin
class ${Feature}ViewModelTest {
    private val testDispatcher = StandardTestDispatcher()
    private lateinit var viewModel: ${Feature}ViewModel
    private lateinit var fakeRepository: Fake${Feature}Repository

    @BeforeTest
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        fakeRepository = Fake${Feature}Repository()
        viewModel = ${Feature}ViewModel(repository = fakeRepository)
    }

    @AfterTest
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun givenNewViewModel_whenCreated_thenInitialStateIsLoading() {
        assertEquals(${Feature}ScreenState.Loading, viewModel.stateFlow.value.uiState)
    }

    @Test
    fun givenSuccessResponse_whenDataLoaded_thenStateIsSuccess() = runTest {
        fakeRepository.setItems(testData)
        advanceUntilIdle()

        assertEquals(${Feature}ScreenState.Success, viewModel.stateFlow.value.uiState)
    }
}
```

---

## 2. Screen Test Pattern

### When to Use
- Testing UI composition
- Testing user interactions
- Accessibility testing

### Quick Template

```kotlin
class ${Feature}ScreenTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun loadingState_displaysLoadingIndicator() {
        composeTestRule.setContent {
            ${Feature}Content(
                state = ${Feature}State(uiState = Loading),
                onAction = {}
            )
        }

        composeTestRule
            .onNodeWithTag(${Feature}TestTags.LOADING)
            .assertIsDisplayed()
    }
}
```

---

## 3. Fake Repository Pattern

### When to Use
- Isolating ViewModel tests from real data
- Configuring specific responses for test scenarios

### Quick Template

```kotlin
class Fake${Feature}Repository : ${Feature}Repository {
    var loadCallCount = 0
        private set

    private var loadResponse: DataState<List<${Model}>> = DataState.Loading

    fun setLoadSuccess(data: List<${Model}>) {
        loadResponse = DataState.Success(data)
    }

    fun setLoadError(message: String) {
        loadResponse = DataState.Error(message)
    }

    override fun get${Feature}s(): Flow<DataState<List<${Model}>>> = flow {
        loadCallCount++
        emit(loadResponse)
    }

    fun reset() {
        loadCallCount = 0
        loadResponse = DataState.Loading
    }
}
```

---

## Key Libraries

| Library | Import | Purpose |
|---------|--------|---------|
| kotlin-test | `kotlin.test.*` | Assertions |
| coroutines-test | `kotlinx.coroutines.test.*` | runTest |
| turbine | `app.cash.turbine.*` | Flow testing |
| compose-test | `androidx.compose.ui.test.*` | UI testing |

---

## Test Naming Convention

```
givenX_whenY_thenZ

Examples:
- givenSuccessResponse_whenDataLoaded_thenStateIsSuccess
- givenInvalidInput_whenSubmitClicked_thenShowsValidationError
- givenDialogConfirmed_whenDeleteItem_thenRemovesFromList
```

---

## Coverage Targets

| Test Type | Target | Priority |
|-----------|--------|----------|
| ViewModel Tests | 100% actions | P0 |
| Screen Tests | All states | P1 |
| Integration Tests | Critical flows | P1 |
| Screenshot Tests | Key screens | P2 |
