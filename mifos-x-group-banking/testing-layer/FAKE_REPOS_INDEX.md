# Fake Repositories Index - O(1) Lookup

> **${FAKE_COUNT} repositories** | Test doubles for isolation | **Last Updated**: ${DATE}

---

## Quick Lookup

| # | Feature | Repository | Fake Repository | Status |
|:-:|---------|------------|-----------------|:------:|
| 1 | ${feature_1} | `${Feature1}Repository` | `Fake${Feature1}Repository` | Planned |
| 2 | ${feature_2} | `${Feature2}Repository` | `Fake${Feature2}Repository` | Planned |

---

## O(1) Path Pattern

```
core/testing/src/commonMain/kotlin/org/${package}/core/testing/fake/Fake${Feature}Repository.kt
```

---

## Fake Repository Pattern

### Standard Structure

```kotlin
class Fake${Feature}Repository : ${Feature}Repository {
    // =========================================================================
    // CALL TRACKING
    // =========================================================================
    var loadCallCount = 0
        private set
    var createCallCount = 0
        private set
    var updateCallCount = 0
        private set
    var deleteCallCount = 0
        private set

    // =========================================================================
    // CONFIGURABLE RESPONSES
    // =========================================================================
    private var loadResponse: DataState<List<${Model}>> = DataState.Loading
    private var singleResponse: DataState<${Model}> = DataState.Loading
    private var createResponse: DataState<${Model}> = DataState.Loading
    private var deleteResponse: DataState<Unit> = DataState.Loading

    // =========================================================================
    // SETUP METHODS
    // =========================================================================
    fun setLoadSuccess(data: List<${Model}>) {
        loadResponse = DataState.Success(data)
    }

    fun setLoadError(message: String = "Failed to load") {
        loadResponse = DataState.Error(message)
    }

    fun setLoadEmpty() {
        loadResponse = DataState.Success(emptyList())
    }

    // =========================================================================
    // REPOSITORY IMPLEMENTATION
    // =========================================================================
    override fun get${Feature}s(): Flow<DataState<List<${Model}>>> = flow {
        loadCallCount++
        emit(loadResponse)
    }

    // =========================================================================
    // RESET
    // =========================================================================
    fun reset() {
        loadCallCount = 0
        createCallCount = 0
        updateCallCount = 0
        deleteCallCount = 0
        loadResponse = DataState.Loading
    }
}
```

---

## Usage in Tests

```kotlin
class ${Feature}ViewModelTest {
    private lateinit var fakeRepository: Fake${Feature}Repository
    private lateinit var viewModel: ${Feature}ViewModel

    @BeforeTest
    fun setup() {
        fakeRepository = Fake${Feature}Repository()
        viewModel = ${Feature}ViewModel(repository = fakeRepository)
    }

    @AfterTest
    fun teardown() {
        fakeRepository.reset()
    }

    @Test
    fun `load success updates state`() = runTest {
        val testData = ${Feature}Fixtures.createList(5)
        fakeRepository.setLoadSuccess(testData)

        viewModel.loadData()

        viewModel.stateFlow.test {
            val state = expectMostRecentItem()
            assertEquals(testData, (state.uiState as Success).data)
        }
    }
}
```

---

## Implementation Status

| Status | Count | Description |
|--------|-------|-------------|
| Done | 0 | Fully implemented and tested |
| Planned | ${FAKE_COUNT} | Repository exists, fake needed |
| N/A | - | No repository for feature |

---

## Checklist for New Fake Repository

- [ ] Implements real repository interface
- [ ] Has call counters for all methods
- [ ] Has configurable responses (success, error, loading)
- [ ] Has `reset()` method for test isolation
- [ ] Added to this index
