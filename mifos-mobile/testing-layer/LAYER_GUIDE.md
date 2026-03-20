# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/testing-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-20"

# Testing Layer Guide - mifos-mobile

> Conventions for testing infrastructure and patterns.

---

## Purpose

The testing layer provides shared testing utilities, fake implementations, fixtures, and test patterns for all feature modules.

---

## Directory Structure

```
testing-layer/
├── LAYER_STATUS.md        # Test coverage status
├── TEST_TAGS_INDEX.md     # O(1) TestTag lookup
├── TEST_PATTERNS.md       # Pattern reference
├── TEST_FIXTURES_INDEX.md # Fixture lookup
├── FAKE_REPOS_INDEX.md    # Fake repo lookup
├── LAYER_GUIDE.md         # This file
└── patterns/              # Detailed patterns
    ├── fake-repository.md
    ├── viewmodel-test.md
    ├── screen-test.md
    ├── integration-test.md
    └── screenshot-test.md
```

---

## Code Location

```
core/testing/src/
├── commonMain/kotlin/org/{{package}}/core/testing/
│   ├── di/TestModule.kt           # Koin test module
│   ├── fake/                       # Fake implementations
│   │   ├── FakeAuthRepository.kt
│   │   └── Fake{Feature}Repository.kt
│   ├── fixture/                    # Test data factories
│   │   ├── UserFixture.kt
│   │   └── {Entity}Fixture.kt
│   ├── rule/MainDispatcherRule.kt  # Coroutine test rule
│   ├── tags/                       # TestTag objects
│   │   ├── AuthTestTags.kt
│   │   └── {Feature}TestTags.kt
│   └── util/
│       ├── FlowTestExtensions.kt
│       └── TestCoroutineExtensions.kt
├── androidMain/kotlin/...
│   └── ComposeTestHelpers.kt
└── iosMain/kotlin/...
    └── IosTestUtils.kt
```

---

## Test Types

| Type | Location | Framework | Purpose |
|------|----------|-----------|---------|
| Unit | `commonTest` | kotlin-test | ViewModel, Repository |
| Screen | `androidInstrumentedTest` | Compose UI Test | UI behavior |
| Screenshot | `test` (Android) | Roborazzi | Visual regression |
| Integration | `androidTest` | Espresso | End-to-end |

---

## ViewModel Test Pattern

```kotlin
class FeatureViewModelTest {
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private lateinit var fakeRepository: FakeFeatureRepository
    private lateinit var viewModel: FeatureViewModel

    @Before
    fun setup() {
        fakeRepository = FakeFeatureRepository()
        viewModel = FeatureViewModel(fakeRepository)
    }

    @Test
    fun `initial state is loading`() = runTest {
        viewModel.uiState.test {
            assertEquals(FeatureUiState.Loading, awaitItem())
        }
    }
}
```

---

## Screen Test Pattern

```kotlin
class FeatureScreenTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun `shows content when loaded`() {
        composeTestRule.setContent {
            FeatureScreenContent(
                uiState = FeatureUiState.Success(testData),
                onAction = {},
                onNavigate = {}
            )
        }

        composeTestRule
            .onNodeWithTag(FeatureTestTags.CONTENT)
            .assertIsDisplayed()
    }
}
```

---

## Fake Repository Pattern

```kotlin
class FakeFeatureRepository : FeatureRepository {
    private val items = mutableListOf<Item>()
    var shouldReturnError = false

    override suspend fun getItems(): Result<List<Item>> {
        if (shouldReturnError) {
            return Result.failure(Exception("Test error"))
        }
        return Result.success(items)
    }

    fun addItem(item: Item) {
        items.add(item)
    }
}
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/gap-analysis testing` | Check test coverage |
| `/implement [feature]` | Phase 5 creates test stubs |
| `/verify-tests [feature]` | Run feature tests |
