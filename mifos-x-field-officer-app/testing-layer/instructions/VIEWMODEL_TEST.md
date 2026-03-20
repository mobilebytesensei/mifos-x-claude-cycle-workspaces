# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/testing-layer/instructions/VIEWMODEL_TEST.md"
# last_modified: "2026-03-20"

# ViewModel Test Pattern

> Detailed instructions for testing ViewModels in KMP projects using BaseViewModel

---

## Overview

ViewModel tests verify:
- State transitions (Loading, Success, Error via stateFlow.value)
- Action handling (user interactions via trySendAction)
- Event emission (navigation, dialogs via eventFlow with Turbine)
- Business logic correctness

---

## File Location

```
feature/${feature}/src/commonTest/kotlin/org/${package}/feature/${feature}/${Feature}ViewModelTest.kt
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
            implementation(libs.turbine)       // Flow testing (for eventFlow)
            implementation(libs.mokkery)       // Mocking (for UseCases/Services)
        }
    }
}
```

---

## Test Structure

> **Reference**: `LoginViewModelTest.kt`, `MpayQrViewModelTest.kt`, `ScanQrViewModelTest.kt`
>
> Key patterns from reference projects:
> - Use `StandardTestDispatcher()` with explicit `Dispatchers.setMain/resetMain`
> - Dispatch actions via `viewModel.trySendAction(Action.X)`
> - Assert state with `viewModel.stateFlow.value.fieldName` (NOT Turbine)
> - Assert events with `viewModel.eventFlow.test { awaitItem() }` (Turbine)
> - Call `advanceUntilIdle()` after dispatching actions
> - Use `@OptIn(ExperimentalCoroutinesApi::class)` on the test class
> - Test names use `givenX_whenY_thenZ` convention (no backtick strings)

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class ${Feature}ViewModelTest {
    // ===============================================================
    // SETUP
    // ===============================================================

    private val testDispatcher = StandardTestDispatcher()

    // Option A: Mokkery mocks (for UseCases or interfaces you don't own)
    private val mockUseCase: ${Feature}UseCase = mock()

    // Option B: Hand-written fakes (for repositories with simple state)
    private lateinit var fakeRepository: Fake${Feature}Repository

    private lateinit var viewModel: ${Feature}ViewModel

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

    // ===============================================================
    // INITIAL STATE TESTS
    // ===============================================================

    @Test
    fun givenInitialState_whenViewModelCreated_thenHasCorrectDefaults() {
        assertEquals("", viewModel.stateFlow.value.username)
        assertEquals("", viewModel.stateFlow.value.password)
        assertNull(viewModel.stateFlow.value.dialogState)
    }

    // ===============================================================
    // ACTION HANDLING TESTS (trySendAction + advanceUntilIdle)
    // ===============================================================

    @Test
    fun givenInput_whenActionDispatched_thenStateUpdated() = runTest {
        viewModel.trySendAction(${Feature}Action.NameChanged("Alice"))
        advanceUntilIdle()

        assertEquals("Alice", viewModel.stateFlow.value.name)
    }

    @Test
    fun givenToggleAction_whenDispatchedTwice_thenStateCycles() = runTest {
        assertFalse(viewModel.stateFlow.value.isVisible)

        viewModel.trySendAction(${Feature}Action.ToggleVisibility)
        advanceUntilIdle()
        assertTrue(viewModel.stateFlow.value.isVisible)

        viewModel.trySendAction(${Feature}Action.ToggleVisibility)
        advanceUntilIdle()
        assertFalse(viewModel.stateFlow.value.isVisible)
    }

    // ===============================================================
    // ASYNC OPERATION TESTS (with Mokkery mocks)
    // ===============================================================

    @Test
    fun givenSuccessResponse_whenSubmitClicked_thenNoErrorShown() = runTest {
        // Arrange: mock UseCase to return success
        everySuspend {
            mockUseCase.invoke("user", "pass")
        } returns DataState.Success(result)

        // Act: dispatch actions
        viewModel.trySendAction(${Feature}Action.UsernameChanged("user"))
        viewModel.trySendAction(${Feature}Action.PasswordChanged("pass"))
        viewModel.trySendAction(${Feature}Action.SubmitClicked)
        advanceUntilIdle()

        // Assert: verify mock was called
        verifySuspend {
            mockUseCase.invoke("user", "pass")
        }

        // Assert: no error dialog
        assertNull(viewModel.stateFlow.value.dialogState)
    }

    @Test
    fun givenErrorResponse_whenSubmitClicked_thenErrorDialogShown() = runTest {
        everySuspend {
            mockUseCase.invoke("bad", "creds")
        } returns DataState.Error(Exception("Invalid Credentials"))

        viewModel.trySendAction(${Feature}Action.UsernameChanged("bad"))
        viewModel.trySendAction(${Feature}Action.PasswordChanged("creds"))
        viewModel.trySendAction(${Feature}Action.SubmitClicked)
        advanceUntilIdle()

        verifySuspend {
            mockUseCase.invoke("bad", "creds")
        }

        val dialog = viewModel.stateFlow.value.dialogState
        assertIs<${Feature}State.DialogState.Error>(dialog)
        assertEquals("Invalid Credentials", dialog.message)
    }

    // ===============================================================
    // EVENT TESTS (use Turbine for eventFlow only)
    // ===============================================================

    @Test
    fun whenNavigateBackClicked_thenNavigateBackEventEmitted() = runTest {
        viewModel.eventFlow.test {
            viewModel.trySendAction(${Feature}Action.BackClicked)
            assertIs<${Feature}Event.NavigateBack>(awaitItem())
        }
    }

    @Test
    fun givenSuccessfulSubmit_whenCompleted_thenNavigationEventEmitted() = runTest {
        // Setup mocks for successful submission...
        everySuspend { mockUseCase.invoke(any(), any()) } returns DataState.Success(result)

        viewModel.trySendAction(${Feature}Action.UsernameChanged("user"))
        viewModel.trySendAction(${Feature}Action.PasswordChanged("pass"))
        viewModel.trySendAction(${Feature}Action.SubmitClicked)
        advanceUntilIdle()

        viewModel.eventFlow.test {
            assertTrue(awaitItem() is ${Feature}Event.NavigateToNext)
        }
    }

    // ===============================================================
    // DIALOG TESTS
    // ===============================================================

    @Test
    fun givenDialogVisible_whenDismissed_thenDialogStateIsNull() = runTest {
        // Trigger dialog
        viewModel.trySendAction(${Feature}Action.ShowDialog)
        advanceUntilIdle()
        assertNotNull(viewModel.stateFlow.value.dialogState)

        // Dismiss dialog
        viewModel.trySendAction(${Feature}Action.DismissDialog)
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
fun givenInitialState_whenViewModelCreated_thenHasCorrectDefaults() {
    assertEquals("", viewModel.stateFlow.value.fieldName)
    assertNull(viewModel.stateFlow.value.dialogState)
}
```

### 2. Action Handling Tests

Test each action in the Action sealed interface. Always use `trySendAction` + `advanceUntilIdle()`.

```kotlin
@Test
fun givenAction_whenDispatched_thenStateUpdated() = runTest {
    viewModel.trySendAction(${Feature}Action.SomeAction(param))
    advanceUntilIdle()

    assertEquals(expected, viewModel.stateFlow.value.field)
}
```

### 3. Async Operation Tests (Mokkery)

For tests involving suspend calls, use Mokkery to mock dependencies.

```kotlin
// Setup mock
everySuspend { useCase.invoke(any()) } returns DataState.Success(data)

// Dispatch action
viewModel.trySendAction(Action.Submit)
advanceUntilIdle()

// Verify mock was called
verifySuspend { useCase.invoke(any()) }

// Assert state
assertNull(viewModel.stateFlow.value.dialogState)
```

### 4. Event Tests (Turbine)

Test navigation and one-time events. Use Turbine ONLY for `eventFlow`.

```kotlin
@Test
fun whenActionTriggered_thenEventEmitted() = runTest {
    viewModel.eventFlow.test {
        viewModel.trySendAction(Action.NavigateBack)
        assertIs<Event.OnNavigateBack>(awaitItem())
    }
}
```

### 5. Validation Tests

Test form validation logic.

```kotlin
@Test
fun givenEmptyInput_whenSubmitClicked_thenErrorDialogShown() = runTest {
    viewModel.trySendAction(Action.SubmitClicked)
    advanceUntilIdle()

    assertTrue(viewModel.stateFlow.value.dialogState is DialogState.Error)
}
```

---

## Coroutine Setup (StandardTestDispatcher)

All ViewModel tests MUST set up the test dispatcher:

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class MyViewModelTest {
    private val testDispatcher = StandardTestDispatcher()

    @BeforeTest
    fun setUp() {
        Dispatchers.setMain(testDispatcher)
    }

    @AfterTest
    fun tearDown() {
        Dispatchers.resetMain()
    }
}
```

**Why StandardTestDispatcher (not UnconfinedTestDispatcher)?**
- `StandardTestDispatcher` gives precise control over coroutine execution
- Requires `advanceUntilIdle()` after dispatching actions (matches reference pattern)
- Avoids test flakiness from uncontrolled coroutine scheduling

---

## Mokkery vs Fakes

The reference projects use BOTH approaches:

| Approach | When to Use | Example |
|----------|-------------|---------|
| **Mokkery mocks** | For UseCases, external interfaces you don't own | `LoginUseCase`, `SearchRepository` |
| **Hand-written fakes** | For repositories with simple state, MutableStateFlow-backed | `FakeUserPreferencesRepository` |

### Mokkery Imports

```kotlin
import dev.mokkery.answering.returns
import dev.mokkery.everySuspend
import dev.mokkery.mock
import dev.mokkery.verifySuspend
import dev.mokkery.matcher.any
```

---

## Turbine Usage

### Use Turbine ONLY for eventFlow

```kotlin
// CORRECT: Turbine for eventFlow (Channel-based, hot flow)
viewModel.eventFlow.test {
    viewModel.trySendAction(Action.BackClicked)
    assertIs<Event.NavigateBack>(awaitItem())
}

// INCORRECT: Don't use Turbine for stateFlow (use .value instead)
// viewModel.stateFlow.test { ... }  // DON'T DO THIS
```

### Why not Turbine for stateFlow?

- `stateFlow` is a `StateFlow` -- you can read `.value` directly
- Reference tests consistently use `viewModel.stateFlow.value.field`
- `eventFlow` is a Channel-based flow -- you MUST collect to receive events

### Common Turbine Methods

| Method | Purpose |
|--------|---------|
| `awaitItem()` | Wait for next emission |
| `cancelAndIgnoreRemainingEvents()` | Clean up |
| `assertIs<Type>(awaitItem())` | Type-safe assertion |

---

## Test Naming Convention

Reference projects use the `givenX_whenY_thenZ` pattern:

```kotlin
// CORRECT (works in commonTest / Kotlin/Native)
@Test
fun givenValidCredentials_whenLoginClicked_thenNavigateToHome()

@Test
fun givenEmptyUsername_whenSubmitClicked_thenErrorDialogShown()

// INCORRECT (backtick names don't work in Kotlin/Native)
// @Test fun `valid credentials navigate to home`()
```

---

## Test Coverage Checklist

For each ViewModel, test:

- [ ] Initial state (default field values, null dialog state)
- [ ] Each action in Action sealed interface
- [ ] State changes after action dispatch
- [ ] Error dialog shown on failure
- [ ] Error dialog message content
- [ ] Each event in Event sealed interface
- [ ] Event emission timing (before/after advanceUntilIdle)
- [ ] Dialog show/dismiss cycle
- [ ] Validation errors (if applicable)
- [ ] Mock verification (verifySuspend)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `advanceUntilIdle()` | Always call after `trySendAction` with `StandardTestDispatcher` |
| Using Turbine for stateFlow | Use `viewModel.stateFlow.value.field` instead |
| Using backtick test names | Use `givenX_whenY_thenZ` (works in Kotlin/Native) |
| Missing `@OptIn(ExperimentalCoroutinesApi::class)` | Add to class |
| Forgetting `SavedStateHandle()` | Most ViewModels require it in constructor |
| Not using `runTest` | Wrap all coroutine tests in `runTest { }` |
| Missing `Dispatchers.resetMain()` | Add in `@AfterTest` to avoid test pollution |
| Using `UnconfinedTestDispatcher` | Use `StandardTestDispatcher` to match reference pattern |

---

## Progressive Test Helpers (Complex Form Testing)

> **Reference**: `SignUpViewModelTest.kt` (816 lines) from mobile-wallet.
> For ViewModels with many input fields (sign-up, profile edit, KYC forms),
> use **chained helper functions** where each helper builds on the previous one.
> This eliminates duplication and lets tests specify exactly how far through the
> form the user has progressed.

### Pattern

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class ${Feature}ViewModelTest {

    // ... setUp / tearDown ...

    // ─────────────────────────────────────────────────────────────────
    // PROGRESSIVE TEST HELPERS
    // Each helper calls the previous, building up form state step-by-step.
    // Tests call the helper that matches the "given" precondition.
    // ─────────────────────────────────────────────────────────────────

    private fun enterFirstName() {
        viewModel.trySendAction(${Feature}Action.FirstNameChanged("John"))
    }

    private fun enterLastName() {
        enterFirstName()
        viewModel.trySendAction(${Feature}Action.LastNameChanged("Doe"))
    }

    private fun enterUserName() {
        enterLastName()
        viewModel.trySendAction(${Feature}Action.UserNameChanged("john_doe"))
    }

    private fun enterMobileNumber() {
        enterUserName()
        viewModel.trySendAction(${Feature}Action.MobileNumberChanged("9876543210"))
    }

    private fun enterEmail() {
        enterMobileNumber()
        viewModel.trySendAction(${Feature}Action.EmailChanged("john@example.com"))
    }

    private fun enterPassword() {
        enterEmail()
        viewModel.trySendAction(${Feature}Action.PasswordChanged("SecurePass123!"))
    }

    private fun enterAddress() {
        enterPassword()
        viewModel.trySendAction(${Feature}Action.AddressChanged("123 Main St"))
    }

    /** Fills ALL form fields. Call this for happy-path tests. */
    private fun enterAllFields() {
        enterAddress()
        // Add more fields as needed; the chain continues from the last one.
    }

    // ─────────────────────────────────────────────────────────────────
    // TESTS USING PROGRESSIVE HELPERS
    // ─────────────────────────────────────────────────────────────────

    @Test
    fun givenOnlyFirstName_whenSubmitClicked_thenLastNameErrorShown() = runTest {
        enterFirstName()  // Only first name is filled
        viewModel.trySendAction(${Feature}Action.SubmitClicked)
        advanceUntilIdle()

        assertIs<DialogState.Error>(viewModel.stateFlow.value.dialogState)
    }

    @Test
    fun givenMissingEmail_whenSubmitClicked_thenEmailErrorShown() = runTest {
        enterUserName()  // firstName + lastName + userName filled, but no email
        viewModel.trySendAction(${Feature}Action.SubmitClicked)
        advanceUntilIdle()

        assertIs<DialogState.Error>(viewModel.stateFlow.value.dialogState)
    }

    @Test
    fun givenAllFieldsFilled_whenSubmitClicked_thenNoErrorShown() = runTest {
        enterAllFields()
        viewModel.trySendAction(${Feature}Action.SubmitClicked)
        advanceUntilIdle()

        assertNull(viewModel.stateFlow.value.dialogState)
    }
}
```

### When to Use Progressive Helpers

| Scenario | Use Progressive Helpers? |
|----------|:------------------------:|
| Form with 3+ required fields | Yes |
| Form with field-level validation | Yes |
| Simple 1-2 field forms | No -- inline is fine |
| Multi-step wizard forms | Yes (one chain per step) |

### Key Benefits

- **Partial fill testing**: Each helper stops at a specific field, making it easy to test "missing field X" scenarios.
- **No duplication**: Adding a new field means updating one helper and extending the chain.
- **Readable tests**: `enterEmail()` is self-documenting compared to 5 lines of `trySendAction`.
- **Reference validates pattern**: mobile-wallet's 816-line SignUpViewModelTest uses this exact approach for 12+ fields.

---

## Multi-Event Testing (Sequential Turbine Assertions)

> **Reference**: `SignUpViewModelTest.kt` from mobile-wallet.
> When a single action produces **multiple events** (e.g., show toast THEN navigate),
> use sequential `awaitItem()` calls inside `eventFlow.test { }`.

### Pattern

```kotlin
@Test
fun givenValidInputs_whenSignUpSucceeds_thenShowToastAndNavigate() = runTest {
    // Arrange: mock successful sign-up
    everySuspend {
        mockUseCase.invoke(any(), any())
    } returns DataState.Success(userInfo)

    enterAllFields()
    viewModel.trySendAction(${Feature}Action.SubmitClicked)
    advanceUntilIdle()

    // Assert: multiple events emitted in order
    viewModel.eventFlow.test {
        // First event: toast
        val toastEvent = awaitItem()
        assertIs<${Feature}Event.ShowToast>(toastEvent)
        assertEquals("Registration successful", toastEvent.message)

        // Second event: navigation
        val navEvent = awaitItem()
        assertIs<${Feature}Event.NavigateToLogin>(navEvent)
        assertEquals("john_doe", navEvent.username)
    }
}
```

### When an Action Emits Multiple Events

```kotlin
@Test
fun givenDeleteConfirmed_whenDeleteSucceeds_thenShowToastAndNavigateBack() = runTest {
    everySuspend { mockUseCase.delete(any()) } returns DataState.Success(Unit)

    viewModel.trySendAction(${Feature}Action.ConfirmDelete(itemId = 42L))
    advanceUntilIdle()

    viewModel.eventFlow.test {
        val toast = awaitItem()
        assertIs<${Feature}Event.ShowToast>(toast)

        val nav = awaitItem()
        assertIs<${Feature}Event.NavigateBack>(nav)
    }
}
```

### Rules for Multi-Event Testing

| Rule | Details |
|------|---------|
| Order matters | `awaitItem()` returns events in emission order |
| Type-check each | Use `assertIs<>` for type safety on each event |
| Assert payloads | Check event data (message, ID, etc.) after type assertion |
| Timeout | `awaitItem()` has a default timeout -- if no event arrives, test fails |
| Single event shorthand | For single events, the existing `assertIs<>(awaitItem())` one-liner is fine |

---

## Advanced Mokkery Matcher Patterns

> **Reference**: mobile-wallet tests use `dev.mokkery.matcher.*` for flexible argument matching.

### Imports

```kotlin
import dev.mokkery.matcher.any
import dev.mokkery.matcher.eq
import dev.mokkery.matcher.logical.or
import dev.mokkery.matcher.logical.and
import dev.mokkery.matcher.logical.not
```

### OR Matching (Multiple Valid Values)

```kotlin
// Accept either username or mobile number for search
everySuspend {
    mockSearchRepository.searchResources(
        or(eq("john_doe"), eq("9876543210")),
        any(),
        any()
    )
} returns DataState.Success(emptyList())
```

### Specific Value Matching with `eq()`

```kotlin
// Verify exact parameters were passed
verifySuspend {
    mockUserRepository.assignClientToUser(eq(123), eq(456))
}
```

### Wildcard with `any()`

```kotlin
// Match any value for parameters you don't care about
everySuspend {
    mockUseCase.invoke(any(), any())
} returns DataState.Success(result)
```

### Combining Matchers

```kotlin
// All matchers in a single mock call must use matcher functions
// (cannot mix literal values and matchers)
everySuspend {
    mockRepo.search(eq("query"), any(), eq(10))
} returns searchResults

// INCORRECT: mixing literals and matchers
// everySuspend { mockRepo.search("query", any(), 10) }  // WON'T COMPILE
```

### Verification with Specific Values

```kotlin
@Test
fun givenValidInputs_whenSubmitted_thenRepositoryCalledWithCorrectParams() = runTest {
    enterAllFields()
    viewModel.trySendAction(${Feature}Action.SubmitClicked)
    advanceUntilIdle()

    verifySuspend {
        mockRepository.createUser(
            eq("John"),
            eq("Doe"),
            eq("john_doe"),
            eq("john@example.com")
        )
    }
}
