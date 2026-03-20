# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/testing-layer/TEST_FIXTURES_INDEX.md"
# last_modified: "2026-03-20"

# Test Fixtures Index - O(1) Lookup

> **${FIXTURE_COUNT} fixtures** | Test data factories | **Last Updated**: ${DATE}

---

## Quick Lookup

| # | Feature | Fixture Class | Methods | Status |
|:-:|---------|---------------|---------|:------:|
| 1 | ${feature_1} | `${Feature1}Fixtures` | create(), createList() | Planned |
| 2 | ${feature_2} | `${Feature2}Fixtures` | create(), createList() | Planned |

---

## O(1) Path Pattern

```
core/testing/src/commonMain/kotlin/org/${package}/core/testing/fixtures/${Feature}Fixtures.kt
```

---

## Fixture Pattern

### Standard Structure

```kotlin
object ${Feature}Fixtures {

    /**
     * Creates a single test ${Model} with default values.
     *
     * @param id Optional custom ID
     * @param name Optional custom name
     */
    fun create(
        id: Long = 1L,
        name: String = "Test ${Feature}",
        // Add other common overrides
    ): ${Model} = ${Model}(
        id = id,
        name = name,
        // Default values
    )

    /**
     * Creates a list of test ${Model}s.
     *
     * @param count Number of items to create
     */
    fun createList(count: Int = 5): List<${Model}> =
        (1..count).map { index ->
            create(
                id = index.toLong(),
                name = "Test ${Feature} $index"
            )
        }

    /**
     * Creates test data for specific scenarios.
     */
    fun createEmpty(): ${Model} = create(name = "")

    fun createInvalid(): ${Model} = create(id = -1)
}
```

---

## Usage in Tests

```kotlin
@Test
fun `load success displays items`() = runTest {
    // Use fixtures for test data
    val testData = ${Feature}Fixtures.createList(5)
    fakeRepository.setLoadSuccess(testData)

    viewModel.loadData()

    viewModel.stateFlow.test {
        val state = expectMostRecentItem()
        assertEquals(5, (state.uiState as Success).data.size)
    }
}

@Test
fun `handles empty data`() = runTest {
    fakeRepository.setLoadSuccess(emptyList())

    viewModel.loadData()

    viewModel.stateFlow.test {
        val state = expectMostRecentItem()
        assertTrue((state.uiState as Success).data.isEmpty())
    }
}
```

---

## Common Fixture Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `create()` | Single item with defaults | `UserFixtures.create()` |
| `createList(n)` | List of n items | `UserFixtures.createList(10)` |
| `createEmpty()` | Empty/minimal item | `UserFixtures.createEmpty()` |
| `createInvalid()` | Invalid state for error tests | `UserFixtures.createInvalid()` |
| `createWith*()` | Specific scenario | `UserFixtures.createWithExpiredToken()` |

---

## Implementation Status

| Status | Count | Description |
|--------|-------|-------------|
| Done | 0 | Fully implemented |
| Planned | ${FIXTURE_COUNT} | Fixture needed |

---

## Checklist for New Fixture

- [ ] Object class named `${Feature}Fixtures`
- [ ] `create()` method with sensible defaults
- [ ] `createList(count)` method
- [ ] Common scenario helpers
- [ ] Added to this index
