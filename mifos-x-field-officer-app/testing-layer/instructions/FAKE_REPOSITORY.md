# Fake Repository Pattern

> Detailed instructions for creating test doubles in KMP projects

---

## Overview

Fake repositories:
- Implement the real repository interface
- Provide configurable responses for testing
- Use `MutableStateFlow` for observable state properties
- Enable test isolation without mocking frameworks

---

## Two Approaches in Reference Projects

The reference projects use TWO approaches for test doubles:

### 1. Hand-Written Fakes (Preferred for simple repositories)

Used when the interface exposes `StateFlow` properties or has simple methods.

**Examples**: `FakeUserPreferencesRepository`, `FakeBeneficiaryRepository`, `FakeLocalAssetRepository`

### 2. Mokkery Mocks (Preferred for complex interfaces)

Used when the interface has many suspend methods that need specific argument matching.

**Examples**: `mock<LoginUseCase>()`, `mock<SearchRepository>()`, `mock<UserRepository>()`

---

## File Location

> **Reference pattern**: Fakes are defined INSIDE the test file or in a
> sibling `TestFakes.kt` file in the same `commonTest` source set.
> They are NOT placed in a shared `core/testing` module.

### Option A: Private class inside test file (most common)

```
feature/${feature}/src/commonTest/kotlin/.../MpayQrViewModelTest.kt
// FakeUserPreferencesRepository defined as private class at bottom of file
```

### Option B: Internal class in sibling TestFakes.kt

```
feature/${feature}/src/commonTest/kotlin/.../TestFakes.kt
// FakeBeneficiaryRepository, FakeUserPreferencesRepository defined here
```

---

## Standard Fake Template (MutableStateFlow-backed)

> **Reference**: `FakeUserPreferencesRepository` in `MpayQrViewModelTest.kt` and `TestFakes.kt`

```kotlin
/**
 * Fake implementation of [${Feature}Repository] for testing.
 */
private class Fake${Feature}Repository(
    initialValue: ${Model}? = null,
    initialList: List<${Model}> = emptyList(),
) : ${Feature}Repository {

    // ===============================================================
    // MUTABLE STATE (expose via interface StateFlow properties)
    // ===============================================================

    private val _items = MutableStateFlow(initialList)
    private val _selectedItem = MutableStateFlow(initialValue)

    override val items: StateFlow<List<${Model}>> = _items
    override val selectedItem: StateFlow<${Model}?> = _selectedItem

    // ===============================================================
    // SETTER METHODS (for test configuration)
    // ===============================================================

    fun setItems(list: List<${Model}>) {
        _items.value = list
    }

    fun setSelectedItem(item: ${Model}?) {
        _selectedItem.value = item
    }

    // ===============================================================
    // CONFIGURABLE ERROR FLAG
    // ===============================================================

    private var shouldReturnError = false

    fun setShouldReturnError(error: Boolean) {
        shouldReturnError = error
    }

    // ===============================================================
    // REPOSITORY IMPLEMENTATION
    // ===============================================================

    override suspend fun getItems(): Flow<DataState<List<${Model}>>> {
        return if (shouldReturnError) {
            flowOf(DataState.Error(Throwable("Network error")))
        } else {
            flowOf(DataState.Success(_items.value))
        }
    }

    override suspend fun createItem(payload: ${Model}Payload): DataState<String> {
        return DataState.Success("Success")
    }

    override suspend fun updateItem(
        id: Long,
        payload: ${Model}Payload,
    ): DataState<String> {
        return DataState.Success("Success")
    }

    override suspend fun deleteItem(id: Long): DataState<String> {
        return DataState.Success("Success")
    }
}
```

---

## Reference Examples

### Example 1: FakeBeneficiaryRepository (from TestFakes.kt)

```kotlin
internal class FakeBeneficiaryRepository : BeneficiaryRepository {
    private var beneficiaryList: List<Beneficiary> = emptyList()
    private var shouldReturnError = false

    fun setBeneficiaryList(list: List<Beneficiary>) {
        beneficiaryList = list
    }

    fun setShouldReturnError(error: Boolean) {
        shouldReturnError = error
    }

    override suspend fun getBeneficiaryList(): Flow<DataState<List<Beneficiary>>> {
        return if (shouldReturnError) {
            flowOf(DataState.Error(Throwable("Network error")))
        } else {
            flowOf(DataState.Success(beneficiaryList))
        }
    }

    override suspend fun createBeneficiary(payload: BeneficiaryPayload): DataState<String> {
        return DataState.Success("Success")
    }

    // ... other interface methods return simple defaults
}
```

### Example 2: FakeUserPreferencesRepository (MutableStateFlow-backed)

```kotlin
private class FakeUserPreferencesRepository(
    initialClient: Client? = null,
    initialDefaultAccount: DefaultAccount? = null,
    initialSelectedInstance: ServerInstance? = null,
) : UserPreferencesRepository {
    private val _selectedInstance = MutableStateFlow(initialSelectedInstance)
    private val _client = MutableStateFlow(initialClient)
    private val _defaultAccount = MutableStateFlow(initialDefaultAccount)

    override val selectedInstance: StateFlow<ServerInstance?> = _selectedInstance
    override val client: StateFlow<Client?> = _client
    override val defaultAccount: StateFlow<DefaultAccount?> = _defaultAccount

    fun setSelectedInstance(instance: ServerInstance?) {
        _selectedInstance.value = instance
    }

    fun setClient(client: Client?) {
        _client.value = client
    }

    fun setDefaultAccount(account: DefaultAccount?) {
        _defaultAccount.value = account
    }

    // Minimal defaults for remaining interface methods
    override val userInfo: Flow<UserInfo> = flowOf(UserInfo(...defaults...))
    override val token: StateFlow<String?> = MutableStateFlow(null)
    override suspend fun updateToken(token: String): DataState<Unit> = DataState.Success(Unit)
    override suspend fun logOut() {}
}
```

---

## Usage Examples

### Basic Test Setup

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class ${Feature}ViewModelTest {
    private val testDispatcher = StandardTestDispatcher()
    private lateinit var fakeRepository: Fake${Feature}Repository

    @BeforeTest
    fun setUp() {
        Dispatchers.setMain(testDispatcher)
        fakeRepository = Fake${Feature}Repository()
        viewModel = ${Feature}ViewModel(
            repository = fakeRepository,
            savedStateHandle = SavedStateHandle(),
        )
    }

    @AfterTest
    fun tearDown() {
        Dispatchers.resetMain()
    }
}
```

### Pre-configuring State via Constructor

```kotlin
// Pass initial values via constructor for immediate availability
fakeRepository = FakeUserPreferencesRepository(
    initialClient = createTestClient(),
    initialDefaultAccount = createTestDefaultAccount(),
    initialSelectedInstance = createTestServerInstance(),
)
```

### Changing State During Test

```kotlin
@Test
fun givenNoDefaultAccount_whenViewModelCreated_thenShowsError() = runTest {
    // Override the pre-set value
    fakeRepository.setDefaultAccount(DefaultAccount.DEFAULT)

    val viewModel = createViewModel()
    advanceUntilIdle()

    assertIs<ViewState.Error>(viewModel.stateFlow.value.viewState)
}
```

---

## When to Use Mokkery Instead

Use Mokkery mocks when:
- The interface has many suspend methods needing specific argument matching
- You need to verify exact call parameters with `verifySuspend`
- You need advanced matchers like `any()`, `eq()`, `or()`

```kotlin
// Mokkery mock setup
private val mockSearchRepository: SearchRepository = mock()

// Configure
everySuspend {
    mockSearchRepository.searchResources("john_doe", any(), any())
} returns DataState.Success(emptyList())

// Verify
verifySuspend {
    mockSearchRepository.searchResources("john_doe", any(), any())
}
```

---

## Naming Convention

| Real Interface | Fake Class |
|----------------|------------|
| `UserPreferencesRepository` | `FakeUserPreferencesRepository` |
| `BeneficiaryRepository` | `FakeBeneficiaryRepository` |
| `LocalAssetRepository` | `FakeLocalAssetRepository` |

---

## Checklist

When creating a fake repository:

- [ ] Implements real repository interface
- [ ] Uses `MutableStateFlow` for observable state properties
- [ ] Has setter methods for test configuration (e.g., `setItems()`, `setSelectedItem()`)
- [ ] Has `shouldReturnError` flag for error testing
- [ ] Returns simple defaults for methods not under test
- [ ] Defined as `private class` in test file or `internal class` in TestFakes.kt
- [ ] Supports constructor parameters for initial state

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Putting fakes in `core/testing/src/commonMain/` | Put in same `commonTest` directory as the test |
| Over-engineering with call counters | Only add tracking when test needs it |
| Not implementing all interface methods | Use simple defaults for unused methods |
| Using mutable vars instead of MutableStateFlow | Use MutableStateFlow for StateFlow-backed properties |
