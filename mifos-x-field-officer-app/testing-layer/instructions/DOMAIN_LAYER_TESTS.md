# Domain Layer Tests

> Comprehensive testing patterns for the domain layer (core/domain)

---

## Overview

Domain layer tests verify business logic in use cases and data transformation in mappers. These tests are generated during `/kmp-feature` execution when UseCase classes exist.

**In-Module Testing Rule (RULE-TEST-001)**: Tests are written in the same module where source code is written.

---

## Test File Locations

| Component | Source | Test Location |
|-----------|--------|---------------|
| UseCase | `core/domain/src/commonMain/.../usecase/` | `core/domain/src/commonTest/.../usecase/` |
| Mapper | `core/domain/src/commonMain/.../mapper/` | `core/domain/src/commonTest/.../mapper/` |

---

## UseCase Tests (P0)

### Purpose

Verify that use case classes correctly:
- Return domain models on success
- Handle repository errors gracefully
- Apply business logic (filtering, sorting, pagination)
- Validate input parameters
- Transform data as expected

### Test Template

Reference: `templates/testing-layer/USECASE_TEST_TEMPLATE.kt.md`

### Required Test Scenarios

| Scenario | Priority | Description |
|----------|:--------:|-------------|
| Success with data | P0 | Returns domain models on success |
| Empty list | P0 | Handles empty data properly |
| Repository error | P0 | Propagates error correctly |
| Exception handling | P0 | Catches and wraps exceptions |
| Filter active items | P1 | Business logic: filtering |
| Sort by date | P1 | Business logic: sorting |
| Limit to page size | P1 | Business logic: pagination |
| Search filter | P1 | Business logic: text search |
| Invalid params | P1 | Rejects invalid parameters |
| Repository call verification | P2 | Verifies correct params passed |

### UseCase Test Pattern

```kotlin
class GetItemsUseCaseTest {

    private lateinit var fakeRepository: FakeItemRepository
    private lateinit var useCase: GetItemsUseCase

    @BeforeTest
    fun setup() {
        fakeRepository = FakeItemRepository()
        useCase = GetItemsUseCase(repository = fakeRepository)
    }

    @Test
    fun `invoke returns Success with domain models`() = runTest {
        // Given
        fakeRepository.setLoadSuccess(ItemFixtures.createList(5))

        // When/Then
        useCase().test {
            // Skip Loading state
            val loading = awaitItem()
            assertTrue(loading is DataState.Loading)

            // Verify Success
            val success = awaitItem()
            assertTrue(success is DataState.Success)
            assertEquals(5, (success as DataState.Success).data.size)

            awaitComplete()
        }
    }

    @Test
    fun `invoke returns Error when repository fails`() = runTest {
        // Given
        fakeRepository.setLoadError("Network error")

        // When/Then
        useCase().test {
            skipItems(1) // Skip Loading

            val error = awaitItem()
            assertTrue(error is DataState.Error)
            assertEquals("Network error", (error as DataState.Error).message)

            awaitComplete()
        }
    }
}
```

### Business Logic Test Pattern

```kotlin
@Test
fun `invoke filters inactive items`() = runTest {
    // Given - Mix of active and inactive items
    val items = listOf(
        ItemFixtures.createSingle(id = 1L, isActive = true),
        ItemFixtures.createSingle(id = 2L, isActive = false),
        ItemFixtures.createSingle(id = 3L, isActive = true)
    )
    fakeRepository.setLoadSuccess(items)

    // When/Then
    useCase(filterActive = true).test {
        skipItems(1) // Skip Loading

        val success = awaitItem() as DataState.Success
        // Business logic: should only return active items
        assertEquals(2, success.data.size)
        assertTrue(success.data.all { it.isActive })

        awaitComplete()
    }
}

@Test
fun `invoke sorts items by date descending`() = runTest {
    // Given - Items in random order
    val items = listOf(
        ItemFixtures.createSingle(id = 1L, createdAt = "2026-01-20"),
        ItemFixtures.createSingle(id = 2L, createdAt = "2026-01-22"),
        ItemFixtures.createSingle(id = 3L, createdAt = "2026-01-21")
    )
    fakeRepository.setLoadSuccess(items)

    // When/Then
    useCase(sortBy = SortOrder.DATE_DESC).test {
        skipItems(1) // Skip Loading

        val success = awaitItem() as DataState.Success
        // Business logic: should be sorted by date descending
        assertEquals(2L, success.data[0].id) // Jan 22
        assertEquals(3L, success.data[1].id) // Jan 21
        assertEquals(1L, success.data[2].id) // Jan 20

        awaitComplete()
    }
}

@Test
fun `invoke limits results to page size`() = runTest {
    // Given - More items than page size
    val items = ItemFixtures.createList(25)
    fakeRepository.setLoadSuccess(items)

    // When/Then
    useCase(pageSize = 10).test {
        skipItems(1) // Skip Loading

        val success = awaitItem() as DataState.Success
        // Business logic: should limit to page size
        assertEquals(10, success.data.size)

        awaitComplete()
    }
}
```

### Suspend-Returning UseCase Pattern (Mokkery)

> **Reference**: mobile-wallet `LoginViewModelTest.kt`.
> When a UseCase is a suspend function returning `DataState<T>` directly
> (not `Flow<DataState<T>>`), use Mokkery mocks for repository dependencies
> and `StandardTestDispatcher` with `Dispatchers.setMain/resetMain`.

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class LoginUseCaseTest {

    private val testDispatcher = StandardTestDispatcher()
    private val mockAuthRepository: AuthenticationRepository = mock()
    private val mockClientRepository: ClientRepository = mock()

    @BeforeTest
    fun setUp() { Dispatchers.setMain(testDispatcher) }

    @AfterTest
    fun tearDown() { Dispatchers.resetMain() }

    @Test
    fun givenValidCredentials_whenInvoked_thenReturnsSuccess() = runTest {
        everySuspend {
            mockAuthRepository.authenticate(eq("user"), eq("pass"))
        } returns DataState.Success(userInfo)

        val useCase = LoginUseCase(mockAuthRepository, mockClientRepository, testDispatcher)
        val result = useCase("user", "pass")

        assertIs<DataState.Success<UserInfo>>(result)
        assertEquals("user", result.data.username)
    }

    @Test
    fun givenInvalidCredentials_whenInvoked_thenReturnsError() = runTest {
        everySuspend {
            mockAuthRepository.authenticate(any(), any())
        } returns DataState.Error(Exception("Invalid credentials"))

        val useCase = LoginUseCase(mockAuthRepository, mockClientRepository, testDispatcher)
        val result = useCase("bad", "creds")

        assertIs<DataState.Error>(result)
    }

    @Test
    fun givenAuthSuccess_whenClientAssignment_thenVerifyBothCalls() = runTest {
        everySuspend {
            mockAuthRepository.authenticate(any(), any())
        } returns DataState.Success(UserInfo(id = 1L, clientId = 456))

        everySuspend {
            mockClientRepository.assignClientToUser(eq(1), eq(456))
        } returns DataState.Success(Unit)

        val useCase = LoginUseCase(mockAuthRepository, mockClientRepository, testDispatcher)
        val result = useCase("user", "pass")

        assertIs<DataState.Success<UserInfo>>(result)
        verifySuspend { mockAuthRepository.authenticate(any(), any()) }
        verifySuspend { mockClientRepository.assignClientToUser(eq(1), eq(456)) }
    }
}
```

### When to Use Which Pattern

| Pattern | UseCase Returns | Mock Strategy | Flow Testing |
|---------|----------------|---------------|:------------:|
| **Flow-returning (fakes)** | `Flow<DataState<T>>` | Hand-written fakes | Turbine `awaitItem()` |
| **Suspend-returning (Mokkery)** | `DataState<T>` | Mokkery `mock()` | Direct assertions |

Use **Flow-returning** for list/stream UseCases (e.g., `GetMoviesUseCase`).
Use **Suspend-returning** for auth/mutation UseCases (e.g., `LoginUseCase`, `DeleteItemUseCase`).

### Parameter Validation Pattern

```kotlin
@Test
fun `invoke with invalid id returns Error`() = runTest {
    // Given - Invalid negative ID
    // When/Then
    useCase(id = -1L).test {
        val error = awaitItem()
        assertTrue(error is DataState.Error)
        assertTrue((error as DataState.Error).message.contains("Invalid"))

        awaitComplete()
    }
}

@Test
fun `invoke validates page number is positive`() = runTest {
    // Given
    fakeRepository.setLoadSuccess(ItemFixtures.createList(5))

    // When/Then
    useCase(page = 0).test {
        val error = awaitItem()
        assertTrue(error is DataState.Error)
        assertTrue((error as DataState.Error).message.contains("page"))

        awaitComplete()
    }
}
```

---

## Mapper Tests (P1)

### Purpose

Verify that mapper functions correctly:
- Map all fields from DTO to domain model
- Map all fields from domain model to DTO
- Handle null optional fields
- Parse date strings to LocalDateTime
- Generate computed properties (formattedDate, displayName)

### Test Template

Reference: `templates/testing-layer/MAPPER_TEST_TEMPLATE.kt.md`

### Required Test Scenarios

| Scenario | Priority | Description |
|----------|:--------:|-------------|
| Map all required fields | P0 | All non-null fields mapped correctly |
| Handle null fields | P0 | Null → default values |
| Parse ISO 8601 date | P0 | String → LocalDateTime |
| Computed properties | P1 | formattedDate, displayName generated |
| DTO→Domain→DTO round-trip | P1 | Data preserved |
| Edge cases | P2 | Empty strings, special chars |

### DTO to Domain Pattern

```kotlin
@Test
fun `toDomainModel maps all fields correctly`() {
    // Given
    val dto = ItemDto(
        id = 1L,
        name = "Test Item",
        description = "Test description",
        createdAt = "2026-01-21T10:30:45Z",
        isActive = true
    )

    // When
    val domain = dto.toDomainModel()

    // Then
    assertEquals(1L, domain.id)
    assertEquals("Test Item", domain.name)
    assertEquals("Test description", domain.description)
    assertTrue(domain.isActive)
}

@Test
fun `toDomainModel parses ISO 8601 date correctly`() {
    // Given
    val dto = ItemDto(
        id = 1L,
        name = "Test",
        createdAt = "2026-01-21T10:30:45Z"
    )

    // When
    val domain = dto.toDomainModel()

    // Then
    assertEquals(2026, domain.createdAt.year)
    assertEquals(1, domain.createdAt.monthNumber)
    assertEquals(21, domain.createdAt.dayOfMonth)
    assertEquals(10, domain.createdAt.hour)
    assertEquals(30, domain.createdAt.minute)
}
```

### Null Handling Pattern

```kotlin
@Test
fun `toDomainModel handles null optional fields`() {
    // Given
    val dto = ItemDto(
        id = 1L,
        name = "Test",
        description = null,  // Optional field is null
        createdAt = "2026-01-21T10:00:00Z"
    )

    // When
    val domain = dto.toDomainModel()

    // Then
    assertNull(domain.description)
    // Or verify default value if applicable
}

@Test
fun `toDomainModel uses default for null optional field`() {
    // Given
    val dto = ItemDto(
        id = 1L,
        name = "Test",
        rating = null,  // null rating
        createdAt = "2026-01-21T10:00:00Z"
    )

    // When
    val domain = dto.toDomainModel()

    // Then
    assertEquals(0.0, domain.rating)  // Default value
}
```

### Computed Properties Pattern

```kotlin
@Test
fun `toDomainModel generates formattedDate`() {
    // Given
    val dto = ItemDto(
        id = 1L,
        name = "Test",
        createdAt = "2026-01-21T10:30:45Z"
    )

    // When
    val domain = dto.toDomainModel()

    // Then
    assertEquals("Jan 21, 2026", domain.formattedDate)
}

@Test
fun `toDomainModel generates displayName`() {
    // Given
    val dto = ItemDto(
        id = 1L,
        name = "test item",
        createdAt = "2026-01-21T10:00:00Z"
    )

    // When
    val domain = dto.toDomainModel()

    // Then
    assertEquals("Test Item", domain.displayName)  // Title case
}
```

### Round-Trip Pattern

```kotlin
@Test
fun `domain to DTO to domain preserves data`() {
    // Given
    val original = Item(
        id = 1L,
        name = "Test Item",
        description = "Description",
        createdAt = LocalDateTime(2026, 1, 21, 10, 30, 45),
        isActive = true
    )

    // When
    val restored = original.toDto().toDomainModel()

    // Then
    assertEquals(original.id, restored.id)
    assertEquals(original.name, restored.name)
    assertEquals(original.description, restored.description)
    assertEquals(original.isActive, restored.isActive)
}
```

---

## Fake Repository Pattern

```kotlin
class FakeItemRepository : ItemRepository {

    // Call tracking
    var loadCallCount = 0
        private set
    var lastCategory: String? = null
        private set
    var lastPage: Int? = null
        private set

    // Response configuration
    private var loadResponse: DataState<List<Item>> = DataState.Success(emptyList())
    private var singleResponse: DataState<Item>? = null

    fun setLoadSuccess(data: List<Item>) {
        loadResponse = DataState.Success(data)
    }

    fun setLoadError(message: String) {
        loadResponse = DataState.Error(message)
    }

    fun setLoadEmpty() {
        loadResponse = DataState.Success(emptyList())
    }

    fun setLoadException(exception: Exception) {
        loadResponse = DataState.Error(exception.message ?: "Unknown error")
    }

    override fun getItems(category: String?, page: Int): Flow<DataState<List<Item>>> = flow {
        loadCallCount++
        lastCategory = category
        lastPage = page
        emit(DataState.Loading)
        emit(loadResponse)
    }

    fun reset() {
        loadCallCount = 0
        lastCategory = null
        lastPage = null
        loadResponse = DataState.Success(emptyList())
    }
}
```

---

## Domain Model Fixtures

```kotlin
object ItemFixtures {

    fun createSingle(
        id: Long = 1L,
        name: String = "Test Item",
        description: String? = "Test description",
        createdAt: LocalDateTime = LocalDateTime(2026, 1, 21, 10, 0, 0),
        isActive: Boolean = true
    ): Item = Item(
        id = id,
        name = name,
        description = description,
        createdAt = createdAt,
        isActive = isActive,
        formattedDate = "Jan 21, 2026",
        displayName = name.replaceFirstChar { it.uppercase() }
    )

    fun createList(
        count: Int = 5,
        startId: Long = 1L
    ): List<Item> = (0 until count).map { index ->
        createSingle(
            id = startId + index,
            name = "Item ${startId + index}"
        )
    }
}
```

---

## Test Dependencies

```kotlin
// build.gradle.kts (core/domain)
kotlin {
    sourceSets {
        commonTest.dependencies {
            implementation(kotlin("test"))
            implementation(libs.kotlinx.coroutines.test)
            implementation(libs.turbine)  // Flow testing
            implementation(libs.kotlinx.datetime)  // Date testing
        }
    }
}
```

---

## Coverage Requirements

| Test File | Min Tests | P0 Coverage |
|-----------|:---------:|:-----------:|
| `Get{Feature}sUseCaseTest.kt` (Flow) | 7 | Success, empty, error, exception |
| `{Feature}UseCaseTest.kt` (Suspend) | 4 | Success, error, multi-repo |
| `{Model}MapperTest.kt` | 5 | All fields, nulls, dates |

**Total Domain Layer: ~16 tests per feature**

---

## Related Files

| File | Purpose |
|------|---------|
| `templates/testing-layer/USECASE_TEST_TEMPLATE.kt.md` | UseCase test template |
| `templates/testing-layer/MAPPER_TEST_TEMPLATE.kt.md` | Mapper test template |
| `templates/testing-layer/TESTING_GENERATION_INDEX.md` | Test generation index |
| `templates/shared/PATTERNS.md` | DataState patterns |
