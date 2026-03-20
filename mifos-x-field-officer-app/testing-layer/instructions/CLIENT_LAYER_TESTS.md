# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/testing-layer/instructions/CLIENT_LAYER_TESTS.md"
# last_modified: "2026-03-20"

# Client Layer Tests

> Comprehensive testing patterns for the client layer (core/network, core/data, core/model)

---

## Overview

Client layer tests verify the data pipeline from API services through repositories to the rest of the application. These tests are MANDATORY and are generated during `/kmp-client` execution.

**In-Module Testing Rule (RULE-TEST-001)**: Tests are written in the same module where source code is written.

---

## Test File Locations

| Layer | Source | Test Location |
|-------|--------|---------------|
| Network (Service) | `core/network/src/commonMain/.../services/` | `core/network/src/commonTest/.../services/` |
| Network (DTO) | `core/network/src/commonMain/.../model/` | `core/network/src/commonTest/.../model/` |
| Data (Repository) | `core/data/src/commonMain/.../repositories/` | `core/data/src/commonTest/.../repositories/` |

---

## Service Tests (P0)

### Purpose

Verify that API service classes correctly:
- Construct HTTP requests
- Parse HTTP responses
- Handle HTTP error codes
- Pass correct parameters

### Test Template

Reference: `templates/testing-layer/SERVICE_TEST_TEMPLATE.kt.md`

### Required Test Scenarios

| Scenario | Priority | Description |
|----------|:--------:|-------------|
| GET list 200 | P0 | Returns list on successful response |
| GET list empty | P0 | Returns empty list when no data |
| GET single 200 | P0 | Returns item on successful response |
| GET 404 | P0 | Throws on not found |
| POST 201 | P0 | Returns created item |
| POST 400 | P0 | Throws on validation error |
| Server 500 | P0 | Throws on server error |
| Unauthorized 401 | P1 | Throws on auth failure |

### Mock Engine Pattern

> **Note on test naming**: Use `givenX_whenY_thenZ` convention (NOT backtick strings).
> Backtick test names do not work in Kotlin/Native which is used for iOS targets in KMP.

```kotlin
private val json = Json {
    ignoreUnknownKeys = true
    isLenient = true
}

@Test
fun givenApi200_whenGetItems_thenReturnsSuccess() = runTest {
    // Given
    val expectedData = listOf(ItemDto(id = 1L, name = "Test"))
    mockEngine = MockEngine { request ->
        respond(
            content = json.encodeToString(expectedData),
            status = HttpStatusCode.OK,
            headers = headersOf(HttpHeaders.ContentType, ContentType.Application.Json.toString())
        )
    }

    // When
    val result = service.getItems()

    // Then
    assertEquals(1, result.size)
    assertEquals("Test", result.first().name)
}
```

### Request Verification Pattern

```kotlin
@Test
fun givenItemId_whenGetItem_thenPassesCorrectIdInRequest() = runTest {
    // Given
    var capturedUrl: String? = null
    mockEngine = MockEngine { request ->
        capturedUrl = request.url.toString()
        respond(
            content = json.encodeToString(ItemDto(id = 123L, name = "Test")),
            status = HttpStatusCode.OK,
            headers = headersOf(HttpHeaders.ContentType, ContentType.Application.Json.toString())
        )
    }

    // When
    service.getItem(id = 123L)

    // Then
    assertTrue(capturedUrl?.contains("123") == true)
}
```

---

## Repository Tests (P0)

### Purpose

Verify that repository classes correctly:
- Emit Loading → Success/Error states
- Call service methods with correct parameters
- Map DTOs to domain models
- Handle exceptions gracefully

### Test Template

Reference: `templates/testing-layer/REPOSITORY_TEST_TEMPLATE.kt.md`

### Required Test Scenarios

| Scenario | Priority | Description |
|----------|:--------:|-------------|
| Loading then Success | P0 | Emits Loading, then Success with data |
| Loading then Error | P0 | Emits Loading, then Error on failure |
| DTO→Domain mapping | P0 | Transforms DTOs correctly |
| Empty data | P1 | Handles empty list properly |
| Refresh behavior | P1 | Force refresh bypasses cache |
| Multiple calls | P1 | Tracks call count |

### DataState Flow Pattern

> **Note**: The reference projects use `DataState.Success` and `DataState.Error` (with `Exception`/`Throwable`).
> Some repositories wrap results in `Flow<DataState<T>>` while others return `DataState<T>` directly.

```kotlin
@Test
fun givenSuccessfulApi_whenGetItems_thenEmitsSuccessWithData() = runTest {
    // Given
    fakeService.setGetListSuccess(listOf(ItemDto(id = 1L, name = "Test")))

    // When/Then
    repository.getItems().test {
        // First emission: Loading
        val loading = awaitItem()
        assertTrue(loading is DataState.Loading)

        // Second emission: Success
        val success = awaitItem()
        assertTrue(success is DataState.Success)
        assertEquals(1, (success as DataState.Success).data.size)

        awaitComplete()
    }
}
```

### Error Handling Pattern

```kotlin
@Test
fun givenApiFailure_whenGetItems_thenEmitsError() = runTest {
    // Given
    fakeService.setGetListError("Network error")

    // When/Then
    repository.getItems().test {
        // Skip Loading
        skipItems(1)

        // Verify Error
        val error = awaitItem()
        assertTrue(error is DataState.Error)

        awaitComplete()
    }
}
```

### Fake Service Pattern

> **Reference pattern**: Fakes use simple mutable state and `shouldReturnError` flags.
> They are defined as `private class` in the test file or `internal class` in TestFakes.kt.

```kotlin
class FakeItemService : ItemService {

    // Call tracking
    var getListCallCount = 0
        private set
    var lastRequestedId: Long? = null
        private set

    // Response configuration
    private var listResponse: Result<List<ItemDto>> = Result.success(emptyList())
    private var singleResponse: Result<ItemDto>? = null

    fun setGetListSuccess(data: List<ItemDto>) {
        listResponse = Result.success(data)
    }

    fun setGetListError(message: String) {
        listResponse = Result.failure(Exception(message))
    }

    override suspend fun getItems(): List<ItemDto> {
        getListCallCount++
        return listResponse.getOrThrow()
    }

    override suspend fun getItem(id: Long): ItemDto {
        lastRequestedId = id
        return singleResponse?.getOrThrow() ?: throw Exception("Not configured")
    }

    fun reset() {
        getListCallCount = 0
        lastRequestedId = null
        listResponse = Result.success(emptyList())
        singleResponse = null
    }
}
```

### Alternative: Mokkery Mocks for Services

When services have many methods or you need argument matching, use Mokkery:

```kotlin
private val mockService: ItemService = mock()

@BeforeTest
fun setUp() {
    everySuspend { mockService.getItems() } returns listOf(ItemDto(id = 1L, name = "Test"))
}

@Test
fun givenMockedService_whenGetItems_thenVerifyCall() = runTest {
    val result = mockService.getItems()
    verifySuspend { mockService.getItems() }
    assertEquals(1, result.size)
}
```

---

## DTO Serialization Tests (P1)

### Purpose

Verify that DTO classes correctly:
- Serialize to JSON
- Deserialize from JSON
- Handle null fields
- Map JSON field names correctly

### Test Template

Reference: `templates/testing-layer/DTO_TEST_TEMPLATE.kt.md`

### Required Test Scenarios

| Scenario | Priority | Description |
|----------|:--------:|-------------|
| Deserialize valid JSON | P0 | Parses all fields correctly |
| Deserialize minimal JSON | P0 | Handles required fields only |
| Handle null optionals | P0 | Accepts null for optional fields |
| Serialize to JSON | P1 | Outputs correct JSON format |
| Round-trip | P1 | Data preserved through serialize/deserialize |
| snake_case mapping | P1 | @SerialName annotations work |
| Wrong type error | P1 | Throws on type mismatch |
| Missing required error | P1 | Throws on missing required field |

### Serialization Test Pattern

```kotlin
private val json = Json {
    ignoreUnknownKeys = true
    isLenient = true
}

@Test
fun givenValidJson_whenDeserialized_thenItemDtoHasCorrectFields() {
    // Given
    val jsonString = """
        {
            "id": 1,
            "name": "Test Item",
            "created_at": "2026-01-21T10:00:00Z"
        }
    """.trimIndent()

    // When
    val dto = json.decodeFromString<ItemDto>(jsonString)

    // Then
    assertEquals(1L, dto.id)
    assertEquals("Test Item", dto.name)
    assertEquals("2026-01-21T10:00:00Z", dto.createdAt)
}

@Test
fun givenItemDto_whenSerialized_thenJsonHasCorrectFormat() {
    // Given
    val dto = ItemDto(
        id = 1L,
        name = "Test Item",
        createdAt = "2026-01-21T10:00:00Z"
    )

    // When
    val jsonString = json.encodeToString(dto)

    // Then
    assertTrue(jsonString.contains("\"id\":1"))
    assertTrue(jsonString.contains("\"name\":\"Test Item\""))
    assertTrue(jsonString.contains("\"created_at\":"))  // snake_case
}
```

---

## DTO Fixtures

### Purpose

Provide reusable test data for DTO tests and downstream tests.

### Pattern

```kotlin
object ItemDtoFixtures {

    fun createSingle(
        id: Long = 1L,
        name: String = "Test Item",
        description: String? = "Test description",
        createdAt: String = "2026-01-21T10:00:00Z",
        isActive: Boolean = true
    ): ItemDto = ItemDto(
        id = id,
        name = name,
        description = description,
        createdAt = createdAt,
        isActive = isActive
    )

    fun createList(
        count: Int = 5,
        startId: Long = 1L
    ): List<ItemDto> = (0 until count).map { index ->
        createSingle(
            id = startId + index,
            name = "Item ${startId + index}"
        )
    }

    fun createJsonString(id: Long = 1L, name: String = "Test"): String = """
        {"id":$id,"name":"$name","created_at":"2026-01-21T10:00:00Z"}
    """.trimIndent()
}
```

---

## UseCase Tests (P1)

### Purpose

Verify that UseCase classes correctly:
- Compose repository calls
- Apply business logic (filtering, sorting, validation)
- Handle errors from underlying repositories
- Return the correct domain model or DataState

### Test Template

Reference: `templates/testing-layer/USECASE_TEST_TEMPLATE.kt.md`

### Two UseCase Patterns

| Pattern | Returns | Test With | When to Use |
|---------|---------|-----------|-------------|
| **Flow-returning** | `Flow<DataState<T>>` | Turbine `awaitItem()` | List/stream UseCases |
| **Suspend-returning** | `DataState<T>` | Direct assertions | Auth/mutation UseCases |

### Suspend-Returning UseCase Test (Mokkery)

> **Reference**: mobile-wallet's `LoginViewModelTest.kt`.
> When a UseCase is a suspend function returning `DataState<T>` directly,
> use Mokkery to mock repository dependencies and assert results directly.

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class LoginUseCaseTest {

    private val testDispatcher = StandardTestDispatcher()
    private val mockAuthRepository: AuthenticationRepository = mock()
    private val mockClientRepository: ClientRepository = mock()

    private lateinit var useCase: LoginUseCase

    @BeforeTest
    fun setUp() {
        Dispatchers.setMain(testDispatcher)
        useCase = LoginUseCase(
            authRepository = mockAuthRepository,
            clientRepository = mockClientRepository,
            ioDispatcher = testDispatcher,
        )
    }

    @AfterTest
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun givenValidCredentials_whenInvoked_thenReturnsSuccess() = runTest {
        // Given
        everySuspend {
            mockAuthRepository.authenticate(eq("user"), eq("pass"))
        } returns DataState.Success(UserInfo(id = 1L, username = "user"))

        // When
        val result = useCase("user", "pass")

        // Then
        assertIs<DataState.Success<UserInfo>>(result)
        assertEquals("user", result.data.username)
    }

    @Test
    fun givenInvalidCredentials_whenInvoked_thenReturnsError() = runTest {
        // Given
        everySuspend {
            mockAuthRepository.authenticate(any(), any())
        } returns DataState.Error(Exception("Invalid credentials"))

        // When
        val result = useCase("bad", "creds")

        // Then
        assertIs<DataState.Error>(result)
    }

    @Test
    fun givenAuthSuccess_whenClientAssignment_thenVerifyBothCalls() = runTest {
        // Given
        everySuspend {
            mockAuthRepository.authenticate(any(), any())
        } returns DataState.Success(UserInfo(id = 1L, username = "user", clientId = 456))

        everySuspend {
            mockClientRepository.assignClientToUser(eq(1), eq(456))
        } returns DataState.Success(Unit)

        // When
        val result = useCase("user", "pass")

        // Then
        assertIs<DataState.Success<UserInfo>>(result)

        verifySuspend { mockAuthRepository.authenticate(any(), any()) }
        verifySuspend { mockClientRepository.assignClientToUser(eq(1), eq(456)) }
    }
}
```

### Advanced Mokkery Matchers for UseCase Tests

```kotlin
import dev.mokkery.matcher.any
import dev.mokkery.matcher.eq
import dev.mokkery.matcher.logical.or

// OR matching: accept multiple valid values
everySuspend {
    mockSearchRepository.searchResources(
        or(eq("john_doe"), eq("9876543210")),
        any(),
        any()
    )
} returns DataState.Success(emptyList())

// IMPORTANT: All parameters must use matchers (cannot mix literals and matchers)
// CORRECT:   mockRepo.search(eq("query"), any(), eq(10))
// INCORRECT: mockRepo.search("query", any(), 10)  // won't compile
```

### Required Test Scenarios (UseCase)

| Scenario | Priority | Description |
|----------|:--------:|-------------|
| Valid input success | P0 | Returns Success with domain model |
| Invalid input error | P0 | Returns Error for bad parameters |
| Repository failure | P0 | Propagates repository errors |
| Multi-repo composition | P1 | Verifies interaction between repositories |
| Business logic | P1 | Filtering, sorting, validation |
| Parameter passing | P2 | Correct params forwarded to repositories |

---

## Test Dependencies

```kotlin
// build.gradle.kts

// core/network
kotlin {
    sourceSets {
        commonTest.dependencies {
            implementation(kotlin("test"))
            implementation(libs.ktor.client.mock)
            implementation(libs.kotlinx.coroutines.test)
        }
    }
}

// core/data
kotlin {
    sourceSets {
        commonTest.dependencies {
            implementation(kotlin("test"))
            implementation(libs.kotlinx.coroutines.test)
            implementation(libs.turbine)  // Flow testing
        }
    }
}
```

---

## Coverage Requirements

| Test File | Min Tests | P0 Coverage |
|-----------|:---------:|:-----------:|
| `{Feature}ServiceTest.kt` | 8 | GET success/error, POST success/error |
| `{Feature}RepositoryTest.kt` | 6 | Loading→Success, Loading→Error, mapping |
| `{Model}DtoTest.kt` | 10 | Serialize, deserialize, null, errors |
| `{Feature}UseCaseTest.kt` | 6 | Success, error, multi-repo, business logic |

**Total Client Layer: ~30 tests per feature**

---

## Related Files

| File | Purpose |
|------|---------|
| `templates/testing-layer/SERVICE_TEST_TEMPLATE.kt.md` | Service test template |
| `templates/testing-layer/REPOSITORY_TEST_TEMPLATE.kt.md` | Repository test template |
| `templates/testing-layer/DTO_TEST_TEMPLATE.kt.md` | DTO test template |
| `templates/testing-layer/TESTING_GENERATION_INDEX.md` | Test generation index |
| `templates/testing-layer/USECASE_TEST_TEMPLATE.kt.md` | UseCase test template |
| `templates/instructions/testing-layer/DOMAIN_LAYER_TESTS.md` | Domain layer test patterns |
| `templates/instructions/client-layer/CLIENT_PATTERNS.md` | Client implementation patterns |
