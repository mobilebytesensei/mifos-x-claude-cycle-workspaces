# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/testing-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-20"

# Testing Layer Guide - mobile-wallet

> Test patterns and documentation

---

## Test Categories

| Category | Location | Framework |
|----------|----------|-----------|
| Unit Tests | `*/src/commonTest/` | kotlin-test |
| UI Tests | `*/src/androidTest/` | Compose UI Test |
| Screenshot Tests | `*/src/test/` | Paparazzi |

---

## Directory Structure

```
testing-layer/
├── LAYER_GUIDE.md         # This file
├── TEST_TAGS_INDEX.md     # Test tag registry
├── patterns/              # Test patterns
│   ├── VIEWMODEL_TEST.md
│   ├── SCREEN_TEST.md
│   └── INTEGRATION_TEST.md
└── fixtures/              # Test data
```

---

## Test Patterns

### ViewModel Testing

```kotlin
class HomeViewModelTest {
    private lateinit var viewModel: HomeViewModel
    private lateinit var fakeRepository: FakeAccountRepository

    @BeforeTest
    fun setup() {
        fakeRepository = FakeAccountRepository()
        viewModel = HomeViewModel(fakeRepository)
    }

    @Test
    fun `when load called, state updates with accounts`() = runTest {
        // Given
        fakeRepository.setAccounts(testAccounts)

        // When
        viewModel.onAction(HomeAction.Load)

        // Then
        assertEquals(testAccounts, viewModel.state.value.accounts)
    }
}
```

### Screen Testing

```kotlin
class HomeScreenTest {
    @get:Rule
    val composeRule = createComposeRule()

    @Test
    fun homeScreen_displaysAccountBalance() {
        composeRule.setContent {
            HomeScreen(
                state = HomeState(balance = "$1,234.56"),
                onAction = {}
            )
        }

        composeRule
            .onNodeWithText("$1,234.56")
            .assertIsDisplayed()
    }
}
```

---

## Fake Repositories

| Repository | Fake | Location |
|------------|------|----------|
| AccountRepository | FakeAccountRepository | `core/testing/` |
| AuthRepository | FakeAuthRepository | `core/testing/` |
| TransferRepository | FakeTransferRepository | `core/testing/` |

---

## Commands

| Command | Purpose |
|---------|---------|
| `/test [module]` | Run tests |
| `/gen-tests [feature]` | Generate tests |
| `/gap-analysis testing` | Check coverage |
